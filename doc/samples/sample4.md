# Web App Server

## An Extended Application

Create **``__``init``__``.py** :

```python
#
# An web server module
#

import datetime
from appmodule import AppModule

class MyAppModule(AppModule):

    def init(self):
        """
            Initialisation code.
            Put here what you need to be executed
            when the application is created. 
        """
        self.datetimeformat = "%d-%b-%Y %H:%M:%S"
        print("Init module {}".format(self.module_name))


app = MyAppModule()

def getApp():
    return app


@app.route("/")
@app.view("index.tpl")
def _():
    """
        Default view
    """
    title = "Index of {}".format(app.module_name)
    now = datetime.datetime.now()
    return dict(title = title, now = now, datetimeformat = app.datetimeformat)
```

Create **index.tpl** inside of **view** folder:

```html
% include("header.tpl")

<h1>{{title}}</h1>
Now is {{now.strftime(datetimeformat)}}.

% include("footer.tpl")
```

The **datetime format** defined in **MyAppModule** 
as **self.datetimeformat** is passed to template as variable
**datetimeformat**.

