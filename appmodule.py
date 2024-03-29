"""

MIT License

Copyright (c) 2017-2019 Ioan Coman

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
import threading
import bottle

from tools import html_redirect, make_bootstrap_navbar, load_config


#
#   module config (config.json) is cached in AppModule
#   user config (config_xxx.json for user xxx) is cached in beaker session
#

class AppModule(bottle.Bottle):

    def __init__(self, catchall=True, autojson=True):
        super(AppModule, self).__init__(catchall, autojson)
        self.error_handler[404] = self._err_http_server
        self.error_handler[500] = self._err_http_server
        self._tpl_map_lock = threading.Lock()
        self._templates_map = {}

    def update(self, module_name, server_config, module_folder):
        """
            updates from main before bottle server starts
            when code parse extensions folder
            and dynamically loads the modules
        """
        self.server_config = server_config
        server_folder = server_config['DATAFOLDER']
        server_global_tplfolder = server_config.get('server_global_tplfolder')
        self.server_template_folder = os.path.join(
            server_folder, server_global_tplfolder)
        static_folder = server_config.get('static_folder')
        template_folder = server_config.get('template_folder')
        if module_name:
            self.module_name = module_name
            if module_folder:
                self.module_folder = module_folder
            else:
                extensions_folder = os.path.join(
                    server_folder, server_config.get('extensions_folder'))
                self.module_folder = os.path.join(extensions_folder, module_name)
        else:
            self.module_name = ''
            self.module_folder = server_folder
        self.login_url = server_config.get('login_url')
        self.module_static_folder = os.path.join(
            self.module_folder, static_folder)
        self.module_template_folder = os.path.join(
            self.module_folder, template_folder)
        # load module config - if config.json changed, must restart server to apply changes
        self.module_config = self.load_config('config.json')
        # call custom init
        self.init()

    def init(self):
        """
            place initialisation code
            into derived class
        """
        pass

    def auth(self, permission):
        """

        decorator function for check permission access

        permission is a string, a list or a tuple

        single permission:
          @app.auth('access module')
          def _():
              ...

        allow multiple permissions:
          @app.auth(['access module HC','access module FD'])
          def _():
              ...

        """
        saved_permission = permission

        def decorator(func):
            def wrapper(*args, **kwargs):
                # executed on each request
                if self.module_config.get('module disabled'):
                    return self.err_msg("Error", "Module disabled by admin")
                accesspath = '/{}{}'.format(self.module_name,
                                            bottle.request.path)
                if self.server_config.get('DEBUG'):
                    print('auth {} {}'.format(bottle.request.method, accesspath))
                # check permission
                authenticated = False
                permission = saved_permission
                if isinstance(permission, (str,)):
                    permission = [permission]
                for p in permission:
                    groups_list = self.module_config.get(p)
                    if self.check_user_in_groups(groups_list):
                        authenticated = True
                        break
                if not authenticated:
                    url = '{}?back={}'.format(self.login_url, accesspath)
                    return html_redirect(url)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def view(self, template_name):
        """
            decorator function for render template
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if self.module_config.get('module disabled'):
                    return self.err_msg("Error", "Module disabled by admin")
                else:
                    result = func(*args, **kwargs)
                    if isinstance(result, (dict,)):
                        # if function return a dict, then render a template
                        template_body = self._get_template(template_name)
                        return self.render_template(template_body, result)
                    else:
                        return result

            return wrapper

        return decorator

    def load_config(self, filename):
        """
            Load a config file:
                - module config
                - user config
        """
        config_file = os.path.join(self.module_folder, filename)
        return load_config(config_file)

    def _get_template(self, templateName):
        """
            return raw content of template
            try to cache results
        """
        ret = None
        if templateName:
            body = self._templates_map.get(templateName, None)
            if body is None:
                filename1 = os.path.join(
                    self.server_template_folder, templateName)
                filename2 = os.path.join(
                    self.module_template_folder, templateName)
                if os.path.isfile(filename1):
                    filename = filename1
                else:
                    filename = filename2
                with open(filename, 'rb') as f:
                    body = f.read()
                if not self.server_config.get('DEBUG'):
                    with self._tpl_map_lock:
                        self._templates_map[templateName] = body
            ret = body
        return ret

    def _update_data(self, data):
        """
            Inject some info into data used
            to render a template
        """
        bs = self.get_beaker_session()
        userid = bs.get('userid') or 0
        cookielaw_name = self.server_config.get('cookielaw_name')
        using_cookies = bottle.request.get_cookie(cookielaw_name)
        accesspath = '/{}{}'.format(self.module_name, bottle.request.path)
        if accesspath.endswith('/'):
            accesspath = accesspath[:-1]
        extra_data = dict(
            module_name=self.module_name,
            module_config=self.module_config,
            user_config=self.get_user_config(),
            userid=userid,
            using_cookies=using_cookies,
            navbar=self._get_navbar(accesspath)
        )
        data.update(extra_data)

    def render_template(self, template_body, dict_data):
        """
            populate a bottle template
            with a dictionary data
            starting from template_body
        """
        TEMPLATE_PATH = [self.server_template_folder,
                         self.module_template_folder]
        template = bottle.SimpleTemplate(template_body, lookup=TEMPLATE_PATH)
        data = dict_data.copy()
        self._update_data(data)
        return template.render(**data)

    def check_user_in_groups(self, access_groups):
        """
            Verify if user is member of at least one group from access_groups
        """
        # unauthenticated users has id group = 0 (Anonymous)
        # -1 is id of 'All Users' virtual group
        bs = self.get_beaker_session()
        access_groups = access_groups or []  # if access_groups is None
        if type(access_groups) is not type([]):  # access_groups is not a list
            access_groups = [access_groups]
        try:
            access_groups = [int(x) for x in access_groups]
        except:
            access_groups = []
        user_groups = bs.get('groups') or [0]
        userid = bs.get('userid') or 0
        authenticated = False
        if userid and (-1 in access_groups) or (1 in user_groups):
            # user is logged in
            # and -1 is in access_groups (all users access)
            # or 1 is in user_groups (user is in built in admin group)
            authenticated = True
        else:
            # check acces groups
            for gr_id in access_groups:
                if gr_id in user_groups:
                    authenticated = True
                    break
        return authenticated

    def get_beaker_session(self):
        """
            Build user http session
        """
        # obs: you can cache values in beaker_session
        cookielaw_name = self.server_config.get('cookielaw_name')
        if bottle.request.get_cookie(cookielaw_name):
            beaker_session = bottle.request.environ.get('beaker.session')
        else:
            # no cookies = no session
            beaker_session = {}
        return beaker_session

    def get_user_config(self):
        # Build user config on each access
        beaker_session = self.get_beaker_session()
        userconfig = {}
        userid = beaker_session.get('userid') or 0
        # if logged in and module config enable access to user config
        if userid and self.module_config.get('user config'):
            username = beaker_session.get('username')
            config_filename = 'config_{}.json'.format(username)
            try:
                userconfig = self.load_config(config_filename)
            except:
                # ignore error
                pass
        return userconfig



    def _get_navbar(self, accesspath):
        """
            Navigation bar for bootstrap menu
        """
        server_folder = self.server_config['DATAFOLDER']
        menufile = os.path.join(
            server_folder, self.server_config.get('menufile'))
        login_url = self.server_config.get('login_url')
        logout_url = self.server_config.get('logout_url')
        brand_url = self.server_config.get('brand_url')
        brand_title = self.server_config.get('brand_title')
        bs = self.get_beaker_session()
        navbar = make_bootstrap_navbar(
            accesspath, bs, menufile, login_url, logout_url, brand_url, brand_title)
        return navbar

    def _err_http_server(self, error):
        """
            Render an error message
            for http error codes 404 and 500
        """
        body = error.body
        exception = error.exception
        traceback = error.traceback
        title = exception or 'Server Error'
        data = dict(title=title, body=body, traceback=traceback)
        template_body = self._get_template('error.tpl')
        return self.render_template(template_body, data)

    def err_msg(self, title, body):
        """
            Render an error message
        """
        data = dict(title=title, body=body)
        template_body = self._get_template('error.tpl')
        return self.render_template(template_body, data)
