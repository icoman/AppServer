% include('header.tpl', local_js=['sample.js'], local_py=['sample.pyscript'], local_css=['sample.css'])

Sample template with
sample.js, sample.css and sample.pyscript
delivered from local module static folder
/{{module_name}}/static/sample.js
/{{module_name}}/static/sample.css
/{{module_name}}/static/sample.pyscript


Variables local_js, local_css and local_py are lists of filenames.

% include('footer.tpl')



