# Web App Server

A modular [Python](https://www.python.org/) web application server  tested on both **python2** and **python3**.

On client side the server is using [Brython](https://www.brython.info/) and [Bootstrap 3](http://getbootstrap.com/).

Over 95% of copyright credits should go to Marcel Hellkamp, the creator of [bottlepy](https://bottlepy.org), 
also to the creators of [Beaker Cache and Session Library](https://beaker.readthedocs.io),
to the creators of [SQLAlchemy](http://www.sqlalchemy.org/)
and to the creators of [Brython](https://www.brython.info/).




## Install and Config

* [Install python and its dependencies](doc/install/install.md)
* [Activate emergency admin and start server](doc/install/emergencyadmin.md)
* [Configure server](doc/install/configure.md): config **auth** and **adm**
* [Customize web server](doc/install/customize.md): edit **config** and **menu**

## Code samples and recipes

* [Sample 1](doc/samples/sample1.md) - The smallest application, just one file: **``__``init``__``.py**
* [Sample 2](doc/samples/sample2.md) - Application with a template, two files: **``__``init``__``.py** and **index.tpl**
* [Sample 3](doc/samples/sample3.md) - Template and app config file.
* [Sample 4](doc/samples/sample4.md) - An Extended Application.
* [Sample 5](doc/samples/sample5.md) - Setup Security in Application.
* [Sample 6](doc/samples/sample6.md) - A [Brython](http://www.brython.info/) button.
* [Sample 7](doc/samples/sample7.md) - User config file.
* [Sample 8](doc/samples/sample8.md) - Access server config file.
* [Sample 9](doc/samples/sample9.md) - Hack the server.
* [golang approach](doc/samples/sample10.md) - Use golang to read module config



## Features or Intended Design Rules

 * The server is designed to be as simple as possible.
 
 * The server load and use modules from **extensions** folder.
 
 * The server itself don't use SQL, but load and call module **auth**, which use SQL.
 
 * The **auth** module provide login, logout and readonly access to 
groups for other modules. 
A tipical example: module **wiki** use in config **access module**, 
**admins access** and **publishers access** which get 
the group list from **auth** module.

 * The **adm** module allow admins to edit modules config, 
change description of modules and add modules to **extensions** 
folder from a list of templates.

 * The login process, if succeed, create a session cookie with 
user name, user id, user groups membership and so on. 
The group list stored in session cookie is used by other modules to check if user has access.

 * The server warn user that is using cookies, according to an 
[European Law from May 2011](https://www.cookielaw.org/about-this-message/), 
and ask for confirmation.

 * The server can be used with zero cookies, but user will not be able 
to authenticate and will have limited access.

 * The session cookie is encrypted with fixed keys (useful for cluster of servers) or 
randomly generated keys at server startup (if **random_session_keys** is enabled in server config).

 * The config of modules from **extensions** folder can be 
changed from server web interface or using an [external application](https://github.com/icoman/PropertiesEditor_v1).
 
 * You can import compiled modules with [nuitka](https://nuitka.net/): **nuitka --module mymodule.py**.

 * You can customize server menu changing **menu.ini**.

 * Server supports SSL and FCGI.

 * Server can run frozen (frozen Python mode).
