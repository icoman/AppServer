#
# Wiki module - modeldb
#

"""

MIT License

Copyright (c) 2017-2020 Ioan Coman

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

import datetime
from sqlalchemy import create_engine, Table, ForeignKey
from sqlalchemy import Column, Integer
from sqlalchemy import String, Unicode, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.pool import QueuePool

Base = declarative_base()
engine = None
inited = False


class WikiPages(Base):
    __tablename__ = 'WikiPages'
    id = Column(Integer, primary_key=True)
    path = Column(Unicode(128))
    userid = Column(Integer)  # pointer to table Users
    created = Column(DateTime, default=datetime.datetime.now)
    # field 'versions' defined here is a list dynamically created with objects from table WikiVersions, for relation one-to-many
    versions = relationship("WikiVersions", back_populates="parent")

    def __init__(self, path, userid):
        self.path = path
        self.userid = userid


class WikiVersions(Base):
    __tablename__ = 'WikiVersions'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128))
    userid = Column(Integer)  # pointer to table Users
    userfullname = Column(Unicode(64))
    body = Column(Unicode)
    created = Column(DateTime, default=datetime.datetime.now)
    # for relation one-to-many - it doesn't matter field name
    parent_id = Column(Integer, ForeignKey('WikiPages.id'))
    # parent -> a field dynamically created by backref
    parent = relationship("WikiPages", back_populates="versions")
    groups = Column(String(128))  # json list of ids of groups who can view page

    def __init__(self, title, body, userid, userfullname, groups):
        self.title = title
        self.body = body
        self.userid = userid
        self.userfullname = userfullname
        self.groups = groups


def getSession():
    return scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


class MyS(object):
    '''
        My session class
        ex:
        with MyS() as session:
            ...
            session.query(...)
            session.add(...)
            session.delete(...)
            ...
    '''

    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = getSession()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.commit()
            self.session.remove()


def addWikiPage(path, title, body, userid, username, groups):
    session = getSession()
    page = WikiPages(path, userid)
    ver = WikiVersions(title, body, userid, username, groups)
    page.versions.append(ver)
    session.add(page)
    session.add(ver)
    session.commit()
    session.close()


def populateWiki():
    addWikiPage(u'/FrontPage', u'Front Page', u'''
This demo wiki understands the [Python-Markdown language](https://pythonhosted.org/Markdown/)

and identify as wiki links any text between square brackets: [link] or [link|title of link].

# Text with H1
## Text with H2
### Text with H3

 * Rendered markdown links: [App Server Home](/) - [Todo](/todo) - [Wiki](/wiki) - [Python](http://www.python.org) - [Wiki History](http://wiki.c2.com/?WikiHistory)

 * Rendered wiki links test1:
[/|Wiki FrontPage] - [/page1|Page 1] - [/Page2|Page 2] - [/Page3|Page 3] - [/Page4|Page 4]

 * Rendered wiki links test2:
[/page1] - [/page2] - [/page3] - [/page4] - [/page5]

 * Rendered wiki links test3:
[page1] - [page2] - [page3] - [page4] - [page5]

 * Rendered wiki links test4:
[http://www.python.org] - [http://www.python.org|Python http link] - [https://www.python.org/] - [https://www.python.org/|Python https link]

Inexistent pages (or pages not created yet) has link with style text-decoration : line-through


''', 1, u'The Admin', '[-1,0]')


def setupDB(DSN, init=False):
    global engine, inited
    if inited:
        # print('already inited')
        return
    inited = True
    # DSN = "sqlite+pysqlite:///file.db"
    # DSN = "postgres://user:password@server/Database"
    # DSN = "postgresql://user:password@server/Database"
    # DSN = "mssql://user:password@server/Database"
    # DSN = "mssql+pymssql://user:password@server/Database"
    # engine = create_engine(DSN, poolclass=QueuePool, connect_args={'timeout': 30})
    engine = create_engine(DSN)
    engine.echo = False
    if init:
        # session = getSession()
        print('Init DB')
        print('Drop all tables')
        Base.metadata.drop_all(engine)
        print('Create all tables')
        Base.metadata.create_all(engine)
        populateWiki()
        # session.close()
    # end setupDB


if __name__ == "__main__":
    # run standalone, init SQL db, drop all tables and create all
    import os, sys

    py = sys.version_info
    py3k = py >= (3, 0, 0)
    try:
        web_server_folder = os.path.join(os.getcwd(), '..', '..')
        sys.path.insert(0, web_server_folder)
        from tools import load_config  # import from web server folder

        config_file = os.path.join(os.getcwd(), 'config.json')
        config = load_config(config_file)
        DSN = config.get('DSN')
        # for sqlite chdir to server folder
        # if sqlite database is stored in server folder
        os.chdir("../..")
        msg = "Init SQL DB (drop and create all tables)? [Y/N]"
        if py3k:
            ans = input(msg)
        else:
            ans = raw_input(msg)
        if ans.upper().startswith('Y'):
            setupDB(DSN, True)
        else:
            print("SQL Init aborted.\nNothing changed.")
    except Exception as ex:
        print(ex)
    finally:
        msg = 'Program ends, press Enter.'
        if py3k:
            input(msg)
        else:
            raw_input(msg)
