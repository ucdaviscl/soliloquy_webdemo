<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="UC Davis Utterance Variation Web Demo">
        <meta name="author" content="UC Davis Computational Linguistics Lab">
        <title>Utterance Variation: Sign In</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="text-center" style="padding-top:100px; justify-content: center; display: flex;">
        <form action="/authenticate" method="post" enctype="multipart/form-data">
            <img src="https://www.printwand.com/blog/media/2012/10/variety-of-assorted-apples-300x199.jpg" alt="" height="72">
            <h1 class="h3 mb-3 font-weight-normal">Sign In</h1>
            <label for="username" class="sr-only">Username</label>
            <input type="text" id="username" name="username" class="form-control" placeholder="Username" required autofocus>
            <label for="password" class="sr-only">Password</label>
            <input type="password" id="password" name="password" class="form-control" placeholder="Password" required>
            
            <div style="padding-top:30px">
                <button class="btn btn-lg btn-primary btn-block" type="submit" name="login_button">Sign in</button>
            </div>
        </form>
    </body>
</html>