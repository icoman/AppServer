% include('header.tpl')

<!-- Admin module -->

% include('adm_edcfg.tpl')

% include('confirm_dlg.tpl')

<form class="md-form form-horizontal">
% include('input_dlg.tpl')
</form>

% include('ok_dlg.tpl')


<script>

function post_request(url, data, myfunc){
	$.ajax({
		url: url,
		method: "POST",
		data: data,
		timeout: timeout_ajax
	}).done(function( ret ) {
		if(!ret.ok) {
			if(ret.data){
				ok_dlg('Error',ret.data);
				}
			else {
				var cpst = 'Redirect '+'to';
				if(String(ret).indexOf(cpst) > -1){
					ok_dlg('Error','Need authentication!');
					}
				else {
					ok_dlg('Server error',ret);
					}
			}
		} else {myfunc(ret.data);}
  }).fail(function( data ) {
		ok_dlg('Error','Ajax error!');
	});
}

$('#confirm_title').text('Confirm');
$('#confirm_msg').text('Restart server?');
$("#btnconfirmok").click(function(){
	$('.tooltip').hide();
	$('#confirmdlg').modal('hide');
	post_request('/{{module_name}}/restart', {}, func_reload);
});

function func_reload(data){
	location.reload(); 
}

function change_descr(module, description) {
	$('.tooltip').hide();
	$('#input_title').text(`Change description for "${module}" ?`);
	$('#input_name').text('Description');
	$('#input_value').val(description);
	$("#btninputok").click(function(){
		$('.tooltip').hide();
		$('#inputdlg').modal('hide');
		new_description = $('#input_value').val();
		tmpl = document.getElementById('tmpl');
		ix = tmpl.selectedIndex;
		v = tmpl.item(ix).value;
		post_request('/{{module_name}}/chdscr', {module:module,description:new_description}, func_reload);
	}); 
	$('#inputdlg').modal('show');
}


function addmodule(){
	$('.tooltip').hide();
	$('#input_title').text('New module name?');
	$('#input_name').text('Name');
	$('#input_value').val('new module');
	$("#btninputok").click(function(){
		$('.tooltip').hide();
		$('#inputdlg').modal('hide');
		new_module_name = $('#input_value').val();
		if(new_module_name){
			tmpl = document.getElementById('tmpl');
			ix = tmpl.selectedIndex;
			v = tmpl.item(ix).value;
			post_request('/{{module_name}}/addmod', {tmpl:v,newmodulename:new_module_name}, func_reload);
		}
	}); 
	$('#inputdlg').modal('show');
}
</script>


<form class="form-inline">
<input type="button" value="Add" class="btn btn-success" 
	data-toggle="tooltip" data-placement="auto bottom"
	onclick="addmodule()" title="Add module" />
<select class="form-control" id="tmpl">
%for i in alltemplates:
<option value="{{i[0]}}">{{i[1]}}</option>
%end
</select>
</form>

<p align="right">
<a href="#confirmdlg" class="btn btn-danger btn" 
	data-toggle="modal"
	data-toggle="tooltip" data-placement="auto bottom"
	title="Shutdown, then restart the webserver"><span class="glyphicon glyphicon-repeat"></span> Restart Webserver</a>
</p>

<p>Python version: {{pyver}}</p>

<table class="table table-nonfluid table-hover">
<thead>
<tr><th>Module Name</th><th>Config</th><th>Link</th><th>Module Description</th></tr>
</thead>
<tbody>
%for m in allmodules:
<tr>
<td>{{m[0]}}</td>
<td><a href="#" onclick="edit_user_config('{{m[0]}}');return false;" 
	data-toggle="tooltip" data-placement="auto top"
	class="btn btn-primary btn-xs" 
	title="Edit user config for module '{{m[0]}}'"><span class="glyphicon glyphicon-cog"></span><span class="glyphicon glyphicon-user"></span></a>
	<a href="#" onclick="edit_module_config('{{m[0]}}');return false;" 
	data-toggle="tooltip" data-placement="bottom"
	class="btn btn-danger btn-xs" 
	title="Edit module config for module '{{m[0]}}'"><span class="glyphicon glyphicon-cog"></span><span class="glyphicon glyphicon-tasks"></span></a>
</td>	
<td><a href="/{{m[0]}}/">/{{m[0]}}/</a></td>
<td><a href="#" onclick="change_descr('{{m[0]}}','{{m[1]}}');return false;"
	data-toggle="tooltip" data-placement="auto left"
	class="btn btn-success btn-xs" 
	title="Change '{{m[0]}}' description"><span class="glyphicon glyphicon-pencil"></span></a>
{{m[1]}}</td> 
</tr>
%end
</tbody>
</table>


% include('footer.tpl')
