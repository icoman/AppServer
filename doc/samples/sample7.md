# Web App Server

## User config file

Create **``__``init``__``.py** :

```python
#
# An web server module
#

import json
from appmodule import AppModule

app = AppModule()

def update_app(module_name, server_config):
    app.update(module_name, server_config)

@app.route("/")
@app.view("index.tpl")
def _():
    """
        Default view
    """
    title = "Index of {}".format(app.module_name)
    return dict(title = title, json = json)

```

Create **index.tpl** inside of **view** folder:

```html
% include("header.tpl")

<h1>{{title}}</h1>

<p>userid = {{userid}}</p>
<p>module name = {{module_name}}</p>

<p>module config</p>
<pre>
{{json.dumps(module_config, indent=4, sort_keys=True)}} 
</pre>

<p>user config</p>
<pre>
{{json.dumps(user_config, indent=4, sort_keys=True)}} 
</pre>

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

When you open the user config editor, if there is no user config file, 
the template file **config_default_.json** will be copied as user config file.

You must be logged in to be able to edit user config file.

Because there is no security set on this sample application, anonymous 
users will be able to view index page, but user config will be empty and 
userid  will be 0 (zero).



