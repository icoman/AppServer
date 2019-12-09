% include('header.tpl')

<h1 class="col-sm-offset-2">{{title}}</h1>

%if msg:
<div>{{msg}}</div>
%else:
<form class="md-form form-horizontal" action="/{{module_name}}/users/reset" method="post" enctype="multipart/form-data">
    <div class="form-group">
        <label for="email" class="control-label col-sm-2">Email:</label>
		<div class="col-sm-4">
        <input type="text" class="form-control" id="email" name="email" value="" placeholder="your email">
		</div>
	</div>
    <div class="form-group">
		<div class="col-sm-offset-2 col-sm-4">
		<button type="submit" class="btn btn-primary btn-sm"><span class="glyphicon glyphicon-lock"></span> Reset password</span></button>
		<a href="/{{module_name}}/login" class="btn btn-success btn-sm"><span class="glyphicon glyphicon-user"></span> Login</a>
		</div>
    </div>
</form>
%end

% include('footer.tpl')
