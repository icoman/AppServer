#
# my module
#

"""

Your license message ...

"""

import bottle, os, time
import datetime
from appmodule import AppModule


class MyAppModule(AppModule):

    def init(self):
        """
            initialisation code
        """
        self.datetimeformat = "%d-%b-%Y %H:%M"


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
    title = 'Index page'
    return dict(title=title)


@app.route('/config')
@app.auth('access module')
@app.view('config.tpl')
def _():
    """
        Show config and object life
    """
    title = 'Module config'
    return dict(title=title)


@app.route('/info', method=["get", "post"])
@app.auth('access module')
@app.view('info.tpl')
def _():
    title = 'Info page'
    get_vars = bottle.request.query
    post_vars = bottle.request.forms
    d = dict(title=title, get_vars=get_vars, post_vars=post_vars)
    return d


@app.route('/test')
@app.auth('access module')
def _():
    print('test sleep')
    for i in range(10):
        print(i)
        time.sleep(1)
    print('end test sleep')
    return 'Test Page module: {}, Time: {}'.format(app.module_name,
                                                   datetime.datetime.now().strftime(app.datetimeformat))
