% include('header.tpl')

<h1 class="col-sm-offset-2">{{title}}</h1>

%if emergency_admin_activated:
<div class="alert alert-warning">
Warning: Emergency Admin is activated!<br/><br/>
<a href="login?EmergencyAdmin=Yes">Login as Emergency Admin</a>
</div>
%end

%if notUsingCookies:
<div class="alert alert-warning">
Warning: You can not authenticate if you do not accept to use cookies!
</div>
%end

%if msg:
<div class="alert alert-warning">{{!msg}}</div>
%end

<form class="md-form form-horizontal" action="/{{module_name}}/login" method="post" enctype="multipart/form-data">
<input type="hidden" name="back" value="{{back}}" />

    <div class="form-group">
        <label for="user" class="control-label col-sm-2">User:</label>
		<div class="col-sm-4">
        <input type="text" class="form-control" id="user" name="user" value="" placeholder="your user name">
		</div>
	</div>
    <div class="form-group">
        <label for="password" class="control-label col-sm-2">Password:</label>
		<div class="col-sm-4">
        <input type="password" class="form-control" id="password" name="password" value="" placeholder="your password">
		</div>
	</div>
    <div class="form-group">
		<div class="col-sm-offset-1 col-sm-6">
		<button type="submit" class="btn btn-success btn" value="Login"><span class="glyphicon glyphicon-user"></span> Login</span></button>
		<a href="#" id="scanlink" class="btn btn-success btn" ><span class="glyphicon glyphicon-qrcode"></span> Scan Login</a>
		<a href="/{{module_name}}/users/reset" class="btn btn-warning btn"><span class="glyphicon glyphicon-lock"></span> Reset password</a>
		</div>
    </div>
</form>

<script>
function setScanLink(){
	//On android
	if(navigator.userAgent.toLowerCase().indexOf("android") !== -1) {
		pathArray = location.href.split( "/" );
		protocol = pathArray[0];
		host = pathArray[2];
		url = protocol + "//" + host;
		ret = encodeURIComponent(url+"/auth/users/qrscan?format={FORMAT}&type={TYPE}&meta={META}&code={CODE}");
		document.getElementById("scanlink").href = "zxing://scan/?ret="+ret;
	}
	else {
		//document.getElementById("scanlink").href = "https://play.google.com/store/apps/details?id=com.google.zxing.client.android";
		document.getElementById("scanlink").href = "http://zxing.appspot.com/scan";
	}
}

$(document).ready(function () {
	setScanLink();
});

</script>

% include('footer.tpl')
