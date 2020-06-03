#
# Auth module: users, groups and menu
#

"""

MIT License

Copyright (c) 2020 Ioan Coman

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

import bottle, json, time
import os, sys, string, random, smtplib
from email.mime.text import MIMEText

import qrcode
import qrcode.image.svg

try:
    from StringIO import StringIO
except ImportError:
    # py3
    from io import BytesIO as StringIO

from appmodule import AppModule
from tools import html_redirect
from .modeldb import setupDB, MyS, Users, Groups

py   = sys.version_info
py3k = py >= (3, 0, 0)

def getRndString(n):
    ret = ''
    area = string.ascii_letters + string.digits
    for i in range(n):
        ix = random.randint(0, len(area) - 1)
        ret = ret + area[ix]
    return u'' + ret


class MyAppModule(AppModule):

    def init(self):
        DSN = self.module_config.get('DSN')
        try:
            setupDB(DSN)
        except:
            # ignore error here
            # the error message will be visible on login
            pass
        self.module_config['ANY'] = [-1, 0]  # All users and Anonymous
        self.module_config['ADMIN'] = [1]  # Admin group


app = MyAppModule()


def getApp():
    return app


#
# auth methods which return html:
#   view, index users, index groups, login, logout, confirm logout, reset password
#

@app.get('/static/<path:path>')
def _(path):
    return bottle.static_file(path, root=app.module_static_folder)


@app.get('/')
@app.auth('ANY')
@app.view('index.tpl')
def index_view():
    """
        Default view for /auth
    """
    title = 'Auth module'
    bs = app.get_beaker_session()
    user = bs.get('username', None)
    return dict(user=user, title=title)


@app.get('/users')
@app.auth('rw users')
@app.view('users.tpl')
def index_users():
    """
        View for /auth/users
    """
    title = 'Edit Users'
    bs = app.get_beaker_session()
    user = bs.get('username', None)
    return dict(user=user, title=title)


@app.get('/groups')
@app.auth('rw groups')
@app.view('groups.tpl')
def index_groups():
    """
        View for /auth/groups
    """
    title = 'Edit Groups'
    bs = app.get_beaker_session()
    user = bs.get('username', None)
    return dict(user=user, title=title)


@app.get('/logout')
@app.auth('ANY')
def logout():
    """
        Logout method
    """
    bs = app.get_beaker_session()
    try:
        bs.delete()
        confirm_logout = '/{}/confirmlogout'.format(app.module_name)
        return html_redirect(confirm_logout)
    except:
        return 'Logout Error'


@app.get('/confirmlogout')
@app.auth('ANY')
@app.view('logout.tpl')
def confirmlogout():
    """
        Display logout confirmation
    """
    title = 'Logout'
    return dict(title=title)


@app.route('/li', method=['get', 'post'])
@app.auth('ANY')
def login_info():
    """
        Login info for logged user
    """
    bs = app.get_beaker_session()
    user = bs.get('username', 'Anonymous')
    userid = int(bs.get('userid', 0))
    return dict(user=user, userid=userid)


@app.route('/login', method=['get', 'post'])
@app.auth('ANY')
@app.view('login.tpl')
def login():
    """
        Login dialog
    """
    title = 'Login'
    with MyS() as session:
        bs = app.get_beaker_session()
        notUsingCookies = type(bs) is dict
        back = bottle.request.forms.get('back', None)  # from HTML form with POST
        if not back:
            back = bottle.request.query.get('back', '/')  # from URL with GET
        if not back.startswith('/'):
            back = '/' + back
        emergency_admin_activated = app.server_config.get('emergency admin')
        if emergency_admin_activated:
            # Emergency Admin
            back = '/adm'
            EmergencyAdmin = bottle.request.query.EmergencyAdmin
            if EmergencyAdmin:
                print('Login Emergency Admin')
                bs.clear()
                # something random
                bs[getRndString(12)] = getRndString(32)
                bs['username'] = 'emadmin'
                bs['userfullname'] = 'Emergency Admin'
                bs['userid'] = 1
                bs['REMOTE_ADDR'] = bottle.request.environ.get('REMOTE_ADDR')
                # Emergency Admin groups: All users, Anonymous and Admins
                bs['groups'] = [-1, 0, 1]
                bs['authenticated'] = True
                # something random
                bs[getRndString(12)] = getRndString(32)
                return html_redirect(back)
        authenticated = False
        user = bottle.request.forms.user  # POST
        password = bottle.request.forms.password  # POST
        msg = ''
        if user:
            try:
                obuser = session.query(Users).filter(Users.name == user).first()
                if obuser:
                    if obuser._validate(password):
                        bs.clear()
                        # when password is correct, set the session cookie
                        # something random
                        bs[getRndString(12)] = getRndString(32)
                        bs['username'] = obuser.name
                        bs['userid'] = obuser.id
                        bs['userfullname'] = obuser.fullname
                        bs['REMOTE_ADDR'] = bottle.request.environ.get('REMOTE_ADDR')
                        # add group id -1 (All users)
                        L = [gr.id for gr in obuser.groups]
                        L.append(-1)
                        bs['groups'] = L
                        bs['authenticated'] = True
                        authenticated = True
                        # something random
                        bs[getRndString(12)] = getRndString(32)
                    else:
                        msg = "Invalid password"
                else:
                    msg = "Invalid user"
            except Exception as ex:
                # import sys, traceback
                # traceback.print_exc(file=sys.stdout)
                if emergency_admin_activated:
                    msg = 'SQL error: <b>{}</b>'.format(ex)
                else:
                    msg = '''SQL error: <b>{}</b>

Activate emergency admin in auth module and login
as emergency admin if this error persists.
'''.format(ex).replace('\n', '<br>')

    if authenticated:
        return html_redirect(back)
    else:
        # render login
        return dict(title=title, msg=msg, back=back,
                    emergency_admin_activated=emergency_admin_activated,
                    notUsingCookies=notUsingCookies)


@app.route('/users/reset', method=['GET', 'POST'])
@app.auth('ANY')
@app.view('resetpassw.tpl')
def resetpassw():
    """
        Reset password
    """
    title = 'Reset password'
    smtp_server = app.module_config.get('smtp server')
    if not smtp_server:
        return 'smtp server is not defined'
    msg = ''
    with MyS() as session:
        email = bottle.request.forms.email  # POST
        if email:
            user = session.query(Users).filter(Users.email == email).first()
            msg = 'If user exists, it will receive the password by email.'
            if user:
                try:
                    password = getRndString(7)
                    user.password = user._mkpass(password)
                    session.commit()
                    mailmsg = MIMEText(u'''
Your password has been reset.

User: {}
Password: {}

'''.format(user.name, password))
                    msg_from = app.module_config.get('msg from')
                    msg_to = email
                    mailmsg['Subject'] = 'Password reset'
                    mailmsg['From'] = msg_from
                    mailmsg['To'] = msg_to
                    # send mail
                    s = smtplib.SMTP(smtp_server)
                    s.sendmail(msg_from, [msg_to], mailmsg.as_string())
                    s.quit()
                    # print(mailmsg.as_string())
                except Exception as ex:
                    print(ex)
                    msg = str(ex)
    return dict(msg=msg, title=title)


#
# auth methods which return json:
#   all, list, add, update, delete users and groups
#

@app.post('/users/list')
@app.auth('rw users')
def _():
    """
        Json list of users
    """
    try:
        with MyS() as session:
            filter = bottle.request.forms.filter
            if filter:
                q = session.query(Users) \
                    .filter(Users.name.like(u'%{}%'.format(filter)) | Users.fullname.like(u'%{}%'.format(filter))) \
                    .order_by(Users.id.asc())
            else:
                q = session.query(Users).order_by(Users.id.asc())
            L = []
            for i in q.all():
                d = {'id': i.id, 'name': i.name, 'fullname': i.fullname, 'email': i.email,
                     'groups': [g.id for g in i.groups]}
                L.append(d)
        ret = dict(ok=True, data=L)
    except Exception as ex:
        ret = dict(ok=False, data=str(ex))
    return ret


@app.post('/groups/list')
@app.auth('rw groups')
def _():
    """
        Json list of groups
    """
    try:
        with MyS() as session:
            filter = bottle.request.forms.filter
            if filter:
                q = session.query(Groups) \
                    .filter(Groups.name.like(u'%{}%'.format(filter)) | Groups.description.like(u'%{}%'.format(filter))) \
                    .order_by(Groups.id.asc())
            else:
                q = session.query(Groups).order_by(Groups.id.asc())
            L = []
            for i in q.all():
                d = {'id': i.id, 'name': i.name, 'description': i.description}
                L.append(d)
            ret = dict(ok=True, data=L)
    except Exception as ex:
        ret = dict(ok=False, data=str(ex))
    return ret


@app.post('/groups/all')
@app.auth('ANY')
def _():
    """
        Json list of groups used by other modules.
        Anybody has access to this method.

        This method is used by ajax to populate
        list of groups from config file (a mc type property).
    """
    try:
        with MyS() as session:
            data = {}
            bs = app.get_beaker_session()
            try:
                allgr = session.query(Groups).all()
                d = {gr.id: (gr.name, gr.description) for gr in allgr}
                data.update(d)
                data.update({0: ('Anonymous', 'Any unauthenticated user')})
                data.update({-1: ('All users', 'All authenticated users')})
            except Exception as ex:
                if app.server_config.get('emergency admin'):
                    data = {1: ('Emergency Admins', 'Emergency admins group')}
                else:
                    data = str(ex)
            ret = dict(ok=True, data=data)
    except Exception as ex:
        ret = dict(ok=False, data=str(ex))
    return ret


@app.post('/users/update')
@app.auth('rw users')
def _():
    """
        Update user definition
    """
    try:
        with MyS() as session:
            _id = int(bottle.request.forms.get('id', 0))
            data = json.loads(bottle.request.forms.data)
            grlist = [ob for ob in session.query(Groups).all() if ob.name in data[-1]]
            ob = session.query(Users).filter(Users.id == _id).first()
            if ob:
                ob.fullname = data[0]
                ob.email = data[1]
                password = data[2]
                if password:
                    if len(password) >= int(app.module_config.get('min pass len') or 3):
                        ob.password = ob._mkpass(password)
                    else:
                        raise Exception('Password too short.')
                ob.groups = grlist
                session.commit()
                ret = dict(ok=True, id=ob.id, data=ob.id)
            else:
                raise Exception('User not found.')
    except Exception as ex:
        ret = dict(ok=False, data=str(ex), id=0)
    return ret


@app.post('/groups/update')
@app.auth('rw groups')
def _():
    """
        Update group definition
    """
    try:
        with MyS() as session:
            _id = int(bottle.request.forms.get('id', 0))
            data = json.loads(bottle.request.forms.data)
            ob = session.query(Groups).filter(Groups.id == _id).first()
            if ob:
                obid = ob.id
                ob.name = data[0]
                ob.description = data[1]
                ret = dict(ok=True, id=ob.id, data=ob.id)
            else:
                raise Exception('Group not found.')
    except Exception as ex:
        ret = dict(ok=False, id=0, data=str(ex))
    return ret


@app.post('/users/add')
@app.auth('rw users')
def _():
    """
        Add an user
    """
    try:
        with MyS() as session:
            data = json.loads(bottle.request.forms.data)
            username = data[0]
            fullname = data[1]
            email = data[2]
            password = data[3]
            user = session.query(Users).filter(Users.name == username).first()
            if user:
                raise Exception('User exists!')
            else:
                grlist = [ob for ob in session.query(Groups).all() if ob.name in data[-1]]
                ob = Users(username, password)
                ob.groups = grlist
                ob.fullname = fullname
                ob.email = email
                session.add(ob)
                session.commit()  # need commit to get ob.id
                obid = ob.id
                ret = dict(ok=True, id=obid, data=obid)
    except Exception as ex:
        ret = dict(ok=False, data=str(ex), id=0)
    return ret


@app.post('/groups/add')
@app.auth('rw groups')
def _():
    """
        Add a group
    """
    try:
        with MyS() as session:
            data = json.loads(bottle.request.forms.data)
            ob = Groups(data[0], data[1])
            session.add(ob)
            session.commit()  # need commit to get ob.id
            obid = ob.id
        ret = dict(ok=True, id=obid, data=obid)
    except Exception as ex:
        ret = dict(ok=False, id=0, data=str(ex))
    return ret


@app.post('/users/delete')
@app.auth('rw users')
def _():
    """
        Delete an user
    """
    try:
        with MyS() as session:
            _id = int(bottle.request.forms.get('id', 0))
            if _id > 2:
                ob = session.query(Users).filter(Users.id == _id).first()
                if ob:
                    obid = ob.id
                    session.delete(ob)
                    ret = dict(ok=True, data=obid)
                else:
                    raise Exception('User not found.')
            else:
                raise Exception('It is not allowed to delete first 2 users!')
    except Exception as ex:
        ret = dict(ok=False, data=str(ex))
    return ret


@app.post('/groups/delete')
@app.auth('rw groups')
def _():
    """
        Delete a group
    """
    try:
        with MyS() as session:
            _id = int(bottle.request.forms.get('id', 0))
            if _id > 2:
                ob = session.query(Groups).filter(Groups.id == _id).first()
                if ob:
                    obid = ob.id
                    session.delete(ob)
                    ret = dict(ok=True, data=obid)
                else:
                    raise Exception('Group not found.')
            else:
                raise Exception('It is not allowed to delete first 2 groups!')
    except Exception as ex:
        ret = dict(ok=False, data=str(ex))
    return ret


@app.get('/users/qrscan')
@app.auth('ANY')
def _():
    """
        Login with token
    """
    code = bottle.request.query.code
    # format = bottle.request.query.format
    # type = bottle.request.query.type
    bs = app.get_beaker_session()
    token = code.split('=')[-1]
    with MyS() as session:
        obuser = session.query(Users).filter(Users.token == token).first()
        if obuser:
            # user is logged in
            bs.clear()
            bs[getRndString(12)] = getRndString(32)
            bs['username'] = obuser.name
            bs['userid'] = obuser.id
            bs['userfullname'] = obuser.fullname
            bs['REMOTE_ADDR'] = bottle.request.environ.get('REMOTE_ADDR')
            # add group id -1 (All users)
            L = [gr.id for gr in obuser.groups]
            L.append(-1)
            bs['groups'] = L
            bs['authenticated'] = True
            # something random
            bs[getRndString(12)] = getRndString(32)
            return html_redirect('/')
        else:
            # return 'No access! Invalid or expired token.'
            return html_redirect('/auth/login')


@app.get('/qrcode')
@app.auth('rw users')
@app.view('qrcode.tpl')
def _():
    """
        Generate qrcode used for login with token
    """
    new = bottle.request.query.new
    username = bottle.request.query.user
    url = bottle.request.query.url
    if username:
        with MyS() as session:
            obuser = session.query(Users).filter(Users.name == username).first()
            if obuser:
                if new:
                    obuser._gen_token()
                token = obuser.token
                fullname = obuser.fullname
            else:
                raise Exception("User not found!")

        title = '{}'.format(fullname)
        # Simple factory, just a set of rects.
        # factory = qrcode.image.svg.SvgImage
        # Fragment factory (also just a set of rects)
        # factory = qrcode.image.svg.SvgFragmentImage
        # Combined path factory, fixes white space that may occur when zooming
        factory = qrcode.image.svg.SvgPathImage
        # fill the background of the SVG with white:
        # factory = qrcode.image.svg.SvgFillImage
        # factory = qrcode.image.svg.SvgPathFillImage

        #if py3k:
        #    import urllib.parse
        #    quote = urllib.parse.quote
        #else:
        #    import urllib
        #    quote = urllib.pathname2url
        #qrdata = '{}?owner={}&code={}'.format(url, quote(username), token)
        qrdata = '{}?owner={}&code={}'.format(url, username, token)
        img = qrcode.make(qrdata, image_factory=factory)
        output = StringIO()
        img.save(output)
        imgout = output.getvalue()

        return dict(title=title, imgout=imgout, qrdata=qrdata)
