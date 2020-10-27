
#
# Auth module: users, groups and menu
#

"""

MIT License

Copyright (c) 2017 Ioan Coman

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

import os, datetime

from sqlalchemy import create_engine, Table, ForeignKey
from sqlalchemy import Column, Integer
from sqlalchemy import String, Unicode, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool

#from hashlib import md5 as HASHFUNC
from hashlib import sha1 as HASHFUNC3
from hashlib import sha256 as HASHFUNC2
from hashlib import sha512 as HASHFUNC


Base = declarative_base()
engine = None
inited = False

association_table = Table('users_groups_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('Users.id')),
    Column('group_id', Integer, ForeignKey('Groups.id'))
)

class Groups(Base):
    __tablename__ = 'Groups'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(64))
    description = Column(Unicode(512))
    #users is a list of sqlalchemy objects
    users = relationship("Users", secondary=association_table, back_populates="groups")
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(64))
    fullname = Column(Unicode(64))
    email = Column(Unicode(64))
    password = Column(String(256)) #hexdigest(salt)+hexdigest(password+hexdigest(salt))
    created = Column(DateTime, default=datetime.datetime.now)
    changed = Column(DateTime, default=datetime.datetime.now)
    token = Column(String(128)) #auth token qrcode
    home = Column(Unicode(64))
    #groups is a list of sqlalchemy objects
    groups = relationship("Groups", secondary=association_table, back_populates="users")
    def __init__(self, name, password, groups=[]):
        self.name = name
        self.fullname = u'User {}'.format(name)
        self.email = u''
        self.password = self._mkpass(password)
        self._gen_token()
        for i in groups:
            self.groups.append(i)
    def _validate(self, password):
        hashed_pass = HASHFUNC()
        #self.password is stored as hash
        #half of self.password is salt and the other half is hashed password
        #HALF = int(len(self.password)/2)
        HALF = len(hashed_pass.hexdigest())
        hashed_pass.update(password.encode('utf-8') + self.password[:HALF].encode('utf-8'))
        return self.password[HALF:] == hashed_pass.hexdigest()
    def _mkpass(self, password):
        salt = HASHFUNC()
        salt.update(os.urandom(300))
        hash = HASHFUNC()
        hash.update(password.encode('utf-8') + salt.hexdigest().encode('utf-8'))
        return salt.hexdigest() + hash.hexdigest()
    def _gen_token(self):
        token = HASHFUNC2()
        token.update(os.urandom(300))
        self.token = token.hexdigest()
        return self.token

def addUsers(session):
    '''
    built in groups:
        -1 = All authenticated users
        0 = Anonymous
    groups from db:
        1 = Administrators
        2 = Power users
    '''
    print ('Add groups')
    g1 = Groups(u'Administrators',u'Full admin rights'); session.add(g1)
    g2 = Groups(u'Power Users',u'Limited admin rights'); session.add(g2)
    session.add(Groups(u'Wiki admins',u'Create, edit and delete any wiki page'))
    session.add(Groups(u'Wiki users',u'Create, edit and delete own wiki pages'))
    print ('Add users')
    session.add(Users(u'admin',u'admin',[g1]))
    session.add(Users(u'guest',u'guest',[]))
    session.commit()


def getSession():
    return sessionmaker(bind=engine)()

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
    def __exit__(self,exc_type, exc_val, exc_tb):
        if self.session:
            self.session.commit()
            self.session.close()


def setupDB(DSN, init=False):
    global engine, inited
    if inited:
        #print('already inited')
        return
    inited = True
    #setupDB auh module
    #DSN = "sqlite+pysqlite:///file.db"
    #DSN = "postgres://user:password@server/Database"
    #DSN = "postgresql://user:password@server/Database"
    #DSN = "mssql://user:password@server/Database"
    #DSN = "mssql+pymssql://user:password@server/Database"
    global engine
    engine = create_engine(DSN)
    engine.echo = False
    if init:
        session = getSession()
        print ('Init SQL DB')
        print ('Drop all tables')
        Base.metadata.drop_all(engine)
        print ('Create all tables')
        Base.metadata.create_all(engine)
        addUsers(session)
        session.close()
    #end setupDB

if __name__ == "__main__":
    #run standalone, init SQL db, drop all tables and create all
    import os, sys
    py   = sys.version_info
    py3k = py >= (3, 0, 0)
    try:
        web_server_folder = os.path.join(os.getcwd(), '..','..')
        sys.path.insert(0,web_server_folder)
        from tools import load_config #import from web server folder
        config_file = os.path.join(os.getcwd(), 'config.json')
        config = load_config(config_file)
        DSN = config.get('DSN')
        #for sqlite chdir to server folder
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
        print (ex)
    finally:
        msg = 'Program ends, press Enter.'
        if py3k:
            input(msg)
        else:
            raw_input(msg)

