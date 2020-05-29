#
# Modular python web app server with bottlepy,
# beaker and sqlalchemy for python2 and python3
#

"""

MIT License

Copyright (c) 2017-2020 Ioan Coman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import os
import sys
import time
import datetime
import importlib
import socket
import traceback

import bottle
from beaker.middleware import SessionMiddleware

from appmodule import AppModule
from tools import html_redirect, get_props
from tools import SSLWSGIRefServer, myWaitressServer, myPasteServer
from tools import myCherryPyServer, myGeventWebSocketServer


server_config = get_props('config.ini')

DEBUG = int(server_config.get('DEBUG', 0))
RELOADER = int(server_config.get('RELOADER', 0))

server_folder = server_config['DATAFOLDER']
extensions_folder = os.path.join(
    server_folder, server_config.get('extensions_folder'))
sessions_folder = os.path.join(
    server_folder, server_config.get('sessions_folder'))
sys.path.append(extensions_folder)

root = AppModule()
root.update(None, server_config)


@root.route('/')
def _():
    return html_redirect(server_config.get('home_url', '/adm'))


@root.route('/favicon.ico')
def _():
    return bottle.static_file('favicon.ico', root=root.module_static_folder)


@root.route('/static/<path:path>')
def _(path):
    return bottle.static_file(path, root=root.module_static_folder)


# for free ssl - https://zerossl.com/free-ssl/
@root.route('/.well-known/acme-challenge/<path:path>')
def _(path):
    return bottle.static_file(path, root=server_config.get('free_ssl_folder'))


# confirm accept cookie
@root.route('/confirmcookie')
def callback():
    expires = int(server_config.get('cookie_life') or 3)
    bottle.response.set_cookie(server_config.get('cookielaw_name'), 'yes',
                               expires=datetime.datetime.now() + datetime.timedelta(days=expires), path="/")
    return html_redirect(bottle.request.environ.get('HTTP_REFERER', '/'))


def session_setup():
    # Beaker session setup
    session_timeout = int(server_config.get(
        'session_timeout', 3600))  # Seconds
    random_session_keys = server_config.get('random_session_keys')
    if random_session_keys:
        # use random beaker session keys for single server
        from hashlib import sha512 as HASHFUNC
        hash = HASHFUNC()
        hash.update(os.urandom(300))
        session_encrypt_key = hash.hexdigest()
        hash.update(os.urandom(300))
        session_validate_key = hash.hexdigest()
    else:
        # change these keys and use them in a cluster
        session_encrypt_key = server_config.get('session_encrypt_key')
        session_validate_key = server_config.get('session_validate_key')

    return {
        # session stored only in cookie (max 4096 bytes) is best for cluster
        'session.type': 'cookie',

        # 'session.type':'file',
        # 'session.data_dir':sessions_folder,

        'session.path': '/',
        'session.httponly': True,
        'session.cookie_expires': True,

        # Seconds until the session is considered invalid, after which it will be
        # ignored and invalidated. This number is based on the time since the
        # session was last accessed, not from when the session was created.
        'session.timeout': session_timeout,

        # Whether or not the session cookie should be marked as secure.
        # When marked as secure, browsers are instructed to not send the cookie
        # over anything other than an SSL connection.
        'session.secure': False,

        # When set, calling the save() method is no longer required, and the
        # session will be saved automatically anytime its accessed during a request.
        'session.auto': True,
        'session.key': server_config.get('server_cookie_name'),
        'session.encrypt_key': session_encrypt_key,
        'session.validate_key': session_validate_key
    }


def load_modules():
    extensions_folder = os.path.join(
        server_folder, server_config.get('extensions_folder'))
    for module_name in os.listdir(extensions_folder):
        fullpath = os.path.join(extensions_folder, module_name)
        if not module_name.startswith('_') and os.path.isdir(fullpath):
            try:
                t1 = time.time()
                prefix = '/{}'.format(module_name)
                module = importlib.import_module(module_name)
                module.update_app(module_name, server_config)
                root.mount(prefix, module.app)
                t2 = time.time()
                if DEBUG:
                    print('\tLoading "{}" in {:.2f} sec'.format(
                        module_name, t2-t1))
            except Exception as ex:
                traceback.print_exc(file=sys.stdout)


def fix_frozen_apps():
    #
    # fix import for py2exe, cx_freeze, pyinstaller, ...
    #
    # import here whatever fail to import when application is frozen
    #
    #import pyodbc, pymssql, _mssql
    import pymssql
    import _mssql
    import sqlalchemy
    import sqlalchemy.sql
    import sqlalchemy.ext
    from sqlalchemy.sql import default_comparator
    from sqlalchemy.ext import declarative, baked

    # ImportError: No module named image, audio and message
    from email.mime.image import MIMEImage
    from email.mime.audio import MIMEAudio
    from email.mime.message import MIMEMessage
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    import PIL
    import qrcode
    import qrcode.image
    import qrcode.image.svg
    import markdown
    #import Crypto
    #import Crypto.Util

    # for server extensions
    import openpyxl
    import msgpackrpc
    import tools
    import appmodule


def main():
    '''
        Start bottle web server
    '''
    FROZEN = getattr(sys, 'frozen', False)
    PORT = int(server_config.get('PORT', 80))
    HOST = server_config.get('HOST', 'localhost')
    useSSL = int(server_config.get('useSSL', 0))
    useFCGI = int(server_config.get('useFCGI', 0))
    if not RELOADER or os.getenv('BOTTLE_CHILD'):
        print('Start web server on port {}.'.format(PORT))
        print('Hostname and IP:')
        for ip in socket.gethostbyname_ex(socket.gethostname()):
            if ip:
                print('\t{}'.format(ip))
        print('Python version: {}'.format(sys.version))
        if(FROZEN):
            print('Running frozen.')
        print('SSL = {}, FCGI = {}, DEBUG = {}, RELOADER = {}'.format(
            useSSL, useFCGI, DEBUG, RELOADER))
        t1 = time.time()
        load_modules()
        t2 = time.time()
        if DEBUG:
            print('Total loading modules: {:.2f} sec.\n'.format(t2-t1))

    if useSSL:
        webserver = SSLWSGIRefServer(host=HOST, port=PORT)
    else:
        if useFCGI:
            webserver = bottle.FlupFCGIServer
        else:
            '''
                gevent: works with patches and is quite good
                eventlet, tornado, wsgiref: pretty good
                cherrypy, twisted, waitress, paste: are only which works with multithreading
            '''
            webserver = server_config.get('webserver')
            if webserver == 'gevent':
                from gevent import monkey
                monkey.patch_all()
            if webserver == 'mywaitress':
                webserver = myWaitressServer
            if webserver == 'mypaste':
                webserver = myPasteServer
            if webserver == 'mycherrypy':
                webserver = myCherryPyServer
            if webserver == 'mygeventws':
                webserver = myGeventWebSocketServer

    session_root = SessionMiddleware(root, session_setup())
    bottle.run(app=session_root, server=webserver,
               host=HOST, port=PORT, debug=DEBUG, reloader=RELOADER)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)
        traceback.print_exc(file=sys.stdout)
