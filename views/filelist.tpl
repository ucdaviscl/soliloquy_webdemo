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
    		%if err != None:
        <div class="alert" 
            style="padding: 20px;
            padding-left: 100px;
            background-color: #f44336;
            color: white;
            opacity: 1;
            transition: opacity 0.6s;
            margin-bottom: 15px;">
            <span class="closebtn">&times;</span>  
            Error Message.
        </div>
        %end

        <script>
            var close = document.getElementsByClassName("closebtn");
            var i;
        
            for (i = 0; i < close.length; i++) {
              close[i].onclick = function(){
                var div = this.parentElement;
                div.style.opacity = "0";
                setTimeout(function(){ div.style.display = "none"; }, 600);
              }
            }
        </script>

        <div class="container" style="padding: 100px; padding-bottom: 20px;">
            <h2>Utterance Variety Generation</h2>

            <div style="padding-top:30px">
                <!--p>Upload a text file with one sentence/utterance per line, or select 
                    an existing file to paraphrase, view or annotate.
                </p-->
            </div>
        </div>


        <div class="container" style="padding: 100px; padding-top:0px;">
            <h6>To upload a file to paraphrase, browse for a text file with one sentence/utterance per line and click the Upload button:</h6>
            <div id="upload" class="input-group">
                <form action="/upload" method="post" enctype="multipart/form-data" style="width: 100%;">
                    <input type='hidden' name='username' value='{{username}}' />
                    <div class="input-group">
                    <div class="custom-file">
                        <input type="file" name="upload" class="custom-file-input" id="inputGroupFile04" onchange="$('#filenamedisplay').html(this.files[0].name)" />
                        <label class="custom-file-label" for="inputGroupFile04" id="filenamedisplay">Choose new file</label>
                    </div>
                    <div class="input-group-append">
                        <button class="btn btn-primary" name="submit_button_delete">Upload</button>
                    </div>
                    </div>
                </form>
            </div>
        </div>

        <div class="container" style="padding: 100px; padding-top:0px;">
            <h6>Or select an existing file and choose an action:</h6>
            <form action="/list" method="post" onsubmit="">
                <input type='hidden' name='username' value='{{username}}'>
                
                %if filelist == []:
          			<div>No files</div>
        		%else:
          		%for item in filelist:
                <div class="inputGroup">
                    <input value="{{item}}" id="{{item}}" name="radio" type="radio"/>
                    <label for="{{item}}">{{item}}</label>
                </div>
				%end
				%end
				
				<button class="btn btn-primary" name="submit_button_paraphrase">Paraphrase</button>
                <button class="btn btn-primary" name="submit_button_view">View</button>
                <!--button class="btn btn-primary" name="submit_button_annotate">Annotate</button-->
                <button class="btn btn-primary" name="submit_button_delete">Delete</button>

            </form>
        </div>
        
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha256-4+XzXVhsDmqanXGHaHvgh1gMQKX40OUvDEBTu8JcmNs=" crossorigin="anonymous"></script>
    </body>
</html>