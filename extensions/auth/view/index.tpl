% include('header.tpl')

<h1>{{title}}</h1>

<a href="/{{module_name}}/users">Edit Users</a><br>
<a href="/{{module_name}}/groups">Edit Groups</a><br>
<a href="/{{module_name}}/login">Login</a><br>
<a href="/{{module_name}}/logout">Logout</a><br>
<a href="/{{module_name}}/users/reset">Reset password</a><br>

% include('footer.tpl')
