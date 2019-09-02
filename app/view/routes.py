#-*- coding:utf-8 -*-

from flask import render_template, request, session, url_for, current_app
#from . import app, socketio
from flask_socketio import emit
import time


users = {}

class MsgFrame():

    def __init__(self, user, msg, typ):
        self._data = { 
                'user' : user,
                'message' : msg,
                'time' : time.strftime('%H:%M'),
                'type' : typ
                }

    def getFrame(self):
        return self._data


def create_endpoints(app, socketio):

    @app.route('/')
    def index():
        return render_template('login.html'), 400


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        else:
            error = "Incorrect uer ID or password"
            return render_template('login.html', error=error)

    @app.route('/main', methods=['POST'])
    def nicklogin():
        nickname = request.form['nickname']

        if nickname in users:
            error = nickname + "nickname already exists"
            return render_template('login.html', error=error)

        users[nickname] = {
                'portrait' : None,
                'current' : None
                }

        session['username'] = nickname
        return render_template('main.html', nickname=request.form['nickname'])

    @socketio.on('connect', namespace='/nicklogin')
    def on_connect():

        temp = MsgFrame('system', session['username'] + ' has joined.', 'system')
        emit('message', temp.getFrame(), broadcast=True)


    @socketio.on('disconnect', namespace='/nicklogin')
    def on_disconnect():

        del users[session['username']]

        temp = MsgFrame('system', session['username'] + ' has left.', 'system')
        emit('message', temp.getFrame(), broadcast=True)



    @socketio.on('post-message', namespace='/nicklogin')
    def on_post_message(message):
        data_dict = {
                'user' : session['username'],
                'message' : message['message'],
                'time' : time.strftime('%H:%M'),
                'type' : 'chat'
                }
        emit('message', data_dict, broadcast=True, include_self=False )

        data_dict['type'] = 'chat_self'
        emit('message', data_dict, broadcast=False)


