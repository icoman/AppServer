
% include('header.tpl')

<h1>{{title}}</h1>
<a href="/{{module_name}}/">Module index</a><br>

<table class="table table-sm">
<tr>
<td>
<h1>User Config</h1>
<ul>
%for i in sorted(user_config.keys()):
<li>{{i}} = {{user_config.get(i)}}</li>
%end
</ul>
</td>
<td>
<h1>Module Config</h1>
<ul>
%for i in sorted(module_config.keys()):
<li>{{i}} = {{module_config.get(i)}}</li>
%end
</ul>
</td>
</tr>
</table>

% include('footer.tpl')
