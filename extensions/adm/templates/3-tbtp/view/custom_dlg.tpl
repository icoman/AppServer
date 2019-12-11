<div id="customdlg" class="modal fade" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
		<h3 id="custom_input_title" class="modal-title">Title</h3>
      </div>
	  <div class="modal-body">
    <div class="form-group">
        <label id="custom_input_name1" class="control-label col-xs-2">Name:</label>
		<div class="col-xs-10">
        <input type="text" class="form-control" id="custom_input_value1" name="custom_input_value1" value="" placeholder="">
		</div>
	</div>
    <div class="form-group">
        <label id="custom_input_name2" class="control-label col-xs-2">Name:</label>
		<div class="col-xs-10">
        <input type="text" class="form-control" id="custom_input_value2" name="custom_input_value2" value="" placeholder="">
		</div>
	</div>
    <div class="form-group">
        <label id="custom_input_name3" class="control-label col-xs-2">Name:</label>
		<div class="col-xs-10">
        <input type="text" class="form-control" id="custom_input_value3" name="custom_input_value3" value="" placeholder="">
		</div>
	</div>
    <div class="modal-footer">
		<button type="button" class="btn btn-success btn-sm" id="btncustomok"><span class="glyphicon glyphicon-ok"></span> Ok</button>
		<button type="button" class="btn btn-danger btn-sm" id="btncustomcancel" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span> Cancel</button>
		<button type="button" class="btn btn-info btn-sm" id="btncustomhelp"><span class="glyphicon glyphicon-info-sign"></span> Help</button>
    </div>
	</div>
	</div>
</div>
</div>

<script>
$('#customdlg').on('shown.bs.modal', function () {
    $('#custom_input_value1').focus();
});  
function show_custom_dlg(title, name1, value1, name2, value2, name3, value3){
	$('#custom_input_title').text(title);
	$('#custom_input_name1').text(name1);
	$('#custom_input_value1').val(value1);
	$('#custom_input_name2').text(name2);
	$('#custom_input_value2').val(value2);
	$('#custom_input_name3').text(name3);
	$('#custom_input_value3').val(value3);
	$('#customdlg').modal('show');
}
function hide_custom_dlg(){
	$('#customdlg').modal('hide');
}
</script>

