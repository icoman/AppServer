# Web App Server

## Setup Security in Application

To require authentication in an application you should use **@app.auth("permission name")**

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
    title = "Index of {}".format(app.module_name)
    return dict(title = title)

@app.route("/test1")
@app.auth("access module")
def _():
	"""
		Axccess to this resource
		is restricted
	"""
    return "This is test 1"
```

Create **index.tpl** inside of **view** folder:

```html
% include("header.tpl")

<h1>{{title}}</h1>
<a href="/{{module_name}}/test1">Test 1</a> - need authentication.

% include("footer.tpl")
```

Create a JSON file named **config.json** in the module folder
(where is **``__``init``__``.py** located) using the 
[Application web config editor](https://github.com/icoman/PropertiesEditor_v1) and template for **Web Config Document**.

Make sure you create a property (named **access module** in default config) 
of type **mc** (multiple checks) and **posturl** has 
value **/auth/groups/all**. 

The link **http:// your server /auth/groups/all** is available 
only with POST method.

The property of type **mc** will be populated with id of selected groups 
(hence posturl=**/auth/groups/all**) using [AJAX POST](https://api.jquery.com/jQuery.post/) by **web config editor**.

Use that property with the **auth** decorator in python code.

Exemple of **mc** properties: "access module", "admin module", "wiki publishers", ...

Test secured link (**/your_app/test1**) with a non admin account, 
because users from admin group (the group with id=1) will always have access.
The access of admins is granted in function **check_user_in_groups** in file **appmodule.py**.


