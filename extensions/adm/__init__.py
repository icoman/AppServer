#
# adm module
#

"""

MIT License

Copyright (c) 2019 Ioan Coman

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

import bottle
import sys
import os
import time
import json
from distutils import dir_util
from shutil import copyfile

from tools import html_redirect
from appmodule import AppModule

try:
    from thread import interrupt_main
except:
    from _thread import interrupt_main


class MyAppModule(AppModule):

    def init(self):
        """
            initialisation code
        """
        self.datetimeformat = "%d-%b-%Y %H:%M"
        #
        # json module config contains sensitive data (like SQL DSN)
        # and is accesible ony to ADMIN = users in group id=1
        #
        self.module_config['ADMIN'] = [1]  # Admin group
        # self.module_config['ANY'] = [-1, 0] #All users and Anonymous
        # self.module_config['USERS'] = [-1] #All users


app = MyAppModule()


def update_app(module_name, server_config):
    app.update(module_name, server_config)


@app.route('/')
@app.auth('access module')
@app.view('index.tpl')
def _():
    """
        Default view
    """
    title = 'Configure server modules'
    bs = app.get_beaker_session()
    server_folder = app.server_config['DATAFOLDER']
    extensions_folder = os.path.join(server_folder, app.server_config.get('extensions_folder', 'extensions'))
    templates_folder = os.path.join(app.module_folder, 'templates')
    allmodules = []
    for ext in os.listdir(extensions_folder):
        if os.path.isdir(os.path.join(extensions_folder, ext)) and not ext.startswith('_'):
            description_file = os.path.join(extensions_folder, ext, 'description.txt')
            description = ''
            if os.path.isfile(description_file):
                with open(description_file, 'rt') as f:
                    description = f.read()
            allmodules.append((ext, description))
    alltemplates = []
    for i in os.listdir(templates_folder):
        fullpath = os.path.join(templates_folder, i)
        if os.path.isdir(fullpath):
            filename = os.path.join(fullpath, 'description.txt')
            description = 'no description file'
            if os.path.isfile(filename):
                with open(filename) as f:
                    description = f.read()
            alltemplates.append((i, description))
    return dict(title=title, pyver=sys.version, allmodules=allmodules, alltemplates=alltemplates)


@app.post('/restart')
@app.auth('ADMIN')
def _():
    """
        Restart server.
        Only builtin admins (group=1) can do it.
    """
    print('Restarting server.')
    interrupt_main()
    return 'Server is restarting ...'


@app.post('/addmod')
@app.auth('admin module')
def _():
    """
        Add server modules.
    """
    module_folder = app.module_folder
    new_module_name = bottle.request.forms.newmodulename
    tmpl_name = bottle.request.forms.tmpl
    templates_folder = os.path.join(module_folder, 'templates')
    extensions_folder = os.path.join(module_folder, '..')
    custom_module_folder = os.path.join(extensions_folder, new_module_name)
    src_template_folder = os.path.join(templates_folder, tmpl_name)
    if os.path.isdir(custom_module_folder):
        return dict(ok=False, data="Module already exists!")
    dir_util.copy_tree(src_template_folder, custom_module_folder)
    old_test_file = os.path.join(custom_module_folder, '_test_module.py')
    new_test_file = os.path.join(custom_module_folder, 'test_module.py')
    if os.path.isfile(old_test_file):
        os.rename(old_test_file, new_test_file)
    return dict(ok=True, data=None)


@app.post('/chdscr')
@app.auth('admin module')
def _():
    """
        Change module description.
    """
    module_name = bottle.request.forms.get('module')
    module_description = bottle.request.forms.get('description')
    if module_name:
        server_folder = app.server_config['DATAFOLDER']
        extensions_folder = os.path.join(server_folder, app.server_config.get('extensions_folder', 'extensions'))
        custom_module_folder = os.path.join(extensions_folder, module_name)
        filename = os.path.join(custom_module_folder, 'description.txt')
        with open(filename, 'wt') as f:
            f.write(module_description)
    return dict(ok=True, data=None)


@app.post('/savecfg')
@app.auth('access module')
def _():
    """
        Save json config of user or of module.
    """
    bs = app.get_beaker_session()
    module_name = bottle.request.forms.module
    foruser = bottle.request.forms.foruser
    if foruser:
        username = bs.get('username')
        configFile = 'config_{}.json'.format(username)
    else:
        configFile = 'config.json'
        #
        # json module config contains sensitive data (like SQL DSN)
        # and is accesible ony to ADMIN = users in group id=1
        #
        if not app.check_user_in_groups(app.module_config.get('ADMIN')):
            return 'Access denied.'
    Referer = bottle.request.headers.get('Referer')
    if module_name:
        server_folder = app.server_config['DATAFOLDER']
        extensions_folder = os.path.join(server_folder, app.server_config.get('extensions_folder', 'extensions'))
        custom_module_folder = os.path.join(extensions_folder, module_name)
        config_file = os.path.join(custom_module_folder, configFile)
        with open(config_file) as f:
            data = json.loads(f.read())
        for i in data.get('data').keys():
            name = 'par{}'.format(i)
            value = bottle.request.forms.getall(name) or ''
            if data.get('data')[i]['type'] not in ('mc',):
                if value and len(value) == 1:
                    # because of getall
                    value = value[0]
            else:
                value = value or []
            data.get('data')[i]['value'] = value
        # delete oldest and rename old versions
        VERSIONS = int(app.server_config.get('keep config baks') or 0)
        if VERSIONS < 2:
            # at least 2 versions (baks) must be used
            VERSIONS = 2
        for cnt in range(VERSIONS - 1, 0, -1):
            oldfile = '{}.{}'.format(config_file, cnt)
            newfile = '{}.{}'.format(config_file, cnt - 1)
            if os.path.isfile(oldfile):
                os.remove(oldfile)
            if os.path.isfile(newfile):
                os.rename(newfile, oldfile)
        newfile = '{}.{}'.format(config_file, 0)
        if os.path.isfile(config_file):
            os.rename(config_file, newfile)
        with open(config_file, 'wb') as f:
            ret = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')).encode('utf-8')
            f.write(ret)
        if Referer:
            return html_redirect(Referer)
        else:
            return html_redirect('/{}'.format(module_name))


@app.post('/getcfg')
@app.auth('access module')
def _():
    """
        Load json config of user or of module
        as data source for generated edit form.
    """
    bs = app.get_beaker_session()
    module_name = bottle.request.forms.module
    foruser = bottle.request.forms.foruser
    if foruser:
        username = bs.get('username')
        configFile = 'config_{}.json'.format(username)
    else:
        configFile = 'config.json'
        #
        # json module config contains sensitive data (like SQL DSN)
        # and is accesible ony to ADMIN = users in group id=1
        #
        if not app.check_user_in_groups(app.module_config.get('ADMIN')):
            return dict(ok=False, data='Access denied.')
    if module_name:
        server_folder = app.server_config['DATAFOLDER']
        extensions_folder = os.path.join(server_folder, app.server_config.get('extensions_folder', 'extensions'))
        custom_module_folder = os.path.join(extensions_folder, module_name)
        config_file = os.path.join(custom_module_folder, configFile)
        if not os.path.exists(config_file):
            src_config_file = os.path.join(custom_module_folder, 'config_default_.json')
            if not os.path.exists(src_config_file):
                return dict(ok=False, data='No default config file.')
            copyfile(src_config_file, config_file)
            config_file = os.path.join(custom_module_folder, configFile)
        with open(config_file) as f:
            data = json.loads(f.read())
        # some groups data format fix
        for i in data.get('data').keys():
            if data.get('data')[i]['type'] in ('mc',):
                # mc = multiple checks = a list read by ajax post
                try:
                    _e = eval(str(data.get('data')[i]['value']) or "[]")
                    if type(_e) is not type([]):
                        _e = [_e]
                    _v = [int(x) for x in _e]
                except:
                    _v = []
                data.get('data')[i]['value'] = _v
        return dict(ok=True, data=data)
    return dict(ok=False, data='No module name')
