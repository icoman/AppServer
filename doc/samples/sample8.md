# Web App Server

## Access server config file

Create **``__``init``__``.py** :

```python
#
# An web server module
#

from appmodule import AppModule

app = AppModule()

def getApp():
    return app

@app.route("/")
@app.view("index.tpl")
def _():
    """
        Default view
    """
    title = "Index of {}".format(app.module_name)
    return dict(title = title, server_config = app.server_config)
```
Create **index.tpl** inside of **view** folder:

```html
% include("header.tpl")

<h1>{{title}}</h1>

<p>userid = {{userid}}</p>

<h1>User config</h1>
<ul>
%for k,v in user_config.items():
<li>{{k}} = {{v}}</li>
%end
</ul>

<h1>App config</h1>
<ul>
%for k,v in module_config.items():
<li>{{k}} = {{v}}</li>
%end
</ul>

<h1>Server config</h1>
<ul>
%for k,v in server_config.items():
<li>{{k}} = {{v}}</li>
%end
</ul>

% include("footer.tpl")
```

Create a JSON file named **config.json** in the module folder
(where is **``__``init``__``.py** located) using the 
[Application web config editor](https://github.com/icoman/PropertiesEditor_v1) and template for **Web Config Document**.

Also create a JSON file named **config_default_.json** in the module folder
using the [Application web config editor](https://github.com/icoman/PropertiesEditor_v1) and template for **User Config Document**.

If the server administrator did not enabled **user config** in module config
you will see an empty user config and the editor for user config will 
not be available.

Edit config of module as administrator and enable **user config**,
then edit config of user, made some changes and save it, then view module in browser.

By default the server provide to the template engine 
the **user config** and **application config** and for 
**server config** you need to pass it in python code:

```python
    return dict(title = title, server_config = app.server_config)
```

Warning: Exposing the **server config** in a template is a security risk 
because **server config** contains some secrets.

Applications modules do not need the **server config**, the only 
exception is in **auth** module, where the module need to know if 
**emergency admin** is enabled or not.


