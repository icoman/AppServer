# Web App Server

## Customize web server

After you successfully run the server it is a good 
ideea to do some changes on **config.ini** and **menu.ini**.

The **config.ini** controls how the server starts (http, https or FCGI), 
default link for home (**home_url**), for login, logout, ...


For FCGI ([FastCGI](https://en.wikipedia.org/wiki/FastCGI)) 
I use [nginx](https://nginx.org/) with a config like:

```ini
server {
        listen          80 default_server;
        server_name     www.example.com;
        location / {
            # host and port to fastcgi server
            fastcgi_pass 127.0.0.1:8001;
            fastcgi_param REMOTE_ADDR $remote_addr;
            fastcgi_param SERVER_NAME $server_name;
            fastcgi_param SERVER_PORT $server_port;
            fastcgi_param SERVER_PROTOCOL $server_protocol;
            fastcgi_param PATH_INFO $fastcgi_script_name;
            fastcgi_param REQUEST_METHOD $request_method;
            fastcgi_param QUERY_STRING $query_string;
            fastcgi_param CONTENT_TYPE $content_type;
            fastcgi_param CONTENT_LENGTH $content_length;
            fastcgi_pass_header Authorization;
            fastcgi_intercept_errors off;
            }
}

```

For this **menu.ini** 

```ini
#
# link|title|icon|group list|description
#

/|Home|home|[-1,0]|Home page

|Demo|fire|[-1,0]|Demo apps
    /todo|Todo|tasks|[-1,0]|
    /wiki|Wiki|pencil|[-1,0]|
    /wiki/page1|Wiki page1|random|[-1,0]|
    /wiki/page2|Wiki page2|random|[-1,0]|
    /wiki/page100|Wiki page100|random|[-1,0]|
    /wiki/page101|Wiki page101|random|[-1,0]|
    /wiki/all|All Wiki pages|cog|[-1,0]|
    |loginlogout|user|[0,-1]|


|Admin|cog|[1,2]|Admin menu
    /adm|Adm|wrench|[1,2]|Admin modules
    /auth/users|Edit users|user|[1,2]|Admin edit users
    /auth/groups|Edit groups|th-large|[1,2]|Admin edit groups

# generic login/logout link with userfullname
|loginlogout|user|[-1,0]|

# login for anonymous
#/auth/login|Login|user|[0]|

# logout for any authenticated user
#/auth/logout|Logout|user|[-1]|

```

you should add a **todo** app, named **todo**, and a **wiki** app, named **wiki**.

The **menu.ini** points to /, /adm, /auth/users, /auth/groups, /todo, /wiki, /wiki/page1, /wiki/page2, ...

