% include('header.tpl', local_css = ['wiki.css'], usebrython=True)



<p align="right">
<span class="wikipath">{{wikipath}}</span>
%if is_wiki_admin:
-
<input type="button" id="editbtn" value="Edit" class="btn btn-success" title="Edit page" data-toggle="tooltip" />
%if version_index:
<input type="button" id="editverbtn" value="Edit this version" class="btn btn-warning" title="Edit shown version of this page" data-toggle="tooltip"/>
%end
<span data-toggle="modal" data-target="#upload">
<input type="button" id="uploadbtn" value="Upload" class="btn btn-primary"  title="Attach files" data-toggle="tooltip" />
</span>
<input type="button" id="deletebtn" value="Delete" class="btn btn-danger" title="Delete this page with all its versions" data-toggle="tooltip" />
%end
<br>
<a href="/{{module_name}}/all">All pages</a>
</p>

<h1 class="well well-sm wikititle">{{title or '-no title-'}}</h1>



<div class="fr">

%if attachments:
<div class="well allatt">
<h3>Page attachments:</h3>
<table class="table table-striped">
<tr><th>Filename</th><th>Created</th><th>Size</th></tr>
%for ix,i in enumerate(attachments):
<tr>
<td><a href="/{{module_name}}/get/{{page_id}}/{{ix}}">{{i[0]}}</a></td>
<td>{{i[1]}}</td>
<td>{{i[2]}}</td>
</tr>
%end
</table>
</div>
%end

<div class="well wikivers" id="divpagevers">
%if len(all_page_versions)>1:
<h3>Page versions:</h3>
<table class="table table-striped">
<tr><th>Title</th><th>Created</th><th>Owner</th><th></th></tr>
%for ix, page in enumerate(all_page_versions):
<tr>
<td>
%if is_wiki_admin or has_access(page[2]) or userid == page[0]:
<a href="/{{module_name}}{{wikipath}}?v={{ix}}">{{page[3] or '-no title-'}}</a>
%else:
{{page[3] or '-no title-'}}
%end
</td>
<td>{{page[4].strftime(datetimeformat)}}</td>
<td>{{page[1]}}</td>
<td>
%if is_wiki_admin or userid == page[0]:
<input type="button" verid="{{ix}}" title="Delete version {{len(all_page_versions)-ix}}" value="Del" class="btn btn-xs btn-danger" data-toggle="tooltip" />
<input type="button" verid="{{ix}}" title="Edit version {{len(all_page_versions)-ix}}" value="Ed" class="btn btn-xs btn-warning" data-toggle="tooltip" />
%end
</td>
</tr>
%end
</table>
%else:
<h3>No page versions</h3>
%end
</div>

</div>



<div class="wikibody">
{{!body}}
</div>


<div id="upload" class="modal fade" role="dialog">
  <div class="modal-dialog">
    <!-- Modal content-->
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h2 class="modal-title">Upload file</h2>
		<form method="POST" action="/{{module_name}}/upld" class="md-form form-horizontal" enctype="multipart/form-data">
		<input type="hidden" name="wikipath" value="{{wikipath}}">
    <div class="form-group">
		<div class="col-xs-2">
		</div>
		<div class="col-xs-10">
			<input type="file" class="btn btn-default btn-sm" name="upload">
		</div>
    </div>
    <div class="form-group">
		<div class="col-xs-2">
		</div>
		<div class="col-xs-10">
		<button type="submit" class="btn btn-success btn-sm"><span class="glyphicon glyphicon-paperclip"></span> Upload</span></button>
		<button type="button" class="btn btn-danger btn-sm" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span> Cancel</span></button>
		</div>
    </div>
		</form>

	</div>
	</div>
</div>
</div>
</div>






<script type="text/python">
from browser import document as doc, bind, window, prompt, alert, confirm



def delete_version_func(evt):
	verid = int(evt.target.attrs['verid'])
	title = evt.target.attrs['title']
	if confirm('Delete version {}?'.format({{len(all_page_versions)}}-verid)):
		window.location.href='/{{module_name}}/deletever{{wikipath}}?v={}'.format(verid)

def edit_version_func(evt):
	verid = int(evt.target.attrs['verid'])
	title = evt.target.attrs['title']
	if confirm('Edit version {}?'.format({{len(all_page_versions)}}-verid)):
		window.location.href='/{{module_name}}/edit{{wikipath}}?v={}'.format(verid)


%if is_wiki_admin and version_index:
@bind(doc['editverbtn'], 'click')
def edit_ver_func(evt):
	window.location.href='/{{module_name}}/edit{{wikipath}}?v={{version_index}}'
%end

%if is_wiki_admin:
@bind(doc['editbtn'], 'click')
def edit_func(evt):
	window.location.href='/{{module_name}}/edit{{wikipath}}'

@bind(doc['deletebtn'], 'click')
def delete_func(evt):
	if 'yes' == prompt('Are you sure you want to delete page?\n\nType "yes" to confirm.\n\n','no'):
		if confirm("Do you REALLY want to delete this page?\n\nAll versions will be deleted also.\n\n"):
			window.location.href='/{{module_name}}/delete{{wikipath}}'

%end


for btn in doc['divpagevers'].get(selector="INPUT"):
	if btn.value == 'Del':
		btn.bind('click', delete_version_func)
	if btn.value == 'Ed':
		btn.bind('click', edit_version_func)


</script>

% include('footer.tpl')
