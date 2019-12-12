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

function func_reload(data){
	location.reload(); 
}

function change_descr(module, description) {
	$('.tooltip').hide();
	$("#btninputok").off().click(function(){
		$('.tooltip').hide();
		hide_input_dlg();
		new_description = $('#input_value').val();
		tmpl = document.getElementById('tmpl');
		ix = tmpl.selectedIndex;
		v = tmpl.item(ix).value;
		post_request('/{{module_name}}/chdscr', {module:module,description:new_description}, func_reload);
	}); 
	show_input_dlg(`Change description for "${module}" ?`, 'Description', description);
}


function addmodule(){
	$('.tooltip').hide();
	$("#btninputok").off().click(function(){
		$('.tooltip').hide();
		hide_input_dlg();
		new_module_name = $('#input_value').val();
		if(new_module_name){
			tmpl = document.getElementById('tmpl');
			ix = tmpl.selectedIndex;
			v = tmpl.item(ix).value;
			post_request('/{{module_name}}/addmod', {tmpl:v,newmodulename:new_module_name}, func_reload);
		}
	}); 
	show_input_dlg('Add new module?', 'Name', 'new module');
}



function reboot_server(){
	$('.tooltip').hide();
	$("#btnconfirmok").off().click(function(){
		$('.tooltip').hide();
		hide_confirm_dlg();
		post_request('/{{module_name}}/restart', {}, func_reload);
	}); 
	show_confirm_dlg('Confirm', 'Restart server?');
}

</script>


<form class="form-inline">
<button type="button" class="btn btn-success" 
	data-toggle="tooltip" data-placement="auto bottom"
	onclick="addmodule()" title="Add module">
	<span class="glyphicon glyphicon-plus"></span>
	Add</button>
<select class="form-control" id="tmpl">
%for i in alltemplates:
<option value="{{i[0]}}">{{i[1]}}</option>
%end
</select>
</form>

<p align="right">
<button type="button" class="btn btn-danger" 
	data-toggle="tooltip" data-placement="auto bottom"
	title="Shutdown, then restart the webserver"
	onclick="reboot_server()"><span class="glyphicon glyphicon-repeat"></span> Restart Web Server</button>
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
<td>
	<button type="button" class="btn btn-primary btn-xs" 
		onclick="edit_user_config('{{m[0]}}')"
		data-toggle="tooltip" data-placement="auto top"
		title="Edit user config for module '{{m[0]}}'" > 
		<span class="glyphicon glyphicon-cog"></span><span class="glyphicon glyphicon-user"></span></button>
	<button type="button" class="btn btn-danger btn-xs" 
		onclick="edit_module_config('{{m[0]}}')"
		data-toggle="tooltip" data-placement="auto top"
		title="Edit module config for module '{{m[0]}}'" > 
		<span class="glyphicon glyphicon-cog"></span><span class="glyphicon glyphicon-tasks"></span></button>
</td>	
<td><a href="/{{m[0]}}/">/{{m[0]}}/</a></td>
<td>
	<button type="button" class="btn btn-success btn-xs" 
		onclick="change_descr('{{m[0]}}','{{m[1]}}')"
		data-toggle="tooltip" data-placement="auto left"
		title="Change '{{m[0]}}' description" > 
		<span class="glyphicon glyphicon-pencil"></span></button>
{{m[1]}}</td> 
</tr>
%end
</tbody>
</table>


% include('footer.tpl')
