% include('header.tpl', disable_navbar=True)

<h1>{{title}}</h1>

<div class="hidden-print">
<a href="javascript:window.print()" class="btn btn-success btn-lg"><span class="glyphicon glyphicon-print"></span> Print</a>
<a href="javascript:window.close()" class="btn btn-danger btn-lg"><span class="glyphicon glyphicon-off"></span> Close</a>
<br><br>
Scan code with <a href="http://zxing.appspot.com/scan">Barcode Scanner</a>
from ZXing Team.
<br><br>
Login link: <a href="{{qrdata}}">{{qrdata[:50]}} ...</a>
<br><br>
</div>
{{!imgout}}


% include('footer.tpl')
