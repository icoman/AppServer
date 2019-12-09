#
# todo test module - add, update, delete
#

"""

MIT License

Copyright (c) 2017, 2018 Ioan Coman

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

DELETE_TESTS = True

import requests
import json
import os
import time
import datetime
import traceback


class ApiTests(object):
    def confirmCookie(self):
        f = self.session.get(self.url_confirmcookie, verify=False)
        # print(f.headers)
        print('Server: {}'.format(f.headers.get('Server', '-undefined-')))

    def login(self, user, password):
        p = self.session.post(self.url_login, {'user': user, 'password': password})
        # if is authenticated you get a redirect with meta http-equiv="refresh"
        searchString = '<meta http-equiv="refresh"'
        if -1 == p.text.find(searchString):
            # not authenticated
            return False
        else:
            return True


class TodoTests(ApiTests):

    def add(self, title, description, done='yes'):
        try:
            values = [title, description, done]
            data = dict(data=json.dumps(values))
            result = json.loads(self.session.post(self.url_add, data).text)
            ret = result['ok'], result['data']
        except Exception as ex:
            ret = False, str(ex)
        return ret

    def update(self, obid, title, description, done='yes'):
        try:
            values = [title, description, done]
            data = dict(data=json.dumps(values), id=obid)
            result = json.loads(self.session.post(self.url_update, data).text)
            ret = result['ok'], result['data']
        except Exception as ex:
            ret = False, str(ex)
        return ret

    def delete(self, obid):
        try:
            data = dict(id=obid)
            result = json.loads(self.session.post(self.url_delete, data).text)
            ret = result['ok'], result['data']
        except Exception as ex:
            ret = False, str(ex)
        return ret

    def __init__(self, base_url, modulename):
        print('Test {}/{}'.format(base_url, modulename))
        self.session = requests.session()
        self.url_confirmcookie = '{}/confirmcookie'.format(base_url)
        self.url_login = '{}/auth/login'.format(base_url)
        self.url_add = '{}/{}/add'.format(base_url, modulename)
        self.url_update = '{}/{}/update'.format(base_url, modulename)
        self.url_delete = '{}/{}/delete'.format(base_url, modulename)


def test_function():
    base_url = os.getenv('BASEURL', 'http://localhost')
    user = os.getenv('user', 'admin')
    password = os.getenv('password', 'admin')
    if __name__ == "__main__":
        modulename = os.getcwd().split(os.path.sep)[-1]
    else:
        L = __name__.split('.')
        if len(L) < 2:
            # ignore tests because script is in templates folder
            return
        modulename = L[-2]
    t = TodoTests(base_url, modulename)
    t.confirmCookie()
    flag_login = t.login(user, password)
    assert flag_login == True, 'Not authenticated.'
    N = 3
    print('Authenticated. Run {} tests.'.format(N))
    for i in range(N):
        print('')
        now = datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')
        name = 'Test #{}'.format(i)
        description = 'Module {}, {}'.format(modulename, now)
        ok, obid = t.add(name, '', 'yes')
        assert ok == True, 'Error add.'
        print('Add id #{} ok.'.format(obid))
        ok, obid2 = t.update(obid, name, description, 'no')
        assert obid == obid2, 'Error update.'
        print('Update #{} ok.'.format(obid))
        if DELETE_TESTS:
            ok, obid3 = t.delete(obid)
            assert ok, 'Error deleting.'
            print('Delete #{} ok.'.format(obid3))


if __name__ == "__main__":
    import sys

    py = sys.version_info
    py3k = py >= (3, 0, 0)
    try:
        test_function()
    except Exception as ex:
        print("Exception found: {}".format(ex))
        # traceback.print_exc(file=sys.stdout)
    msg = 'Program ends, press Enter.'
    if py3k:
        input(msg)
    else:
        raw_input(msg)
