<!-- ok dialog -->
<div id="okdlg" class="modal fade" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
		<h3 id="ok_title" class="modal-title">Title</h3>
      </div>
	<div class="modal-body">
	<div class="form-group">
        <label id="ok_msg" class="control-label">Message</label>
	</div>
    <div class="modal-footer">
		<button type="button" class="btn btn-success btn-sm" data-dismiss="modal"><span class="glyphicon glyphicon-ok"></span> Ok</button>
    </div>
	</div>
	</div>
</div>
</div>

<script>
function ok_dlg(title, message) {
	$('.tooltip').hide();
	$('#ok_title').text(title);
	$('#ok_msg').text(message);
	$('#okdlg').modal('show');
}
</script>
