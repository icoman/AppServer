
% include('header.tpl')

<h1>{{title}}</h1>
<a href="/{{module_name}}/">Module index</a><br>

<hr>
<table class="table table-bordered">
<tr><th><h1>GET Form:</h1></th><th><h1>POST Form:</h1></th></tr>
<tr>
<td>
<form method="GET">
Get value: <input type="text" name="get_value" size="12" />
<input type="submit" class="btn btn-primary" name="action" value="Test get 1" />
<input type="submit" class="btn btn-primary" name="action" value="Test get 2" />
</form>
</td>
<td>
<form method="POST">
Post value: <input type="text" name="post_value" size="12" />
<input type="submit" class="btn btn-primary" name="action" value="Test post 1" />
<input type="submit" class="btn btn-primary" name="action" value="Test post 2" />
</form>
</td>
</tr>

<tr>
<td>
<ul>
%for k in get_vars:
<li>{{k}} = {{get_vars[k]}}</li>
%end
</ul>
</td>
<td>
<ul>
%for k in post_vars:
<li>{{k}} = {{post_vars[k]}}</li>
%end
</ul>
</td>
</tr>
</table>

% include('footer.tpl')
