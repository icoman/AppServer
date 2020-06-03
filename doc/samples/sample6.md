# Web App Server

## A Brython button

The server use [Brython](http://www.brython.info/) and 
here is a sample of how to use it:

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
    return dict(title = title)
```

Create **index.tpl** inside of **view** folder:

```html
% include("header.tpl", usebrython=True)

<h1>{{title}}</h1>

<button type="button" id="button1" class="btn btn-primary btn-lg">
    <span class="glyphicon glyphicon-music"></span> Click me
</button>

<script type="text/python">

from browser import bind, alert
import time
import datetime

cnt = 1

@bind("#button1", "click")
def func_button1(evt):
    alert("Hello world!\n(Button 1)")
    global cnt
    #to see this look on javascript browser console
    print("cnt =",cnt)
    print("Time =", time.time())
    print("Now is", datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S"))
    cnt += 1

</script>

% include("footer.tpl")
```

The template include **header.tpl** with 
variable **usebrython** set to **True** and 
that means that the **header.tpl** must include 
the javascript files used by [Brython](http://www.brython.info/).
