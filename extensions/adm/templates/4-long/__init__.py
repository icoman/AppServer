#
# Sample Long running process
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
        self.datetimeformat = "%d-%b-%Y %H:%M:%S"


app = MyAppModule()


def getApp():
    return app


@app.route('/')
@app.auth('access module')
def _():
    """
        Default view
    """
    title = 'Long running process'
    bs = app.get_beaker_session()
    userid = bs.get('userid') or 0
    userconfig = bs.get('userconfig') or {}
    data = dict(title=title)
    template_body = app._get_template('index.tpl')
    rendered_template = app.render_template(template_body, data)
    yield rendered_template
    time.sleep(1)
    N = int(userconfig.get('steps') or 1)
    for i in range(N):
        now = datetime.datetime.now().strftime(app.datetimeformat)
        msg = '{} - Test {}'.format(now, i)
        print(msg)
        yield '<script>info("{}");</script>'.format(msg)
        time.sleep(1)
    msg = 'End.'
    yield '<script>info("{}");</script>'.format(msg)
