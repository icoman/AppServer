#
# Todo module - modeldb
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
from sqlalchemy import create_engine, Column, Integer, Sequence
from sqlalchemy import String, Unicode, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

Base = declarative_base()
engine = None
inited = False


class Todo(Base):
    __tablename__ = 'Todo'
    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    userfullname = Column(Unicode(64), default=u'Anonymous')
    dataora = Column(DateTime, default=datetime.datetime.now)
    title = Column(Unicode(64), default=u'-?-')
    description = Column(Unicode(1024), default=u'')
    done = Column(Boolean, default=False)


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
