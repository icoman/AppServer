
% include('header.tpl')

<h1>{{title}}</h1>

<p id="infotab">Starting "{{user_config.get('job title')}}" ...</p>

<script>
	function info(msg){
		console.log('msg=',msg);
		if(msg){
			document.getElementById("infotab").innerHTML += '<br>'+msg;
		}
	}
</script>



% include('footer.tpl')
