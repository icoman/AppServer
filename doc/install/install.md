# Web App Server

## Install python and its dependencies

To start this server on [Linux](https://www.linux.org/), first install python packages.

For [Microsoft Windows](https://www.microsoft.com/en-us/windows) and any other OS, try your luck after you succeed on [Linux](https://www.linux.org/).

The installation tests were performed on [Ubuntu server](https://www.ubuntu.com/server) under [VirtualBox](https://www.virtualbox.org/) using SQL database host 10.0.2.2 (IP of computer host running VirtualBox).

**On Debian Linux for python2:**

```bash
apt install build-essential
apt install python-pip
apt install python2.7-dev
pip2 install --upgrade pip
pip2 install bottle
pip2 install sqlalchemy
pip2 install markdown
pip2 install pillow
pip2 install qrcode
#for encrypted cookies install pycryptodome or pycrypto
pip2 install pycryptodome
pip2 install pycrypto
pip2 install beaker
#for iot module
pip2 install redis
#install at least one webserver:
pip2 install tornado
pip2 install paste
pip2 install waitress
pip2 install cherrypy
#for postgresql
pip2 install psycopg2
#for ms sql
apt install freetds-dev
pip install pymssql
```

**On Debian Linux for python3:**

```bash
apt install build-essential
apt install python3-pip
apt install python3-dev
pip3 install --upgrade pip
pip3 install bottle
pip3 install sqlalchemy
pip3 install markdown
pip3 install pillow
pip3 install qrcode
#for encrypted cookies install pycryptodome or pycrypto
pip3 install pycryptodome
pip3 install pycrypto
pip3 install beaker
#for iot module
pip3 install redis
#install at least one webserver:
pip3 install tornado
pip3 install paste
pip3 install waitress
pip3 install cherrypy
#for postgresql
pip3 install psycopg2
#for ms sql
apt install freetds-dev
pip3 install pymssql
```


**On Debian Linux for pypy:**

```bash
apt install build-essential
apt install pypy
apt install pypy-dev
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
pypy get-pip.py
pypy -m pip install --upgrade pip
pypy -m pip install bottle
pypy -m pip install sqlalchemy
pypy -m pip install markdown
pypy -m pip install cython
pypy -m pip install pycrypto
pypy -m pip install beaker
pypy -m pip install qrcode
#for iot module
pypy -m pip install redis
#install at least one webserver:
pypy -m pip install tornado
pypy -m pip install paste
pypy -m pip install waitress
pypy -m pip install cherrypy
#for postgresql
apt install postgresql-server-dev-all
pip3 install psycopg2
#for ms sql
apt install freetds-dev
pypy -m pip install pymssql
```
