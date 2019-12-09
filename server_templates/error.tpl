% include('header.tpl')

%if vars().get('title'):
<h1>{{title}}</h1>
%end

%if vars().get('body'):
<h2 class="alert alert-danger">{{body}}</h2>
%end

%if vars().get('traceback'):
<p>
<pre>
{{traceback}}
</pre>
</p>
%end

% include('footer.tpl')

