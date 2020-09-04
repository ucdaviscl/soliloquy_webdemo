
from gevent import monkey; monkey.patch_all()
import bottle
import os
import sqlite3
import tempfile
import parainfer



STATICPATH = 'static'

# The database name
DBNAME = 'parapi.db'
USERDBNAME = 'user.db'

PAGESIZE = 3

# The paraphrasing model
t5p = parainfer.parainfer()

# If the db doesn't exist, create it
if not os.path.exists(DBNAME):
    conn = sqlite3.connect(DBNAME)
    conn.execute("CREATE TABLE parapi (user TEXT, id INTEGER, pid INTEGER, filename TEXT, sentence TEXT, approved BOOL, PRIMARY KEY (user, id, pid, filename))")
    conn.commit()
    conn.close()
    
if not os.path.exists(USERDBNAME):
    conn = sqlite3.connect(USERDBNAME)
    conn.execute("CREATE TABLE user (username TEXT, password TEXT, PRIMARY KEY (username))")
    conn.commit()
    conn.close()
    
@bottle.route('/')
def do_login():
    return bottle.template('login')
    
@bottle.route('/authenticate', method='POST')
def do_authenticate():
    
    # get the username and password
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    
    conn1 = sqlite3.connect(USERDBNAME)
    c1 = conn1.cursor()
    c1.execute('SELECT EXISTS(SELECT 1 FROM user WHERE username=? AND password=?)', (username, password, ))
    a = c1.fetchone()
    if a[0] == 1:
        conn1.close()
    
        bottle.response.status = 307
        bottle.response.set_header('Location', '/list')
    
        return
    
    #bottle.response.status = 307
    #bottle.response.set_header('Location', '/')
    
    return bottle.redirect('/')
    
# Uploading a file will add each line of the file to the db
@bottle.route('/upload', method='POST')
def do_upload():
    
    # get the upload
    upload = bottle.request.files.get('upload')
    username = bottle.request.forms.get('username')
    
    # connect to the db, check if the filename is already in the db
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    if upload is None:
        bottle.response.status = 307
        bottle.response.set_header('Location', '/list')
    
        return
        #return bottle.redirect('/list')
        
    c.execute('SELECT EXISTS(SELECT 1 FROM parapi WHERE user=? AND filename=?)', (username, upload.filename, ))
    a = c.fetchone()
    if a[0] == 1:
        conn.close()
        
        resstr = '''
            <body onload="document.form.submit()">
            <form action="/list" name="form" method="post">
            <input type="hidden" name="err" value="Cannot upload: file exists" />
            <input type="hidden" name="username" value="''' + username + '''" />
            </form>
            </body>
            '''

        return resstr
        
    # save the contents of the file to a tempfile,
    # read the tempfile line by line, inserting lines in the db
    with tempfile.TemporaryFile() as fp:
        upload.save(fp)
        fp.seek(0)
        
        id = 0
        for line in fp:
            line = line.decode('utf-8').strip()
            c.execute('INSERT INTO parapi (user, id, pid, filename, sentence, approved) VALUES (?, ?, 0, ?, ?, NULL)', 
                (username, id, upload.filename, line))
            id += 1
    
    conn.commit()
    conn.close()

    bottle.response.status = 307
    bottle.response.set_header('Location', '/list')
    
    return

# Reinitialize the databse. Delete old db, and create new db
@bottle.route('/initdb')
def do_initdb():
    if os.path.exists(DBNAME):
        os.remove(DBNAME)
    conn = sqlite3.connect(DBNAME)
    conn.execute("CREATE TABLE parapi (user TEXT, id INTEGER, pid INTEGER, filename TEXT, sentence TEXT, approved BOOL, PRIMARY KEY (user, id, pid, filename))")
    conn.commit()
    conn.close()
    
# Get a list of files in the db
@bottle.post('/list')
def list_files():
    
    # error code (might be None)
    err = bottle.request.forms.get('err')
       
    # connect to db
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    
    # get the username
    username = bottle.request.forms.get('username')
    
    print(">>>>>> USERNAME: ", username)

    # get the file selection, if there was one
    filename = bottle.request.forms.get('radio')
    
    # delete file
    if bottle.request.forms.get('submit_button_delete') is not None:
        if filename is not None:
            c.execute('DELETE FROM parapi WHERE user=? AND filename=?', (username, filename, ))
            
    # view file
    if bottle.request.forms.get('submit_button_view') is not None:
        if filename is not None:
            # find out how many lines are in file
            c.execute('SELECT COUNT(*) FROM parapi WHERE user=? AND filename=?', (username, filename, ))
            count = c.fetchall()[0][0]

            bottle.response.status = 307
            bottle.response.filename = filename
            bottle.response.username = username
            bottle.response.set_header('Location', '/view')
            return

    # paraphrase file
    if bottle.request.forms.get('submit_button_paraphrase') is not None:
        if filename is not None:
            
            # find out how many lines are in file
            c.execute('SELECT COUNT(*) FROM parapi WHERE user=? AND filename=? AND pid=0', (username, filename, ))
            count = c.fetchall()[0][0]
            conn.close()
            
            bottle.response.status = 307
            bottle.response.filename = filename
            bottle.response.username = username
            bottle.response.start = "0"
            bottle.response.total = str(count)
            bottle.response.set_header('Location', '/paraphrasefile')
            return
        
    # now get the list of all files in the db
    filelist = set([f[0] for f in c.execute("SELECT filename FROM parapi WHERE user=?", (username, ))])
    
    # close db
    conn.commit()
    conn.close()

    return bottle.template('filelist', filelist=list(filelist), err=err, username=username)

# View a file
@bottle.post('/view')
def do_view():
    
    # get the username and filename
    filename = bottle.response.filename
    username = bottle.response.username
    
    # get the utterances for this file from the db
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    c.execute('SELECT * FROM parapi WHERE user=? AND filename=?', (username, filename, ))

    res = c.fetchall()
    
    # sort by main id, then paraphrase id
    res.sort()

    strres = ""
    
    # go through each utterance
    for r in res:
        
        # field 2 is paraphrase id, and 0 means it's the original sentence
        if r[2] == 0:
            strres += "\nSentence %d:\n%s\n\n" % (r[1] + 1, r[4])
        else:
            # field 5 is a boolean that indicates whether the paraphrase 
            # has been approaved manually
            rating = "not rated"
            if r[5] == True:
                rating = "Approved"
            if r[5] == False:
                rating = "Not approved"
            
            strres += "Paraphrase %d (%s): %s\n" % (r[2], rating, r[4])

    return bottle.template('viewfile', textstr=strres, filename=filename, username=username)

# not in use
@bottle.route('/viewfile')
def do_viewfile():

    start = int(bottle.request.query.start)
    total = int(bottle.request.query.total)
    filename = bottle.request.query.filename
    
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    c.execute('SELECT * FROM parapi WHERE filename=? AND id>=? AND id<?', 
        (filename, start, start+PAGESIZE))
    
    res = c.fetchall()
    res.sort()
    #res = res[:PAGESIZE]
    
    newstart = start + PAGESIZE
    
    print(res)
    print(newstart)
    
    strres = ""
    for r in res:
        strres += "%d %d %s %s %s<br>" % (r[0], r[1], r[2], r[3], r[4])

    if newstart < total:
        strres += '<a href="/viewfile?filename=%s&start=%d&total=%d">Next</a><br>' % (filename, newstart, total)
        
    strres += '<a href="/list">Back to the main menu</a><br>'
    
    return strres

# Paraphrase a file
# (slow without GPU)
@bottle.post('/paraphrasefile')
def do_paraphrasefile():
    
    # these could be used if we paraphrase part of the file,
    # but for now every file is paraphrased all at once
    start = int(bottle.response.start)
    total = int(bottle.response.total)
    
    # get the username and filename for the db
    filename = bottle.response.filename
    username = bottle.response.username

    # if the starting line is beyond the total number of lines,
    # just go back to /list without doing anything
    if start > total:
        rstr = '''
        <form action="/list" name="form" method="post">
        <input type="hidden" name="username" value="''' + username + '''" />
        </form>
        <script>document.form.submit();</script>
        </body>
        </html>
        '''
        return rstr

    # prepare the progress bar
    pbar = '''
        <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>Utterance Variation: Paraphrasing</title>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
                </head>
                <body>
                    <div class="container">
                        <h2>Paraphrasing Progress</h2>
                        <div class="progress">
                            <div id="pbar" class="progress-bar" role="progressbar" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100" style="width: 0%">
                            </div>
                        </div>
                    </div>
    '''

    # print spaces to fill up the cache and start producing output on the browser
    for i in range(200):
        yield "&nbsp"
    yield pbar

    # connect to db
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    # get just the original utterances, and not any existing paraphrases
    c.execute('SELECT * FROM parapi WHERE user=? AND filename=? AND id>=? AND pid=0', 
        (username, filename, start, ))
    result = c.fetchall()
    
    # go through the original utternaces and paraphrase them
    cnt = 0
    for user, mainid, paraid, fname, sent, approved in result:
        cnt += 1
        
        # get a list of paraphrases for this line
        paras = t5p.generate(sent)
        
        # add each paraphrase to the db
        for p in paras:
            c.execute('SELECT * FROM parapi WHERE user=? AND filename=? AND id=? AND sentence=?', (username, filename, mainid, p))
            result = c.fetchone()

            if not result:
                c.execute('SELECT MAX(pid) FROM parapi WHERE user=? AND filename=? AND id=?', (username, filename, mainid))
                newpid = c.fetchone()[0] + 1
                c.execute('INSERT INTO parapi (user, id, pid, filename, sentence, approved) VALUES (?, ?, ?, ?, ?, NULL)', 
                    (username, mainid, newpid, fname, p))

        # calculate done percentage for the progress bar
        perc = str(int((start + cnt) * 100 / total))
            
        js = '<script>document.getElementById("pbar").style.width = "'+ perc + '%" </script>\n'
        
        yield js
           
    # done      
    conn.commit()
    conn.close()

    # go back to /list automatically
    start = start + PAGESIZE
    rstr = '''
        <form action="/list" name="form" method="post">
        <input type="hidden" name="username" value="''' + username + '''" />
        </form>
        <script>document.form.submit();</script>
        '''
    yield rstr + "</body></html>"

# access static files
@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=STATICPATH)
    
@bottle.route('/page/<filename>/<sessionid>/<page>')
@bottle.post('/page/<filename>/<sessionid>/<page>')
def page(filename, sessionid, page):
    
    if bottle.request.forms.get('done_button') is not None:
        return '<meta http-equiv="Refresh" content="0; /list" />'
        
    return 0


bottle.run(host='0.0.0.0', port=80, debug=True, reloader=True, server='gevent')