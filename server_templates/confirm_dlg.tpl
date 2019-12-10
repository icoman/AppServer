<!-- confirm dialog -->
<div id="confirmdlg" class="modal fade" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
		<h3 id="confirm_title" class="modal-title">Title</h3>
      </div>
	<div class="modal-body">
	<div class="form-group">
        <label id="confirm_message" class="control-label">Message</label>
	</div>
    <div class="modal-footer">
		<button type="button" class="btn btn-success btn-sm" id="btnconfirmok"><span class="glyphicon glyphicon-ok"></span> Ok</button>
		<button type="button" class="btn btn-danger btn-sm" id="btnconfirmcancel" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span> Cancel</button>
    </div>
	</div>
	</div>
</div>
</div>

<script>
function show_confirm_dlg(title, message){
	$('#confirm_title').text(title);
	$('#confirm_message').text(message);
	$('#confirmdlg').modal('show');
}
function hide_confirm_dlg(){
	$('#confirmdlg').modal('hide');
}
</script>
