<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AWS EC2 Controller</title>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<script>


function ajax_ec2(e) {
	for (var id in e) {
		var i = e[id];
		$("#ec2-content").append("<div class='ec2' data-ec2='"+i["id"]+"'>"+i["last-launch"]+"</div>");
		alert(e[i]["last-launch"]);
	}
}

function refresh_ec2() {
	$.ajax({
		url: "aws.py",
		data: {},
		success: ajax_ec2,
		dataType: "json"
	});
}




$(document).ready(function () {
	refresh_ec2();
});

</script>

</head>
<body>

<div class="container" id="ec2-content">

</div>

</body>
</html>