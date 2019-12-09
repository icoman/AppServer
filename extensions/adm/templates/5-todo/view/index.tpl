% include('header.tpl', local_py=['todo.script'], usebrython=True)


<label>Todo list:</label>
<input type="button" id="addbtn" value="Add" class="btn btn-success" disabled="yes" />
<input type="button" id="refreshbtn" value="Show All" class="btn btn-primary" disabled="yes" />
&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;
<label for="filter">Filter:</label><input type="text" id="filter" value="" />
<input type="button" id="filterbtn" value="Filter" class="btn btn-primary" disabled="yes" />
<div id="info"></div>
<div id="table"></div>

% include('footer.tpl')
