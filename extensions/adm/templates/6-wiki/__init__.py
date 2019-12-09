#
# Wiki module
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

import bottle
import os, stat
import traceback
import json, datetime, time
import re, markdown

from appmodule import AppModule
from tools import html_redirect
from .modeldb import setupDB, WikiPages, WikiVersions, MyS


class MyAppModule(AppModule):

    def init(self):
        self.datetimeformat = "%d-%b-%Y %H:%M"
        self.module_config['ANY'] = [-1, 0]  # All users and Anonymous
        self.module_config['ADMIN'] = [1]  # Admin group
        DSN = self.module_config.get('DSN')
        try:
            setupDB(DSN)
        except:
            # ignore error here
            pass

    def _renderPage(self, pageVersion):
        extensions = ['markdown.extensions.codehilite', 'markdown.extensions.extra']
        body = markdown.markdown(pageVersion.body)
        # [Front Page|This is front page]
        body = re.sub(r"\[([^]]+)\|([^]]+)\]", self._link_repl2, body)
        # [Front Page]
        body = re.sub(r"\[([^]]+)\]", self._link_repl1, body)
        return body

    def _link_repl1(self, match):
        """ for [Wiki Page]  """
        link = match.group(1)
        return self._mk_link(link, None)

    def _link_repl2(self, match):
        """ for [Wiki Page|wiki page title] """
        link = match.group(1)
        title = match.group(2)
        return self._mk_link(link, title)

    def _mk_link(self, link, title):
        """Return HTML code for given link,title"""
        if link.startswith('http://') or link.startswith('https://') or link.startswith('mailto:'):
            if not title:
                title = link
            ret = u'<a href="{}">{}</a>'.format(link, title)
        else:
            if not link.startswith(u'/'):
                link = u'/' + link
            if link == u'/':
                pageExists = True
            else:
                with MyS() as session:
                    page = session.query(WikiPages).filter(WikiPages.path == link).first()
                    if page:
                        last_version = session.query(WikiVersions).filter(WikiVersions.parent_id == page.id) \
                            .order_by(WikiVersions.created.desc()).all()[0]
                        if not title:
                            title = last_version.title
                    if not title:
                        title = link
                    pageExists = page is not None
            if pageExists:
                ret = u'<a href="/{}{}">{}</a>'.format(self.module_name, link, title)
            else:
                if not title:
                    title = link
                # class nf = class not found
                ret = u'<a class="nf" href="/{}/create{}">{}</a>'.format(self.module_name, link, title)
        return ret


app = MyAppModule()


def update_app(module_name, server_config):
    app.update(module_name, server_config)


@app.get('/static/<path:path>')
@app.auth('ANY')
def _(path):
    return bottle.static_file(path, root=app.module_static_folder)


@app.get('/')
@app.auth('ANY')
def _():
    return view_page(u'FrontPage')


@app.get('/all')
@app.auth('ANY')
@app.view('allpages.tpl')
def _():
    title = "All Wiki Pages"
    bs = app.get_beaker_session()
    userid = bs.get('userid') or 0
    with MyS() as session:
        all_pages = []
        for page in session.query(WikiPages).order_by(WikiPages.path).all():
            all_vers = page.versions
            last_ver_id = max([x.id for x in all_vers])
            last_ver = session.query(WikiVersions).filter(WikiVersions.id == last_ver_id).first()
            is_owner = (last_ver.userid == userid) or (page.userid == userid)
            is_wiki_admin = app.check_user_in_groups(app.module_config.get('admins access')) or is_owner
            can_view = app.check_user_in_groups(json.loads(last_ver.groups)) or is_wiki_admin
            l = (last_ver.userfullname, page.path, last_ver.title,
                 page.created.strftime(app.datetimeformat),
                 last_ver.created.strftime(app.datetimeformat),
                 len(page.versions), can_view)
            all_pages.append(l)
    return dict(title=title, all_pages=all_pages)


@app.route('/edit/<wikipath:path>', method=['get', 'post'])
@app.auth('ANY')
@app.view('edit.tpl')
def _(wikipath):
    if not wikipath.startswith('/'):
        wikipath = '/' + wikipath
    wikipath = u''+wikipath
    version_index = int(bottle.request.query.get('v', 0))
    if bottle.request.forms.get('version_index'):
        version_index = int(bottle.request.forms.get('version_index', 0))
    if version_index:
        title = 'Edit variant #{}'.format(version_index)
    else:
        title = 'Edit last version'
    bs = app.get_beaker_session()
    userfullname = bs.get('userfullname') or 'Anonymous'
    userid = bs.get('userid') or 0
    savedbody = bottle.request.forms.body
    pagetitle = bottle.request.forms.pagetitle
    edited_version_id = int(bottle.request.forms.get('edited_version_id', 0))
    groups = bottle.request.forms.get('groups', '[]')
    with MyS() as session:
        page = session.query(WikiPages).filter(WikiPages.path == wikipath).first()
        if page:
            # load page for editing
            L = session.query(WikiVersions).filter(WikiVersions.parent_id == page.id) \
                .order_by(WikiVersions.created.desc())
            version = L[version_index]
            version_id = version.id
            is_wiki_admin = app.check_user_in_groups(app.module_config.get('admins access'))
            is_owner = (userid == version.userid) or (userid == page.userid)
            can_admin = is_wiki_admin or is_owner
            if savedbody:
                # save page
                if can_admin:
                    if edited_version_id == version_id:
                        newPageVersion = WikiVersions(pagetitle, savedbody, userid, userfullname, groups)
                        page.versions.append(newPageVersion)
                        session.add(newPageVersion)
                        session.commit()
                        edited_version_id = newPageVersion.id
                        # confirm dialog for edit page
                        return json.dumps(dict(
                            ok=True, data=edited_version_id))
                    else:
                        return json.dumps(dict(
                            ok=False,
                            data="Page not saved!\nInvalid version id."))
                else:
                    # return error message
                    return json.dumps(dict(
                        ok=False,
                        data="You no longer can change this page."))
            else:
                # load page
                if can_admin:
                    body = version.body
                    pagetitle = version.title
                    groups = version.groups
                else:
                    return app.err_msg(wikipath, "You can't edit this page.")
            return dict(
                title=title, groups=groups,
                wikipath=wikipath, can_admin=can_admin,
                body=body, version_index=version_index,
                version_id=version_id, pagetitle=pagetitle
            )
        else:
            return app.err_msg(wikipath, "No page to edit.`")


@app.get('/deletever/<wikipath:path>')
@app.auth('ANY')
def _(wikipath):
    if not wikipath.startswith('/'):
        wikipath = '/' + wikipath
    wikipath = u''+wikipath
    version_index = int(bottle.request.query.get('v', 0))
    bs = app.get_beaker_session()
    userid = bs.get('userid') or 0
    with MyS() as session:
        page = session.query(WikiPages).filter(WikiPages.path == wikipath).first()
        if page:
            page_versions = session.query(WikiVersions).filter(WikiVersions.parent_id == page.id) \
                .order_by(WikiVersions.created.desc()).all()
        else:
            page_versions = []
        if page:
            version = page_versions[version_index]
            is_wiki_admin = app.check_user_in_groups(app.module_config.get('admins access'))
            is_owner = (userid == version.userid) or (userid == page.userid)
            can_admin = is_wiki_admin or is_owner
            if can_admin:
                session.delete(version)
            else:
                return app.err_msg(wikipath, "You can't delete this page version.")
    url = '/{}{}'.format(app.module_name, wikipath)
    return html_redirect(url)


@app.get('/delete/<wikipath:path>')
@app.auth('ANY')
def _(wikipath):
    if not wikipath.startswith('/'):
        wikipath = '/' + wikipath
    wikipath = u''+wikipath
    bs = app.get_beaker_session()
    userid = bs.get('userid') or 0
    is_wiki_admin = app.check_user_in_groups(app.module_config.get('admins access'))
    with MyS() as session:
        page = session.query(WikiPages).filter(WikiPages.path == wikipath).first()
        if page:
            is_owner = (userid == page.userid)
            can_admin = is_wiki_admin or is_owner
            if can_admin:
                for ver in page.versions:
                    session.delete(ver)
                session.delete(page)
            else:
                return app.err_msg(wikipath, "You can't delete this page.")
    url = '/{}'.format(app.module_name)
    return html_redirect(url)


@app.route('/create/<wikipath:path>', method=['get', 'post'])
@app.auth('ANY')
@app.view('create.tpl')
def _(wikipath):
    if not wikipath.startswith('/'):
        wikipath = '/' + wikipath
    wikipath = u''+wikipath
    title = 'Create wiki page'
    bs = app.get_beaker_session()
    userfullname = bs.get('userfullname') or 'Anonymous'
    userid = bs.get('userid') or 0
    is_wiki_admin = app.check_user_in_groups(app.module_config.get('admins access'))
    is_wiki_publisher = app.check_user_in_groups(app.module_config.get('publishers access'))
    can_admin = is_wiki_admin or is_wiki_publisher
    if not can_admin:
        return app.err_msg(wikipath, "You can't create this page. You must be wiki publisher or admin.")
    pagetitle = bottle.request.forms.pagetitle
    savedbody = bottle.request.forms.body
    groups = bottle.request.forms.get('groups', '[]')
    body = u'[/|Wiki Home] - [page|title new page]'
    with MyS() as session:
        page = session.query(WikiPages).filter(WikiPages.path == wikipath).first()
        if page:
            return json.dumps(dict(ok=False, data='Page already exists.'))
        if savedbody:
            page = WikiPages(wikipath, userid)
            newPageVersion = WikiVersions(pagetitle, savedbody, userid, userfullname, groups)
            page.versions.append(newPageVersion)
            session.add(newPageVersion)
            session.commit()
            pageid = page.id
            versionid = newPageVersion.id
            return json.dumps(dict(ok=True, data=[pageid, versionid]))
    return dict(
        title=title, wikipath=wikipath,
        can_admin=can_admin, body=body,
        pagetitle=pagetitle
    )


@app.post('/upld')
@app.auth('ANY')
def _():
    bs = app.get_beaker_session()
    userid = bs.get('userid') or 0
    wikipath = bottle.request.forms.wikipath
    if wikipath:
        with MyS() as session:
            page = session.query(WikiPages).filter(WikiPages.path == wikipath).first()
            is_wiki_admin = app.check_user_in_groups(app.module_config.get('admins access'))
            if page:
                page_id = page.id
                is_owner = (userid == page.userid)
                can_admin = is_wiki_admin or is_owner
                if can_admin:
                    upload = bottle.request.files.get('upload')
                    if upload:
                        # name, ext = os.path.splitext(upload.filename)
                        upload_folder = app.module_config.get('upload folder', 'upload')
                        upload_path = os.path.join(app.module_folder, upload_folder)
                        save_path = os.path.join(app.module_folder, upload_folder, str(page_id))
                        try:
                            os.mkdir(upload_path)
                        except:
                            pass
                        try:
                            os.mkdir(save_path)
                        except:
                            pass
                        upload.save(save_path)  # appends upload.filename automatically
            return html_redirect('/{}{}'.format(app.module_name, wikipath))
    return '??'


@app.get('/get/<page_id:int>/<att_ix:int>')
@app.auth('ANY')
def _(page_id, att_ix):
    # get uploaded file
    bs = app.get_beaker_session()
    userid = bs.get('userid') or 0
    # page_id = int(pathlist[2])
    # att_ix = int(pathlist[3])
    if page_id:
        with MyS() as session:
            page = session.query(WikiPages).filter(WikiPages.id == page_id).first()
            ids = [x.id for x in page.versions]
            ids.sort()
            version_index = -1
            version = session.query(WikiVersions).filter(WikiVersions.id == ids[version_index]).first()
            groups = json.loads(version.groups)
            is_admin = app.check_user_in_groups(app.module_config.get('admins access'))
            is_owner = (userid == version.userid)
            if is_owner or is_admin or app.check_user_in_groups(groups):
                upload_folder = app.module_config.get('upload folder', 'upload')
                save_path = os.path.join(app.module_folder, upload_folder, str(page_id))
                try:
                    attachments = os.listdir(save_path)
                    attachments.sort()
                    filename = attachments[att_ix]
                    return bottle.static_file(filename, root=save_path)
                except:
                    return 'no file'
            else:
                return app.err_msg(page.path, "You can't acces this page.")
    return "???"


# this must be declared last
@app.get('/<wikipath:path>')
@app.auth('ANY')
@app.view('view.tpl')
def view_page(wikipath):
    if not wikipath.startswith('/'):
        wikipath = '/' + wikipath
    wikipath = u'' + wikipath
    version_index = int(bottle.request.query.get('v', 0))
    bs = app.get_beaker_session()
    userid = bs.get('userid') or 0
    with MyS() as session:
        page = session.query(WikiPages).filter(WikiPages.path == wikipath).first()
        if page:
            page_versions = session.query(WikiVersions).filter(WikiVersions.parent_id == page.id) \
                .order_by(WikiVersions.created.desc()).all()
        else:
            page_versions = []
        if page:
            page_id = page.id
            if len(page_versions) <= version_index:
                return app.err_msg(wikipath, "No such page version")
            version = page_versions[version_index]
            all_page_versions = [(x.userid, x.userfullname, x.groups, x.title, x.created) for x in page_versions]
            is_owner = (version.userid == userid) or (page.userid == userid)
            is_wiki_admin = app.check_user_in_groups(app.module_config.get('admins access')) or is_owner
            def has_access(groups):
                return app.check_user_in_groups(json.loads(groups))
            can_view = has_access(version.groups)
            if not (can_view or is_wiki_admin):
                return app.err_msg(wikipath, "You can't view this page")
            title = version.title
            body = app._renderPage(version)
            # uploaded files
            upload_folder = app.module_config.get('upload folder', 'upload')
            save_path = os.path.join(app.module_folder, upload_folder, str(page_id))
            attachments = []
            try:
                filelist = os.listdir(save_path)
                filelist.sort()
                for filename in filelist:
                    fullname = os.path.join(save_path, filename)
                    st = os.stat(fullname)
                    size = st[stat.ST_SIZE] / 1024.0 / 1024.0
                    tm = datetime.datetime.fromtimestamp(st[stat.ST_MTIME]).strftime(app.datetimeformat)
                    file_label = '{}'.format(filename)
                    file_title = '{}'.format(tm)
                    file_size = '{:.2f}Mb'.format(size)
                    attachments.append((file_label, file_title, file_size))
            except Exception as ex:
                # print ex
                pass
            page_versions = []
            return dict(
                title=title, wikipath=wikipath,
                datetimeformat=app.datetimeformat,
                all_page_versions=all_page_versions,
                has_access=has_access,
                page_id=page_id,
                is_wiki_admin=is_wiki_admin, attachments=attachments,
                body=body, version_index=version_index
            )
        else:
            title = 'Wiki page not found'
            d = dict(title=title, wikipath=wikipath)
            return app.render_template('nopage.tpl', d)
