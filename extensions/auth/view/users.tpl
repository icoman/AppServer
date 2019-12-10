% include('header.tpl', local_py=['users.script'], usebrython=True)

<b>Users</b>
<input type="button" id="addbtn" value="Add" class="btn btn-success" disabled="yes" />
<input type="button" id="refreshbtn" value="Show All" class="btn btn-primary" disabled="yes" />
&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;
<input type="text" id="filter" value="" />
<input type="button" id="filterbtn" value="Filter" class="btn btn-primary" disabled="yes" />
<br><br>

<div id="divloader">
		<div class="loader col-xs-3"></div>
		<div class="col-xs-9"><h3 id="msgloader"></h3></div>
</div>
<table id="userstable" class="table table-nonfluid table-hover"></table>

% include('confirm_dlg.tpl')


<script>
$("input, password, select, textarea").attr("autocomplete", "off");
</script>

% include('footer.tpl')
