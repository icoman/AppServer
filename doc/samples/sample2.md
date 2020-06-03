# Web App Server

## Application with a template

Create a folder inside **extensions** folder of 
webserver and in the created folder create a python file
name **``__``init``__``.py** with this content:

```python
#
# An web server module
#

import datetime
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
    return dict(title = "Application with a template",
                now = datetime.datetime.now())

```

Then create a folder next to **``__``init``__``.py** and name it **view**.

In the **view** folder create **index.tpl** with this content:

```html
% include("header.tpl")

<h1>{{title}}</h1>
now = {{now}}

% include("footer.tpl")
```

The python function used as web method use two decorators: **app.route** and **app.view**.

Use admin page to view list of applications, reboot server and to access the link to your application.

Your application is available after server restart.