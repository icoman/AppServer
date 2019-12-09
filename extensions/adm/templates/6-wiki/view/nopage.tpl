% include('header.tpl')

<h1 class="well well-sm wikititle">{{title or '-no title-'}}</h1>

<p align="right">
<span class="wikipath">{{wikipath}}</span>
</p>

<a href="/{{module_name}}/create{{wikipath}}">Create page</a>,
see <a href="/{{module_name}}/all">All pages</a>
or go
<a href="/{{module_name}}">Home</a>.

% include('footer.tpl')
