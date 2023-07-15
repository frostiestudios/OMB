from bottle import request, static_file, template, redirect, route, run
import bottle
import sqlite3
import socket
import os

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

bottle.BaseRequest.MEMFILE_MAX = 500000000
@route('/')
def index():
    return static_file('index.html',root='./pages/')

@route('/videos')
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
    name, ext = os.path.splitext(upload.filename)
    save_path = "./media/videos"
    if not os.path.exists(save_path):
        os.makedirs(saved_path)
    upload.save(path)
run(host=IPAddr,port=5500,debug=True,reloader=True)