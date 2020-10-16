<!-- input dialog -->
<div id="inputdlg" class="modal fade" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
		<h3 id="input_title" class="modal-title">Title</h3>
      </div>
	  <div class="modal-body">
    <div class="form-group">
        <label id="input_name" class="control-label col-xs-3">Name:</label>
		<div class="col-xs-9">
        <input type="text" class="form-control" id="input_value" name="name" value="" placeholder="name">
		</div>
	</div>
    <div class="modal-footer">
		<button type="button" class="btn btn-success btn-sm" id="btninputok"><span class="glyphicon glyphicon-ok"></span> Ok</button>
		<button type="button" class="btn btn-danger btn-sm" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span> Cancel</button>
    </div>
	</div>
	</div>
</div>
</div>

<script>
$('#inputdlg').on('shown.bs.modal', function () {
    $('#input_value').focus();
    //setTimeout(()=>{ 
    //    $('#input_value').focus(); 
    //}, 500);
});

//prevent form submit when Enter key is pressed
//but not when inside textarea
$(document).keypress(
  function(event){
    if (event.which == '13' && event.target.type != 'textarea')
      event.preventDefault();
    });

function show_input_dlg(title, name, value){
	$('.tooltip').hide();
	$('#input_title').text(title);
	$('#input_name').text(name);
	$('#input_value').val(value);
	$('#inputdlg').modal('show');
}
function hide_input_dlg(){
	$('#inputdlg').modal('hide');
}
</script>
