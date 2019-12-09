% include('header.tpl')

<!-- Admin module -->
%include('adm_edcfg.tpl')

<script>
function func_reload(data){
	location.reload(); 
}

function change_descr(module, description) {
	new_description = prompt("Change description?", description);
	if (new_description != null){
		adm_post_request('/{{module_name}}/chdscr', {module:module,description:new_description}, func_reload);
	}
}

function restart(){
	if(confirm('Are you sure you want to restart webserver?')){
		adm_post_request('/{{module_name}}/restart', {}, func_reload);
	}
}

function addmodule(){
	newmodulename = prompt("New module name?", 'new module');
	if(newmodulename != null){
		tmpl = document.getElementById('tmpl');
		ix = tmpl.selectedIndex;
		v = tmpl.item(ix).value;
		adm_post_request('/{{module_name}}/addmod', {tmpl:v,newmodulename:newmodulename}, func_reload);
	}
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
<a href="#" onclick="restart();return false;" class="btn btn-danger btn" 
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

