# Web App Server

## Template and app config file

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
    title = "Application with a template and a config"
    return dict(title = title, json = json)

```

Create **index.tpl** inside of **view** folder:

```html
% include("header.tpl")

<h1>{{title}}</h1>

Application config:
<pre>

{{json.dumps(module_config, indent=4, sort_keys=True)}}

</pre>

% include("footer.tpl")
```

Create a JSON file named **config.json** in the module folder
(where is **``__``init``__``.py** located) using the 
[Application web config editor](https://github.com/icoman/PropertiesEditor_v1)
or copy & paste:

```json
{
  "data": {
    "10": {
      "description": "Data Source Name",
      "name": "DSN",
      "posturl": "",
      "type": "text",
      "value": "protocol://user:password@host/database"
    },
    "20": {
      "description": "Enable or disable module execution",
      "name": "module disabled",
      "posturl": "",
      "type": "checkbox",
      "value": ""
    },
    "30": {
      "description": "Show link to module config and user config",
      "name": "config menu",
      "posturl": "",
      "type": "checkbox",
      "value": "yes"
    }
  },
  "fields": {
    "10": [
      "name",
      []
    ],
    "20": [
      "description",
      []
    ],
    "30": [
      "type",
      [
        "text",
        "textarea",
        "password",
        "checkbox",
        "select",
        "mc"
      ]
    ],
    "40": [
      "value",
      []
    ],
    "50": [
      "posturl",
      [
        "",
        "/auth/groups/all",
        "/post1",
        "/post2",
        "/post3"
      ]
    ]
  }
}

```

The application config is passed to template 
(by **appmodule.py** method **render_template**)
as variable **module_config** and template
is show it in a ``<``pre``>`` html tag using function **json.dumps(module_config, indent=4, sort_keys=True)**.

The json config file contains **data** and **fields**, 
but the config of application consists only from **data**.

The info from **fields** is used by **admin web config editor**
to render the edit form.

You must be logged in with administrative rights to be able 
to edit configuration with **admin web config editor**.





