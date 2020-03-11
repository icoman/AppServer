
<style>
.r { color:#FF0000}
.b { color:#000000}
</style>

<form id="edpropsform" class="form-horizontal" method="post" action="/adm/savecfg" enctype="multipart/form-data">
<input type="hidden" name="module" value="">
<input type="hidden" name="foruser" value="">
<input type="hidden" name="parameter1" value="">
<input type="hidden" name="parameter2" value="">
<input type="hidden" name="parameter3" value="">
<div id="edprops" class="modal fade" role="dialog">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
		<h4 id="edpropstitle" class="modal-title">-- edprops title --</h4>
      </div> 
	<div class="modal-body" id="edpropsloader">
		<div class="loader col-xs-3"></div>
		<div class="col-xs-9"><h3 id="edpropsmsgloader"></h3></div>
		<br><br><br><br>
	</div>
      <div class="modal-body" id="edpropscontent"></div>
      <div class="modal-footer" id="edpropsfooter">
		<button type="submit" class="btn btn-success btn-sm" name="act" value="go"><span class="glyphicon glyphicon-ok"></span> Save</button>
		<button type="button" class="btn btn-danger btn-sm" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span> Cancel</button>
      </div>
	</div>
  </div>
</div>
</form>


<script>

var col1 = 3; 			/* name of properties column */
var col2 = 12-col1; 	/* value of properties column */
var textarea_rows = 5;	/* number of rows */
var timeout_ajax = 7000; /* milliseconds */

var form_chunks = [];
var ajax_cnt = 0;
function adm_post_request(url, data, myfunc){
	ajax_cnt++;
	$.ajax({
		url: url,
		method: "POST",
		data: data,
		timeout: timeout_ajax
	}).done(function( ret ) {
		if(!ret.ok) {
			if(ret.data){
				$('#edpropsmsgloader').text(ret.data);
				}
			else {
				var cpst = 'Redirect '+'to';
				if(String(ret).indexOf(cpst) > -1){
					$('#edpropsmsgloader').text('Need authentication!');
					}
				else {
					$('#edpropsmsgloader').text('Server error, see console log for more.');
					console.log(ret);
					}
			}
		} else {myfunc(ret.data);ajax_cnt--;}
  }).fail(function( data ) {
		$('#edpropsmsgloader').text('Ajax error!');
	});
}

function hasClass(el, className) {
  if (el.classList)
    return el.classList.contains(className);
  else
    return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
}

function addClass(el, className) {
  if (el.classList)
    el.classList.add(className);
  else if (!hasClass(el, className)) el.className += " " + className;
}

function removeClass(el, className) {
  if (el.classList)
    el.classList.remove(className);
  else if (hasClass(el, className)) {
    var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
    el.className=el.className.replace(reg, ' ');
  }
}

function update_checks(){
	let alc = document.getElementById('edpropsform').querySelectorAll('input[type="checkbox"]');
	for (var i = 0; i < alc.length; i++) {
		alc[i].addEventListener("click", function (event) {
			let target = event.target;
			if(target.checked){
				removeClass(target.parentElement, 'b');
				addClass(target.parentElement, 'r');
			} else {
				removeClass(target.parentElement, 'r');
				addClass(target.parentElement, 'b');
			}
		});
	}
};

function render_undefined(i, id, ob){
	form_chunks[i] = `
<div class="form-group">
<label class="control-label col-xs-${col1}" title="${ob.description}">${ob.name}</label>
<div class="col-xs-${col2}">type "${ob.type}" - unknown form field</div>
</div>`;
}

function render_text(i, id, ob){
	form_chunks[i] = `
<div class="form-group">
<label for="ob${id}" class="control-label col-xs-${col1}" title="${ob.description}">${ob.name}</label>
<div class="col-xs-${col2}">
<input type="text" class="form-control" title="${ob.description}" id="ob${id}" name="par${id}" value="${ob.value}">
</div>
</div>`;
}

function render_password(i, id, ob){
	form_chunks[i] = `
<div class="form-group">
<label for="ob${id}" class="control-label col-xs-${col1}" title="${ob.description}">${ob.name}</label>
<div class="col-xs-${col2}">
<input type="password" class="form-control" title="${ob.description}" id="ob${id}" name="par${id}" value="${ob.value}">
</div>
</div>`;
}

function render_textarea(i, id, ob){
	form_chunks[i] = `
<div class="form-group">
<label for="ob${id}" class="control-label col-xs-${col1}" title="${ob.description}">${ob.name}</label>
<div class="col-xs-${col2}">
<textarea class="form-control" rows="${textarea_rows}" title="${ob.description}" id="ob${id}" name="par${id}">${ob.value}</textarea>
</div>
</div>`;
}


function render_checkbox(i, id, ob){
	var value=ob.value;
	var checked=ob.value && 'checked' || '';
	var ckcls=ob.value && 'r' || 'b';
	form_chunks[i] = `
<div class="form-group">
<label class="col-xs-${col1} control-label ${ckcls}" title="${ob.description}">${ob.name}
<input type="checkbox" title="${ob.description}" id="ob${id}" name="par${id}" value="yes" ${checked}>
</label>
<div class="col-xs-${col2}">
<label class="control-label">${ob.description}</label>
</div>
</div>`;
}

function render_select(iii, id, ob){
	form = document.forms['edpropsform'];
	param_data = {
		parameter1:form.parameter1.value,
		parameter2:form.parameter2.value,
		parameter3:form.parameter3.value
		}
	adm_post_request(ob.posturl, param_data, function(jsdoc){
		ret = `
<div class="form-group">
<label for="ob${id}" class="control-label col-xs-${col1}" title="${ob.description}">${ob.name}</label>
<div class="col-xs-${col2}">`;
		ret += `<select name="par${id}">`;
		lista = ob.value;
		var keys = Object.keys(jsdoc);
		var int_keys = keys.map(function (x) { return parseInt(x, 10); });
		int_keys.sort(function(a, b){return a-b});
		for(var k in int_keys)
		{
			i = int_keys[k];
			value = jsdoc[i][0]; //name
			description = jsdoc[i][1]; //description
			selected = ob.value == value && 'selected' || '';
			ret += ` <option value="${value}"${selected}>${description}</option>`;
		}
		ret += '</select></div></div>';
		form_chunks[iii] = ret;
	});
}



/* render multiple checks */
function render_mc(iii, id, ob){
	form = document.forms['edpropsform'];
	param_data = {
		parameter1:form.parameter1.value,
		parameter2:form.parameter2.value,
		parameter3:form.parameter3.value
		}
	adm_post_request(ob.posturl, param_data, function(jsdoc){
		ret = `
<div class="form-group">
<label for="ob${id}" class="control-label col-xs-${col1}" title="${ob.description}">${ob.name}</label>
<div class="col-xs-${col2}">`;
		lista = ob.value;
		var keys = Object.keys(jsdoc);
		var int_keys = keys.map(function (x) { return parseInt(x, 10); });
		int_keys.sort(function(a, b){return a-b});
		for(var k in int_keys) {
			i = int_keys[k]; //SQL id
			sep = k>0?', ':'';
			if (lista.indexOf(i) > -1){cls='r';checked='checked';}
			else {cls='b';checked='';}
			var groupName=jsdoc[i][0]; //SQL name
			var description=jsdoc[i][1]; //SQL description
			ret += `
${sep}<label title="${description}" class="${cls}">
${groupName} <input type="checkbox" ${checked} name="par${id}" value="${i}" /></label>
`;
		}
		ret += '</div></div>';
		form_chunks[iii] = ret;
	});
}

function render_datetime(i, id, ob){
	form_chunks[i] = `
<div class="form-group">
<label for="ob${id}" class="control-label col-xs-${col1}" title="${ob.description}">${ob.name}<br>[${ob.format}]</label>
<div class="col-xs-${col2}">
<input type="text" class="form-control" title="${ob.description}" id="ob${id}" name="par${id}" value="${ob.value}">
</div>
</div>`;
	datetime_fields.push({id: "#ob"+id, format: ob.format});
}


function edit_doc(jsondoc){
	start_date = new Date();
	form_chunks = [];
	datetime_fields = [];
	form = document.forms['edpropsform'];
	data = jsondoc.data;
	fields = jsondoc.fields;
	var keys = Object.keys(data);
	var int_keys = keys.map(function (x) { return parseInt(x, 10); });
	int_keys.sort(function(a, b){return a-b});
	$('#edpropscontent').html('');
	for(i in int_keys){
		k = int_keys[i];
		type = data[k].type;
		try {render_func = eval('render_'+type);}
		catch(error){render_func = render_undefined;}
		form_chunks.push('');
		render_func(i, k, data[k]);
	}
	setTimeout(post_update_forms, 500);

}

function post_update_forms(){
	var msec_elapsed = (new Date() - start_date);
	if (msec_elapsed > 1000+timeout_ajax) {
		console.log('I give up');
		return;
	}
	if(ajax_cnt < 1){
		form_body = '';
		for (i=0;i<form_chunks.length;i++){
			form_body += form_chunks[i];
		}
		$('#edpropscontent').html(form_body);
		update_checks();
		for (i=0;i<datetime_fields.length;i++){
			ob=datetime_fields[i];
			$(ob.id).datetimepicker({timepicker:true, format: ob.format});
		}
		$('#edpropsloader').hide();
		$('#edpropscontent').show();
		$('#edpropsfooter').show();
	} else {setTimeout(post_update_forms, 300);}
}


function edit_module_config(module){
	ajax_cnt = 0;
	$('.tooltip').hide();
	$('#edpropstitle').text(`Edit module config for module "${module}"`);
	document.forms['edpropsform'].module.value = module;
	document.forms['edpropsform'].foruser.value = '';
	$('#edpropsmsgloader').text('Loading form ...');
	$('#edpropsloader').show();
	$('#edpropscontent').hide();
	$('#edpropsfooter').hide();
	$('#edprops').modal('show');
	adm_post_request('/adm/getcfg', {module:module}, edit_doc);
}

function edit_user_config(module){
	ajax_cnt = 0;
	$('.tooltip').hide();
	$('#edpropstitle').text(`Edit user config for module "${module}"`);
	document.forms['edpropsform'].module.value = module;
	document.forms['edpropsform'].foruser.value = true;
	$('#edpropsmsgloader').text('Loading form ...');
	$('#edpropsloader').show();
	$('#edpropscontent').hide();
	$('#edpropsfooter').hide();
	$('#edprops').modal('show');
	adm_post_request('/adm/getcfg', {module:module, foruser:true}, edit_doc);
}
</script>




