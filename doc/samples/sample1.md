# Web App Server

## The smallest application

Create a folder inside **extensions** folder of 
webserver and in the created folder create a python file
name **``__``init``__``.py** with this content:

```python
#
# An web server module
#

from appmodule import AppModule

app = AppModule()

def getApp():
    return app

@app.route("/")
def _():
    """
        Default view
    """
    return "<html><h1>Index page</h1>"
```

The python function used as web method use a decorator: **app.route**.

Use admin page to view list of applications, reboot server and to access the link to your application.

Your application is available after server restart.
