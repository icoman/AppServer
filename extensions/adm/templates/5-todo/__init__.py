#
# Todo module
#

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

import os, bottle, json, datetime
from appmodule import AppModule
from .modeldb import setupDB, Todo, MyS


class MyAppModule(AppModule):

    def init(self):
        DSN = self.module_config.get('DSN')
        try:
            setupDB(DSN)
        except:
            # ignore error here
            pass


app = MyAppModule()


def update_app(module_name, server_config):
    app.update(module_name, server_config)


@app.get('/static/<path:path>')
def _(path):
    return bottle.static_file(path, root=app.module_static_folder)


@app.route('/')
@app.auth('access module')
@app.view('index.tpl')
def _():
    '''
        Default view
    '''
    bs = app.get_beaker_session()
    user = bs.get('username')
    if user:
        title = 'Todo for {}'.format(user)
    else:
        title = 'Todo for Anonymous'
    return dict(user=user, title=title)


@app.post('/list')
@app.auth('access module')
def _():
    try:
        with MyS() as session:
            bs = app.get_beaker_session()
            userid = bs.get('userid', 0)
            filter = bottle.request.forms.filter
            if filter:
                q = session.query(Todo) \
                    .filter(Todo.title.like(u'%{}%'.format(filter)) | Todo.description.like(u'%{}%'.format(filter))) \
                    .order_by(Todo.id.asc())
            else:
                q = session.query(Todo).order_by(Todo.id.asc())
            L = []
            for i in q.all():
                d = {'id': i.id, 'userid': i.userid,
                     'userfullname': i.userfullname, 'title': i.title,
                     'dataora': i.dataora.strftime("%d-%b-%Y %H:%M:%S"),
                     'description': i.description,
                     'done': i.done}
                L.append(d)
            return dict(ok=True, data=L, userid=userid)
    except Exception as ex:
        return dict(ok=False, data=str(ex))


@app.post('/add')
@app.auth('access module')
def _():
    with MyS() as session:
        bs = app.get_beaker_session()
        userfullname = bs.get('userfullname', u'Anonymous')
        userid = bs.get('userid', 0)
        ob = Todo()
        ob.userid = userid
        ob.userfullname = userfullname
        data = json.loads(bottle.request.forms.data)
        ob.dataora = datetime.datetime.now()
        ob.title = data[0]
        ob.description = data[1]
        ob.done = (data[2] == 'yes')
        session.add(ob)
        session.commit()  # ob.id is available after commit
        obid = ob.id
        return dict(ok=True, data=obid)


@app.post('/delete')
@app.auth('access module')
def _():
    with MyS() as session:
        bs = app.get_beaker_session()
        userid = bs.get('userid', 0)
        todo_id = int(bottle.request.forms.get('id', 0))
        ob = session.query(Todo).filter(Todo.id == todo_id).first()
        if ob:
            obid = ob.id
            if userid == ob.userid:
                session.delete(ob)
            else:
                return dict(ok=False, data='Access denied.')
        else:
            obid = 0
        return dict(ok=True, data=obid)


@app.post('/update')
@app.auth('access module')
def _():
    with MyS() as session:
        bs = app.get_beaker_session()
        userfullname = bs.get('userfullname', u'Anonymous')
        userid = bs.get('userid', 0)
        todo_id = int(bottle.request.forms.get('id', 0))
        data = json.loads(bottle.request.forms.data)
        ob = session.query(Todo).filter(Todo.id == todo_id).first()
        if ob:
            obid = ob.id
            if userid == ob.userid:
                ob.userfullname = userfullname
                ob.dataora = datetime.datetime.now()
                ob.title = data[0]
                ob.description = data[1]
                ob.done = (data[2] == 'yes')
            else:
                return dict(ok=False, data='Access denied.')
        else:
            obid = 0
        return dict(ok=True, data=obid)
