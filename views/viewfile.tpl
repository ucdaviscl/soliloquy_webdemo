<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="UC Davis Utterance Variation Web Demo">
        <meta name="author" content="UC Davis Computational Linguistics Lab">
        <title>Utterance Variation: Sign In</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <link href="static/css/form.css" rel="stylesheet">
    </head>

<body>
    <div class="container" style="padding: 100px;">
		<div style="background: #fff">
			<h2>Utterance Variety: {{filename}}</h2>
            <br>
                <textarea readonly="True" style="font-family:monospace; width: 100%; height: 500px; padding: 20px; background: #eeefff;">{{textstr}}</textarea>
            <br>
		
		    <form class="form" action="/list" method="post" onsubmit="">
				<input type='hidden' name='username' value='{{username}}'>
        		<button class="btn btn-primary">Back to main menu</button>
            </form>
        </div>
  	</body>
</html>