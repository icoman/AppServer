% include('header.tpl', usebrython=True)

<h1>{{title}}</h1>
%if not can_admin:
You can't create this page.
%else:
<input type="button" id="savebtn" value="Save" class="btn btn-success" />
<input type="button" id="cancelbtn" value="Cancel" class="btn btn-danger" />
<br><br>

<label for="wikititle">Page Title:</label>
<input type="text" id="wikititle" value="{{pagetitle}}" class="form-control"/>
<br>
<label>Select groups who can view page:</label>
<br>
<span id="spanallgroups"></span>
<br>
<br>
<label for="wikiedit">Page Body:</label>
<textarea id="wikiedit" rows="10" class="form-control">{{body}}</textarea>
%end

% include('ok_dlg.tpl')

<script type="text/python">

#for groups selection
#useCheckboxes = False #use SELECT
useCheckboxes = True

from browser import document as doc, bind, ajax, html, window
import json

saveurl = "/{{module_name}}/create{{wikipath}}"

#groups taken from auth module - accesibile to admins and power users
urlgetgroups = '/auth/groups/all'
groups = {} #id:group_name

def ajaxPOST(url, callback_func, data):
	doc['body'].classList.add("wait")
	req = ajax.ajax()
	req.bind('complete',callback_func)
	req.open('POST',url,True)
	req.set_header('content-type','application/x-www-form-urlencoded')
	req.send(data)

def on_complete_save(req):
	doc['body'].classList.remove("wait")
	if req.status==200 or req.status==0:
		try:
			D = json.loads(req.text)
			pageid, versionid = D['data']
			def _ok():
				window.location.href='/{{module_name}}{{wikipath}}'
			doc['btndlgok'].unbind()
			doc['btndlgok'].bind('click', _ok)
			window.ok_dlg('Page created!','Page id: {}, Version id: {}'.format(pageid, versionid))
		except Exception as ex:
			window.ok_dlg('Error', str(ex))
			return
	else:
		window.ok_dlg('Server Error', req.text)

def on_complete_getgroups(req):
	doc['body'].classList.remove("wait")
	global groups
	groups = {}
	if req.status==200 or req.status==0:
		try:
			D = json.loads(req.text)
			if D['ok']:
				groups = D['data']
			#add group Anonymous
			groups['0'] = ('Anonymous','Any unauthenticated user')
			groups['-1'] = ('All users','All authenticated users')
			showPageGroups()
		except Exception as ex:
			print(ex)

@bind(doc['cancelbtn'], 'click')
def cancel_func(evt):
	window.location.href='/{{module_name}}'

@bind(doc['savebtn'], 'click')
def save_func(evt):
	values = []
	if not useCheckboxes:
		#SELECT
		sel = doc['spanallgroups'].get(selector="SELECT")[0]
		values = [int(option.value) for option in sel if option.selected]
	else:
		#CHECKBOX
		sel = doc['spanallgroups'].get(selector='input[type="checkbox"]')
		values = [int(ckbt.value) for ckbt in sel if ckbt.checked]
	ajaxPOST(saveurl, on_complete_save, 
		{'body':doc['wikiedit'].value,
		'pagetitle':doc['wikititle'].value,
		'groups':json.dumps(values)
		})

def getGroups():
	ajaxPOST(urlgetgroups, on_complete_getgroups, {})

def on_checkbox_change(evt):
	ob = doc[evt.target.idlabel]
	if evt.target.checked:
		ob.style={'color':'#FF0000'}
	else:
		ob.style={'color':'#000000'}

def showPageGroups():
	global groups
	cntck = 1000
	pagegroups = []
	#dialog to select groups
	if not useCheckboxes:
		#SELECT
		control = html.SELECT(size=5, multiple=True)
		for idgr in sorted(groups.keys()):
			item = groups.get(idgr)[0]
			isSelected = int(idgr) in pagegroups
			title = groups.get(idgr)[1]
			control <= html.OPTION(item, value=idgr, selected=isSelected, title=title)
	else:
		#CHECKBOX
		control = None
		for idgr in sorted(groups.keys()):
			item = groups.get(idgr)[0]
			isSelected = int(idgr) in pagegroups
			if isSelected:
				style={'color':'#FF0000'}
			else:
				style={'color':'#000000'}
			title = groups.get(idgr)[1]
			#unique name for label checkbox for each module and config key 
			idlabel = 'lck_{}'.format(cntck)
			cntck += 1
			chbox = html.INPUT(Type="checkbox", value=idgr, checked=isSelected, title=title)
			chbox.bind('click', on_checkbox_change)
			chbox.idlabel = idlabel
			lab = html.LABEL(item+" ", value=item, title=title, id=idlabel, style=style)
			if control is None:
				control = html.SPAN()
			else:
				control <= ', '
			#control <= chbox
			lab <= chbox
			control <= lab
	if control is not None:
		spanallgroups = doc['spanallgroups']
		spanallgroups.clear()
		spanallgroups <= control


getGroups()

</script>

% include('footer.tpl')
