% include('header.tpl', usebrython=True)

<!-- Test Bootstrap with Templates -->

<h1>{{title}}</h1>


<!-- include dialogs from "server_templates" folder -->
% include('ok_dlg.tpl')
% include('confirm_dlg.tpl')
<form class="md-form form-horizontal">
% include('input_dlg.tpl')
</form>

<!-- include dialogs from template folder of module "{{module_name}}" -->
<form class="md-form form-horizontal">
% include('custom_dlg.tpl')
</form>



<p>
<button type="button" id="button1"
	class="btn btn-info btn-lg">
	<span class="glyphicon glyphicon-upload"></span> Hello JavaScript
</button>
<button type="button" id="button2"
	class="btn btn-info btn-lg">
	<span class="glyphicon glyphicon-heart"></span> Hello Brython
</button>
</p>

<p>
<button type="button" id="button3"
	class="btn btn-success btn-lg">
	<span class="glyphicon glyphicon-upload"></span> Confirm from JavaScript
</button>
<button type="button" id="button4"
	class="btn btn-success btn-lg">
	<span class="glyphicon glyphicon-heart"></span> Confirm from Brython
</button>
</p>

<p>
<button type="button" id="button5"
	class="btn btn-warning btn-lg">
	<span class="glyphicon glyphicon-upload"></span> Input from JavaScript
</button>
<button type="button" id="button6"
	class="btn btn-warning btn-lg">
	<span class="glyphicon glyphicon-heart"></span> Input from Brython
</button>
</p>

<p>
<button type="button" id="button7"
	class="btn btn-danger btn-lg">
	<span class="glyphicon glyphicon-upload"></span> Custom dlg from JavaScript
</button>
<button type="button" id="button8"
	class="btn btn-danger btn-lg">
	<span class="glyphicon glyphicon-heart"></span> Custom dlg from Brython
</button>
</p>

<script type="text/javascript">

$("#button1").off().click(function(){
	ok_dlg('JavaScript','Hello from JavaScript');
});
$("#button3").off().click(function(){
	$("#btnconfirmok").off().click(function(){
		hide_confirm_dlg();
		ok_dlg('Ok','Ok from JavaScript');
	});
	$("#btnconfirmcancel").off().click(function(){
		hide_confirm_dlg();
		ok_dlg('Cancel','Cancel from JavaScript');
	});
	show_confirm_dlg('Confirm', 'Confirm from JavaScript');
});
$("#button5").off().click(function(){
	$("#btninputok").off().click(function(){
		hide_input_dlg();
		your_name = $('#input_value').val();
		ok_dlg('Input from JavaScript',`Hello, ${your_name}!`);
	});
	show_input_dlg('Input from JavaScript', 'Name', 'your name');
});
$("#button7").off().click(function(){
	$("#btncustomok").off().click(function(){
		hide_custom_dlg();
		v1 = $('#custom_input_value1').val();
		v2 = $('#custom_input_value2').val();
		v3 = $('#custom_input_value3').val();
		ok_dlg('Custom Ok from JavaScript', `Ok: v1=${v1}, v2=${v2}, v3=${v3}`);
	});
	$("#btncustomcancel").off().click(function(){
		hide_custom_dlg();
		v1 = $('#custom_input_value1').val();
		v2 = $('#custom_input_value2').val();
		v3 = $('#custom_input_value3').val();
		ok_dlg('Custom Cancel from JavaScript', `Cancel: v1=${v1}, v2=${v2}, v3=${v3}`);
	});
	$("#btncustomhelp").off().click(function(){
		hide_custom_dlg();
		v1 = $('#custom_input_value1').val();
		v2 = $('#custom_input_value2').val();
		v3 = $('#custom_input_value3').val();
		ok_dlg('Custom Help from JavaScript', `Help: v1=${v1}, v2=${v2}, v3=${v3}`);
	});
	show_custom_dlg('Custom dlg from JavaScript', 'v1', '100', 'v2', '200', 'v3', '300');
});
</script>

<script type="text/python">

from browser import document, bind, window

@bind(document['button2'], 'click')
def _(evt):
	window.ok_dlg('Brython','Hello from Brython')

@bind(document['button4'], 'click')
def _(evt):
	def _ok_func():
		window.hide_confirm_dlg()
		window.ok_dlg('Ok','Ok from Brython')
	def _cancel_func():
		window.hide_confirm_dlg()
		window.ok_dlg('Cancel','Cancel from Brython')
	document['btnconfirmok'].unbind()
	document['btnconfirmok'].bind('click', _ok_func)
	document['btnconfirmcancel'].unbind()
	document['btnconfirmcancel'].bind('click', _cancel_func)
	window.show_confirm_dlg('Confirm', 'Confirm from Brython')

@bind(document['button6'], 'click')
def _(evt):
	def _ok_func():
		window.hide_input_dlg()
		your_name = document['input_value'].value
		message = 'Hello, {}!'.format(your_name)
		window.ok_dlg('Input from Brython', message)
	document['btninputok'].unbind()
	document['btninputok'].bind('click', _ok_func)
	window.show_input_dlg('Input from Brython', 'Name', 'your name')

@bind(document['button8'], 'click')
def _(evt):
	def _ok_func():
		window.hide_custom_dlg()
		v1 = document['custom_input_value1'].value
		v2 = document['custom_input_value2'].value
		v3 = document['custom_input_value3'].value
		message = 'Ok: v1={}, v2={}, v3={}'.format(v1, v2, v3)
		window.ok_dlg('Custom Ok from Brython', message)
	def _cancel_func():
		window.hide_custom_dlg()
		v1 = document['custom_input_value1'].value
		v2 = document['custom_input_value2'].value
		v3 = document['custom_input_value3'].value
		message = 'Cancel: v1={}, v2={}, v3={}'.format(v1, v2, v3)
		window.ok_dlg('Custom Cancel from Brython', message)
	def _help_func():
		window.hide_custom_dlg()
		v1 = document['custom_input_value1'].value
		v2 = document['custom_input_value2'].value
		v3 = document['custom_input_value3'].value
		message = 'Hello: v1={}, v2={}, v3={}'.format(v1, v2, v3)
		window.ok_dlg('Custom Help from Brython', message)
	document['btncustomok'].unbind()
	document['btncustomok'].bind('click', _ok_func)
	document['btncustomcancel'].unbind()
	document['btncustomcancel'].bind('click', _cancel_func)
	document['btncustomhelp'].unbind()
	document['btncustomhelp'].bind('click', _help_func)
	window.show_custom_dlg('Custom dlg from Brython', 'v1', '1', 'v2', '2', 'v3', '3');

</script>


% include('footer.tpl')
