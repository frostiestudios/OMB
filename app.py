from bottle import request, static_file, template, redirect, route, run
import bottle
import sqlite3
import socket
import os

ip=socket.gethostbyname(socket.gethostname())

bottle.BaseRequest.MEMFILE_MAX = 500000000
@route('/pages/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./pages/')

@route('/')
def index():
    return template('./pages/index.html')

@route('/files')
def videos():
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute('SELECT id, name, file FROM videos')
    result = c.fetchall()
    c.close()
    output = template('./pages/videos.html',rows=result)
    return output

@route('/videos/upload', method='POST')
def do_upload():
    upload_name = request.forms.get('name')
    upload = request.files.get('file')
    if upload is not None:
        name, ext = os.path.splitext(upload.filename)
        save_path = "./media/videos"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        upload.save(save_path)
        conn = sqlite3.connect('media.db')
        c = conn.cursor()
        fname = name + ext
        c.execute("INSERT INTO videos (name,file) VALUES (?,?)",(upload_name,upload))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return "ERROR NO FILE UPLOADED"
run(host=ip,port=8888,debug=True,reloader=True)