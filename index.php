<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AWS EC2 Controller</title>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<link rel="stylesheet" href="style.css">

<script>


function ajax_ec2(e) {
	for (var id in e) {
		var i = e[id];
		$("#ec2-content").append("<div class='col-xs-12 ec2 state-"+i["state"]+"' data-ec2='"+i["id"]+"'></div>");
		var ec2 = $("div[data-ec2="+i["id"]+"]");
		ec2.append("<h2>"+i["architecture"]+" "+i["id"]+"</h2>");
		ec2.append("<p>Status: "+i["state"]+"<br>Last launched on "+i["last-launch"]+"<br>Private IP: "+i["private-ip"]+"</p>");
		for (var tname in i["tags"]) {
			ec2.append("<p class='tags'>"+tname+" = "+i["tags"][tname]+"</p>");
		}
		ec2.append("<p class='action'>&nbsp;</p>");
	}
	progress(false);
}


function progress(t=true) {
	$(".loader").css("display",t==true ? "block" : "none");
}

function refresh_ec2() {
	progress(true);
	$.ajax({
		url: "aws.py",
		data: {},
		success: ajax_ec2,
		dataType: "json"
	});
}




$(document).ready(function () {
	refresh_ec2();
	
	$(".ec2.state-stopped").click(function () {
		$(this).find("p.action").text("Click to launch instance...");
	});
	
	$(".ec2.state-running").click(function () {
		$(this).find("p.action").text("Click to stop instance...");
	});
	
	$(".ec2.state-pending").click(function () {
		$(this).find("p.action").text("Please wait until the instance is in a fixed state...");
	});
	
});

</script>

</head>
<body>

<div class="container" id="ec2-content">

</div>

<div class="loader">
</div>

</body>
</html>