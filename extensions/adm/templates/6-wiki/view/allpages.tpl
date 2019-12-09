% include('header.tpl', local_css = ['wiki.css'])


<h1 class="well well-sm wikititle">{{title}}</h1>


<table class="table">
<tr>
<th>Link</th><th>Title</th><th>Author</th><th>Created</th><th>Updated</th><th>Versions</th>
</tr>
%for i in all_pages:
<tr>
<td>
%if i[5]:
	<a href="/{{module_name}}{{i[1]}}">/{{module_name}}{{i[1]}}</a>
%else:
	/{{module_name}}{{i[1]}}
%end
</td>
<td>{{i[2] or '-no title-'}}</td>
<td>{{i[0]}}</td>
<td><b>{{i[3]}}</b></td>
<td><b>{{i[4]}}</b></td>
<td>{{i[5]}} versions.</td>
</tr>
%end
</table>

% include('footer.tpl')
