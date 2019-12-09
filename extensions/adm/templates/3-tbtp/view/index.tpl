% include('header.tpl', usebrython=True)

<h1>{{title}}</h1>


% include('ok_cancel.tpl', id='dlg1', title='Test dialog1', body='Dialog 1', idok='d1Ok', idcancel='d1Cancel')
% include('ok_cancel.tpl', id='dlg2', title='Test dialog2', body='Dialog 2', idok='d2Ok', idcancel='d2Cancel')

<button type="button" class="btn btn-success btn-lg" 
	onclick="$('#dlg1').modal('show');"><span class="glyphicon glyphicon-plus"></span> Dialog 1</button>

<button type="button" class="btn btn-success btn-lg" 
	onclick="$('#dlg2').modal('show');"><span class="glyphicon glyphicon-plus"></span> Dialog 2</button>


<script type="text/python">

from browser import document, bind, alert

@bind(document['d1Ok'], 'click')
def dialog1_ok(evt):
	alert('Dialog1 Ok')

@bind(document['d1Cancel'], 'click')
def dialog1_cancel(evt):
	alert('Dialog1 Cancel')

@bind(document['d2Ok'], 'click')
def dialog1_ok(evt):
	alert('Hello World!')

</script>


% include('footer.tpl')
