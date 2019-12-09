# Web App Server

## Configure server

After you login as **Emergency Admin**, the admin 
interface should be available:

![admin module](adminmodule.jpg)

You have only two modules installed in server: **adm** and **auth**.

## Config "auth" module

You can add more applications later, but first 
configure **auth** module using the red button of module.

Set **DSN = mssql+pymssql://webuser:userweb@10.0.2.2/Database** 
or any other valid **DSN** understood by [SQL Alchemy](https://www.sqlalchemy.org/).

Server **10.0.2.2** is IP of host in VirtualBox.

**admin notes** does nothing but inform admin about status of module.

![config auth module](configauth1.jpg)

Then create all SQL tables for **auth** module running once **modeldb.py** 
from **web server folder/extensions/auth/** and restart webserver.

After server restart, the groups should apear in config dialog:

![config auth module](configauth2.jpg)

Set acces to **read/write groups** and **read/write users** only to **Administrators**.

## Config "adm" module

Now configure **adm** module using the red button of module:

![config adm module](configadm.jpg)

To **adm** module all users should have access to be able to edit its own user config.

But to admin module **adm** anly **Administrators** should have the rights.

**admin notes** does nothing but inform admin about status of module.
