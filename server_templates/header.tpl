<!DOCTYPE html>
<html lang="en">
<head>
%if vars().get('errmsg'):
<!-- Error:
{{errmsg}}
-->
%end

   <meta charset="utf-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1">
%if module_name:
   <base href="/{{module_name}}/">
%end
   <title>{{title}}</title>

   <link rel="icon" href="/static/favicon.ico">

   <link rel="stylesheet" type="text/css" href="/static/bootstrap3/css/bootstrap.min.css">
   <link rel="stylesheet" type="text/css" href="/static/navbar.css">
   <link rel="stylesheet" type="text/css" href="/static/main.css">

   <script type="text/javascript" src="/static/js/jquery-3.4.1.min.js"></script>
   <script type="text/javascript" src="/static/bootstrap3/js/bootstrap.min.js"></script>

   <link rel="stylesheet" type="text/css" href="/static/datetimepicker/jquery.datetimepicker.min.css">
   <script type="text/javascript" src="/static/datetimepicker/jquery.datetimepicker.full.min.js"></script>




%if vars().get('local_css'):
   <!-- module {{module_name}} css -->
%for i in local_css:
%if i.startswith("/"):
   <link rel="stylesheet" type="text/css" href="{{i}}">
%else:
   <link rel="stylesheet" type="text/css" href="/{{module_name}}/static/{{i}}">
%end
%end
%end

%if vars().get('local_js'):
   <!-- module {{module_name}} js scripts -->
%for i in local_js:
%if i.startswith("/"):
   <script type="text/javascript" src="{{i}}"></script>
%else:
   <script type="text/javascript" src="/{{module_name}}/static/{{i}}"></script>
%end
%end
%end

%if vars().get('usebrython'):
   <script type="text/javascript" src="/static/brython-3.6.2/brython.js"></script>
   <script type="text/javascript" src="/static/brython-3.6.2/brython_stdlib.js"></script>
%end


%if vars().get('local_py'):
   <!-- module {{module_name}} python scripts -->
%for i in local_py:
%if i.startswith("/"):
   <script type="text/python" src="{{i}}"></script>
%else:
   <script type="text/python" src="/{{module_name}}/static/{{i}}"></script>
%end
%end
%end



<script>
<!--
function info(){
	var loadTime = window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart;
	console.log('Window load:', loadTime, 'ms.');
};
$(document).ready(function(){
%if vars().get('usebrython'):
  brython();
%end
  $('[data-toggle="tooltip"]').tooltip();
  info();
});
-->
</script>
</head>


<body id="body">


%if not vars().get('disable_navbar'):
<!--
Customized with Twitter Bootstrap 3 Menu Generator
http://bootstrap3-menu.codedorigin.com/
-->

<!-- start navbar -->
{{!navbar}}
<br><br><br>
<!-- end navbar -->
%end


%if not using_cookies:
<div class="alert alert-warning hidden-print">
% include('accept_cookies.tpl')
</div>
%end



%if userid:
%if module_config.get('config menu'):
%include('adm_edcfg.tpl')
<p align="right" class="hidden-print">
%if module_config.get('user config'):
<button type="button" class="btn btn-primary btn-xs" 
	onclick="edit_user_config('{{module_name}}')" data-toggle="tooltip" data-placement="auto top"
	title="Edit user config" ><span class="glyphicon glyphicon-cog"></span><span class="glyphicon glyphicon-user"></span>
</button>
%end
<button type="button" class="btn btn-danger btn-xs" 
	onclick="edit_module_config('{{module_name}}')" data-toggle="tooltip" data-placement="auto top"
	title="Edit module config" ><span class="glyphicon glyphicon-cog"></span><span class="glyphicon glyphicon-tasks"></span>
</button>
<a href="/adm" data-toggle="tooltip" data-placement="auto top" class="btn btn-warning btn-xs" title="Adm modules"><span class="glyphicon glyphicon-wrench"></span></a>
</p>
%end
%end

  
  
