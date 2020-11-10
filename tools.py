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
import string
import json
import bottle

py = sys.version_info
py3k = py >= (3, 0, 0)


def html_redirect(location):
    return '<!-- Redirect to "{0}" -->\n<html><meta http-equiv="refresh" content="0;url={0}"><body>Redirecting...</body></html>'.format(
        location)


def get_props(configFile):
    """
        Load webserver config
    """
    DATAFOLDER = os.getcwd()
    configFilename = os.path.sep.join((DATAFOLDER, configFile))
    if not os.path.isfile(configFilename):
        DATAFOLDER = os.path.sep.join((os.getcwd(), '..'))
        configFilename = os.path.sep.join((DATAFOLDER, configFile))
    ret = _get_props(configFilename, '=')
    ret['DATAFOLDER'] = DATAFOLDER
    return ret


def _get_props(filename, sep, comment=";#"):
    #
    # sep = separator and may be :, =, etc.
    # comment = a list of chars which define starting of comment
    #
    ret = {}
    overWriteProp = True
    # overWriteProp = False #props with same name are grouped into a list
    try:
        accumulator = ''
        flag = False
        with open(filename, "rt") as f:
            while True:
                line = f.readline()
                if not line:
                    # line must have at least '\r\n' (Windows) or '\n' (Unix)
                    break
                line = line.replace('\r', '')
                line = line.replace('\n', '')
                line = line.lstrip()
                if not line:
                    # line is empty
                    continue
                if line[0] in comment:
                    # line starts with a comment
                    continue
                for c in comment:
                    # remove commented section
                    ix = line.find(c)
                    if -1 != ix:
                        line = line[:line.find(c)]
                if line[-1] == '\\':
                    # current line will continue on next line
                    line = line[:-1]
                    if flag:
                        # add to accumulator
                        accumulator = ' '.join((accumulator, line))
                    else:
                        # set
                        accumulator = line
                    flag = True
                    continue
                if flag:
                    # add last part of line to accumulator
                    accumulator = ' '.join((accumulator, line))
                    line = accumulator
                    accumulator = ''
                    flag = False

                # split line to key and value
                ix = line.find(sep)
                if ix > 0:
                    key = line[:ix].rstrip()
                    value = line[ix + 1:].lstrip().rstrip()
                    try:
                        # if value might be a number
                        value = int(value)
                    except:
                        pass
                    if overWriteProp:
                        ret[key] = value
                    else:
                        # append
                        old = ret.get(key)
                        if old:
                            if type(old) is list:
                                # already a list
                                ret[key].append(value)
                            else:
                                ret[key] = [old, value]
                        else:
                            ret[key] = value
    except Exception as ex:
        print(ex)
    return ret


def _make_login_logout(user, icon, loginurl, logouturl):
    if user:
        title = 'Logout {}'.format(user)
        link = logouturl
    else:
        title = 'Login'
        link = loginurl
    if icon:
        icontitle = '<span class="glyphicon glyphicon-{}"></span> {}'.format(
            icon, title)
    else:
        icontitle = title
    return icontitle, link


def make_bootstrap_navbar(url, bs, menufile, loginurl, logouturl, brandurl, brandtitle):
    if py3k:
        userfullname = bs.get('userfullname') or bs.get('username')
    else:
        userfullname = (bs.get('userfullname') or bs.get('username')).encode('utf8')
    user_groups = bs.get('groups') or [0]
    navcode = ''
    L = []
    menuitem = []
    with open(menufile, 'rt') as f:
        for line in f.read().split('\n'):
            line = line.replace('\r', '')
            if line.startswith('#'):
                continue
            if not line.lstrip():
                continue
            link, title, icon, groups, description = line.split('|')
            if not groups:
                groups = '[-1]'  # Default is all authenticated users
            groups = json.loads(groups)
            if line[0] in string.whitespace:
                if menuitem:
                    menuitem[5].append(
                        (link.strip(), title, icon, groups, description))
            else:
                if menuitem:
                    L.append(menuitem)
                menuitem = [link, title, icon, groups, description, []]
    if menuitem:
        L.append(menuitem)
    for i in L:
        link, title, icon, groups, description, childs = i
        if icon:
            icontitle = '<span class="glyphicon glyphicon-{}"></span> {}'.format(
                icon, title)
        else:
            icontitle = title
        hasAccess = False
        for gr in user_groups:
            if gr in groups:
                hasAccess = True
                break
        if title == 'loginlogout':
            hasAccess = True
        if not hasAccess:
            continue
        if len(childs) > 0:
            menuchilds = ''
            for ch in childs:
                ch_link, ch_title, ch_icon, ch_groups, ch_description = ch
                hasAccess = False
                for gr in user_groups:
                    if gr in ch_groups:
                        hasAccess = True
                        break
                if title == 'loginlogout':
                    hasAccess = True
                if not hasAccess:
                    continue
                if ch_icon:
                    ch_icontitle = '<span class="glyphicon glyphicon-{}"></span> {}'.format(
                        ch_icon, ch_title)
                else:
                    ch_icontitle = ch_title
                if ch_title == 'loginlogout':
                    ch_icontitle, ch_link = _make_login_logout(
                        userfullname, ch_icon, loginurl, logouturl)
                if ch_description:
                    ch_descr = ' title="{}"'.format(ch_description)
                else:
                    ch_descr = ''
                if ch_link == url:
                    active = ' class="active"'
                else:
                    active = ''
                menuchilds += '\n<li{}><a href="{}"{}>{}</a></li>'.format(
                    active, ch_link, ch_descr, ch_icontitle)
            if link == url:
                active = ' active'
            else:
                active = ''
            navcode += '''
<li class="dropdown{}">
  <a href="#" title="{}" class="dropdown-toggle" data-toggle="dropdown">{}<b class="caret"></b></a>
  <ul class="dropdown-menu">{}</ul>
</li>'''.format(active, description, icontitle, menuchilds)
        else:
            # no childs
            if description:
                descr = ' title="{}"'.format(description)
            else:
                descr = ''
            if title == 'loginlogout':
                icontitle, link = _make_login_logout(
                    userfullname, icon, loginurl, logouturl)
            if link == url:
                active = ' active'
            else:
                active = ''
            navcode += '\n<li{}><a href="{}"{}>{}</a></li>'.format(
                active, link, descr, icontitle)
    if brandurl and brandtitle:
        brand = '<a href="{}" class="navbar-brand">{}</a>'.format(
            brandurl, brandtitle)
    else:
        brand = ''
    ret = '''
<header class="navbar navbar-inverse navbar-fixed-top bs-docs-nav" role="banner">
  <div class="container">
    <div class="navbar-header">
      <button class="navbar-toggle" type="button" data-toggle="collapse" data-target=".bs-navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
{brand}
    </div>
    <nav class="collapse navbar-collapse bs-navbar-collapse" role="navigation">
      <ul class="nav navbar-nav navbar-right">
      {navcode}
      </ul>
    </nav>
  </div>
</header>
'''.format(**dict(navcode=navcode, brand=brand))
    return ret


def load_config(config_file):
    """
        Load a webserver module config
        Use app from
            https://github.com/icoman/PropertiesEditor_v1
        to generate and edit config files
    """
    config = {}
    if os.path.isfile(config_file):
        with open(config_file, 'rt') as f:
            jsdoc = json.loads(f.read())
            data = jsdoc.get('data', {})
            for x in data:
                ob = data[x]
                name = ob.get('name')
                value = ob.get('value')
                if ob.get('type') in ('mc',):
                    # mc = multiple checks = a list read by ajax post
                    try:
                        _e = eval(str(value or "[]"))
                        if type(_e) is not type([]):
                            _e = [_e]
                        value = [int(x) for x in _e]
                    except:
                        value = []
                config[name] = value
    return config


class SSLWSGIRefServer(bottle.ServerAdapter):
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw):
                    # pylint: disable=E0211
                    pass

            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket(
            srv.socket,
            certfile='server.pem',  # path to certificate
            server_side=True)
        srv.serve_forever()


class myWaitressServer(bottle.ServerAdapter):
    # Multi-threaded, poweres Pyramid
    def run(self, handler):
        from waitress import serve
        serve(handler, host=self.host, port=self.port, threads=10)


class myPasteServer(bottle.ServerAdapter):
    # Multi-threaded, stable, tried and tested
    def run(self, handler):  # pragma: no cover
        from paste import httpserver
        httpserver.serve(handler, host=self.host, port=str(self.port),
                         **self.options)


class myCherryPyServer(bottle.ServerAdapter):
    # Multi-threaded and very stable
    def run(self, handler):  # pragma: no cover
        import wsgiserver
        self.options['bind_addr'] = (self.host, self.port)
        self.options['wsgi_app'] = handler

        certfile = self.options.get('certfile')
        if certfile:
            del self.options['certfile']
        keyfile = self.options.get('keyfile')
        if keyfile:
            del self.options['keyfile']

        server = wsgiserver.CherryPyWSGIServer(**self.options)
        if certfile:
            server.ssl_certificate = certfile
        if keyfile:
            server.ssl_private_key = keyfile

        try:
            server.start()
        finally:
            server.stop()


class myGeventWebSocketServer(bottle.ServerAdapter):
    # Use this for websocket support
    def run(self, handler):
        from gevent import pywsgi
        from geventwebsocket.handler import WebSocketHandler
        server = pywsgi.WSGIServer(
            (self.host, self.port), handler, handler_class=WebSocketHandler)
        server.serve_forever()
