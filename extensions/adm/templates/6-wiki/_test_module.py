#
# wiki test module - create, edit, delete version, delete page with all versions
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


class WikiTests(ApiTests):

    def create(self, pagePath, pageTitle, pageBody):
        try:
            data = dict(pagetitle=pageTitle, body=pageBody)
            url = '{}/{}'.format(self.url_create, pagePath)
            result = json.loads(self.session.post(url, data).text)
            ret = result['ok'], result['data'][0], result['data'][1]
        except Exception as ex:
            print(ex)
            ret = False, str(ex)
        return ret

    def edit(self, pagePath, pageTitle, pageBody, edited_version_id):
        try:
            data = dict(pagetitle=pageTitle,
                        body=pageBody, edited_version_id=edited_version_id)
            url = '{}/{}'.format(self.url_edit, pagePath)
            result = json.loads(self.session.post(url, data).text)
            ret = result['ok'], result['data']
        except Exception as ex:
            ret = False, str(ex)
        return ret

    def deleteversion(self, pagePath, version_index):
        ret = True
        try:
            url = '{}/{}?v={}'.format(self.url_deletever, pagePath, version_index)
            g = self.session.get(url)
            searchString = '<meta http-equiv="refresh"'
            if -1 == g.text.find(searchString):
                # somenthing is wrong
                ret = False
        except Exception as ex:
            ret = False
        return ret

    def delete(self, pagePath):
        ret = True
        try:
            url = '{}/{}'.format(self.url_delete, pagePath)
            p = self.session.get(url)
            searchString = '<meta http-equiv="refresh"'
            if -1 == p.text.find(searchString):
                # somenthing is wrong
                ret = False
        except Exception as ex:
            ret = False
        return ret

    def __init__(self, base_url, modulename):
        print('Test {}/{}'.format(base_url, modulename))
        self.session = requests.session()
        self.url_confirmcookie = '{}/confirmcookie'.format(base_url)
        self.url_login = '{}/auth/login'.format(base_url)
        self.url_create = '{}/{}/create'.format(base_url, modulename)
        self.url_edit = '{}/{}/edit'.format(base_url, modulename)
        self.url_deletever = '{}/{}/deletever'.format(base_url, modulename)
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
    t = WikiTests(base_url, modulename)
    t.confirmCookie()
    flag_login = t.login(user, password)
    assert flag_login == True, 'Not authenticated.'
    #
    # on postgresql I get fail on edit2
    #
    N = 3
    print('Authenticated. Run {} tests.'.format(N))
    for i in range(N):
        print('')
        pagePath = 'Page{}'.format(time.time())
        pageTitle = 'Test {}'.format(pagePath)
        pageBody = 'Test module {}\n__name__ = {}'.format(modulename, __name__)
        ok, pageid, versionid = t.create(pagePath, pageTitle, pageBody)
        assert ok == True, 'Error create.'
        print('Add pageid={} versionid={} ok'.format(pageid, versionid))
        newTitle = '{} v2'.format(pageTitle)
        newBody = '{}\nNew body'.format(pageBody)
        ok, versionid = t.edit(pagePath, newTitle, newBody, versionid)
        assert ok == True, 'Failed to edit'
        print('Edit1 pageid={} newversionid={} ok'.format(pageid, versionid))
        newTitle2 = '{} v3'.format(pageTitle)
        newBody2 = '{}\nNew body2'.format(newBody)
        ok, versionid = t.edit(pagePath, newTitle2, newBody2, versionid)
        assert ok == True, 'Failed to edit2'
        print('Edit2 pageid={} newversionid={} ok'.format(pageid, versionid))
        if DELETE_TESTS:
            # delete version before last version
            ok = t.deleteversion(pagePath, 1)
            assert ok == True, 'Failed to delete version 1'
            print('Del1 version pageid={} ok'.format(pageid))
            # delete last version
            ok = t.deleteversion(pagePath, 0)
            assert ok == True, 'Failed to delete version 0'
            print('Del2 version pageid={} ok'.format(pageid))
        if DELETE_TESTS:
            # delete wiki page with all versions
            ok = t.delete(pagePath)
            assert ok == True, 'Fail delete page'


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
