% include('header.tpl', local_py=['todo.script'], usebrython=True)


<label>Todo list:</label>
<input type="button" id="addbtn" value="Add" class="btn btn-success" disabled="yes" />
<input type="button" id="refreshbtn" value="Show All" class="btn btn-primary" disabled="yes" />
&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;
<label for="filter">Filter:</label><input type="text" id="filter" value="" />
<input type="button" id="filterbtn" value="Filter" class="btn btn-primary" disabled="yes" />
<br><br>

<div id="info"></div>
<div id="divloader">
		<div class="loader col-xs-3"></div>
		<div class="col-xs-9"><h3 id="msgloader"></h3></div>
</div>
<div id="table"></div>

% include('confirm_dlg.tpl')

% include('footer.tpl')
