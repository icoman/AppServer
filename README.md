# Web App Server

A modular [Python](https://www.python.org/) web application server  tested on both **python2** and **python3**.

On client side the server is using [Brython](https://www.brython.info/) and [Bootstrap 3](http://getbootstrap.com/).

Over 95% of copyright credits should go to Marcel Hellkamp, the creator of [bottlepy](https://bottlepy.org), 
also to the creators of [Beaker Cache and Session Library](https://beaker.readthedocs.io),
to the creators of [SQLAlchemy](http://www.sqlalchemy.org/)
and to the creators of [Brython](https://www.brython.info/).




## Install and Config

* [Install python and its dependencies](doc/install/install.md)
* [Activate emergency admin and start server](doc/install/emergencyadmin.md)
* [Configure server](doc/install/configure.md): config **auth** and **adm**
* [Customize web server](doc/install/customize.md): edit **config** and **menu**

## Code samples and recipes

* [Sample 1](doc/samples/sample1.md) - The smallest application, just one file: **``__``init``__``.py**
* [Sample 2](doc/samples/sample2.md) - Application with a template, two files: **``__``init``__``.py** and **index.tpl**
* [Sample 3](doc/samples/sample3.md) - Template and app config file.
* [Sample 4](doc/samples/sample4.md) - An Extended Application.
* [Sample 5](doc/samples/sample5.md) - Setup Security in Application.
* [Sample 6](doc/samples/sample6.md) - A [Brython](http://www.brython.info/) button.
* [Sample 7](doc/samples/sample7.md) - User config file.
* [Sample 8](doc/samples/sample8.md) - Access server config file.
* [Sample 9](doc/samples/sample9.md) - Hack the server.
* [golang approach](doc/samples/sample10.md) - Use golang to read module config



## Features or Intended Design Rules

 * The server is designed to be as simple as possible.
 
 * The server load and use modules from **extensions** folder.
 
 * The server itself don't use SQL, but load and call module **auth**, which use SQL.
 
 * The **auth** module provide login, logout and readonly access to 
groups for other modules. 
A tipical example: module **wiki** use in config **access module**, 
**admins access** and **publishers access** which get 
the group list from **auth** module.

 * The **adm** module allow admins to edit modules config, 
change description of modules and add modules to **extensions** 
folder from a list of templates.

 * The login process, if succeed, create a session cookie with 
user name, user id, user groups membership and so on. 
The group list stored in session cookie is used by other modules to check if user has access.

 * The server warn user that is using cookies, according to an 
[European Law from May 2011](https://www.cookielaw.org/about-this-message/), 
and ask for confirmation.

 * The server can be used with zero cookies, but user will not be able 
to authenticate and will have limited access.

 * The session cookie is encrypted with fixed keys (useful for cluster of servers) or 
randomly generated keys at server startup (if **random_session_keys** is enabled in server config).

 * The config of modules from **extensions** folder can be 
changed from server web interface or using an [external application](https://github.com/icoman/PropertiesEditor_v1).
 
 * You can import compiled modules with [nuitka](https://nuitka.net/): **nuitka --module mymodule.py**.

 * You can customize server menu changing **menu.ini**.

 * Server supports SSL and FCGI.

 * Server can run frozen (frozen Python mode).

## May 19, 2026 update: a sample of Python beauty, simplicity and power

In 2026, after 7 years since I created this project, I still use it for two business partners.

Here is another code snippet:

### The server side python code

```python

from .modeldb import ArhivaCRQS

@app.route('/crqs')
@app.auth('access module')
@app.view('crqs.tpl')
def _():
    title = 'CRQS Archive'
    source_data_map = {
        100: ('id', ''),
        110: ('created', 'Data ora'),
        120: ('operator', 'Op mon'),
        130: ('operator_crqs', 'Op Q'),
        140: ('order', 'Ordin de productie'),
        150: ('box_number', 'box_number'),
        160: ('ean_cu', 'EAN CU'),
        170: ('mrdr_du', 'MRDR DU'),
        180: ('mix_batch_sscc', 'mix_batch_sscc'),
        190: ('lot', 'LOT'),
        200: ('palet_number', 'palet_number'),
        210: ('mixer_number', 'mixer_number'),
        220: ('category', 'category'),
    }
    body = []

    with MyS(1) as session:
        for rec in session.query(ArhivaCRQS).all():
            d = []
            for key in sorted(source_data_map.keys()):
                sql_field = source_data_map[key][0]
                value = getattr(rec, sql_field)
                if isinstance(value, datetime.datetime):
                    value = value.strftime(app.datetimeformat2)
                d.append(value)
            body.append(d)
    head = [source_data_map[x][1] for x in sorted(source_data_map.keys())]

    return dict( title = title, head = head, body = body )


```

### The client side (file **crqs.tpl** as bottle template)

```html
% include('header.tpl', local_js=[], local_css=['app.css', '/com/static/animations.css'])

<table class="table table-striped table-hover table-condensed">
  <thead>
    <tr>
    %for x in head:
    %if x:
       <th>{{x}}</th>
    %end
    %end
    </tr>
  </thead>
  <tbody>
    %for x in body:
    <tr>
        %for index, rec in enumerate(x):
        %if head[index]:
            <td>{{rec}}</td>
        %end
        %end
    </tr>
    %end
  </tbody>
</table>

% include('footer.tpl')
```


### Another and better server side python code

```python
@app.route('/crqs')
@app.auth('access module')
@app.view('crqs.tpl')
def _():

    bs = app.get_beaker_session()
    userid = int(bs.get('userid', 0))
    userfullname = bs.get('userfullname', 'Anonymous')

    now = datetime.datetime.now()
    title = 'Arhiva CRQS'
    nume_operator = userfullname
    filtru_lot = bottle.request.query.lot or ''
    filtru_mrdr = bottle.request.query.mrdr or ''

    source_data = [
        # ('sql_field', 'Header title'),
        ('id', ''), # hidden
        ('', ''), # color of table row
        ('rec_type', ''),  # hidden
        ('created', 'Data creare'),
        ('updated', 'Data actualizare'),
        # ('manufactured', 'Data productie'),
        ('operator', 'Operator mon'),
        ('order', 'Ordin'),
        ('operator_crqs', 'Operator CRQS'),
        ('lot', 'LOT'),
        ('ean_cu', 'EAN CU'),
        ('mrdr_du', 'MRDR DU'),
        ('box_number', 'Nr cutie'),
        ('mix_batch_sscc', 'Nr mixare'),
        ('palet_number', 'Nr palet'),
        ('mixer_number', 'Mixer'),
        ('category', 'Categorie'),
        ('', 'Denumire produs')
    ]

    # table head data passed to bottle template
    head = [description for _, description in source_data]

    # table body data passed to bottle template
    body = []
    with MyS(3) as session:
        d_produse = {x.MrdrDU:x.DenumireLada or x.DenumirePalet for x in session.query(ProduseFD).all()}
    with MyS(1) as session:
        q = session.query(ArhivaCRQS)
        if filtru_lot:
            q = q.filter(ArhivaCRQS.lot.ilike(f'%{filtru_lot}%'))
        if filtru_mrdr:
            q = q.filter(ArhivaCRQS.mrdr_du.ilike(f'%{filtru_mrdr}%'))
        for rec in q.all():
            d = []
            for sql_field, description in source_data:
                if sql_field:
                    value = getattr(rec, sql_field)
                    if isinstance(value, datetime.datetime):
                        value = value.strftime(app.datetimeformat2)
                else:
                    if description:
                        # insert denumire produs
                        value = d_produse.get(rec.mrdr_du)
                    else:
                        # compute color of table row
                        valid = False
                        if rec.rec_type == 1:
                            # Ambalare
                            if rec.box_number and rec.palet_number:
                                valid = True
                        if rec.rec_type == 2:
                            # Mixare
                            if rec.box_number and rec.mix_batch_sscc and rec.mixer_number and rec.palet_number and rec.category:
                                valid = True
                        if valid:
                            # find how old is the record
                            vechime_in_minute = (now - rec.updated).total_seconds() / 60.0
                            if vechime_in_minute > LIMIT_CRQS_REMOVE_MINUTES:
                                value = 'success'
                            else:
                                value = 'default'
                        else:
                            value = 'danger'
                d.append(value)
            body.append(d)

    return dict(title = title, 
        head = head, body = body,
        nume_operator = nume_operator,
        filtru_lot = filtru_lot, 
        filtru_mrdr = filtru_mrdr
        )

```
