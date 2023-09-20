from bottle import Bottle, request, static_file, template, redirect, route, run
from bottle_login import LoginPlugin
import sqlite3
import socket
import os
import configparser



def read_cfg():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config['Settings'].get("ServerDir",'')
directory_path = read_cfg()

print(directory_path) 
ip=socket.gethostbyname(socket.gethostname())



@route('/my_ip')
def show_ip():
    ip2 = request.environ.get('REMOTE_ADDR')
    # or ip = request.get('REMOTE_ADDR')
    # or ip = request['REMOTE_ADDR']
    return template("Your IP is: {{ip2}}", ip2=ip2)
@route('/pages/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./pages/')
@route('/media/video/<filename:path>')
def download(filename):
    return static_file(filename, root=f'{directory_path}/media/video/', download=filename)


@route('/')
def index():

    return template('./pages/index.html')


    return redirect('/')
@route('/files')
def videos():
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute('SELECT id, name, file FROM videos')
    result = c.fetchall()
    c.close()
    output = template('./pages/videos.html',rows=result)
    return output

@route('/files/upload')
def upload():
    return template('./pages/newfile.html')
@route('/files/upload', method='POST')
def do_upload():
    upload_name = request.forms.get('name')
    upload = request.files.get('upload')
    
    if upload is not None:
        name, ext = os.path.splitext(upload.filename)
        save_path = f"{directory_path}/media/video"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        upload.save(save_path)
        
        conn = sqlite3.connect('media.db')
        c = conn.cursor()
        fname = name + ext
        c.execute("INSERT INTO videos (name,file) VALUES (?,?)",(upload_name,fname))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return "ERROR NO FILE UPLOADED"
run(host=ip,port=5500,debug=True,reloader=True)