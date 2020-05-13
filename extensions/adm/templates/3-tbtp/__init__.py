#
# Sample Test Bootstrap with Templates
#

"""

Your license message ...

"""

import bottle, os, time
import datetime
from appmodule import AppModule

app = AppModule()


def update_app(module_name, server_config):
    app.update(module_name, server_config)


@app.route('/')
@app.auth('access module')
@app.view('index.tpl')
def _():
    """
        Default view
    """
    title = 'Test Bootstrap with Templates'
    return dict(title=title)
