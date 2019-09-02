from flask import Flask
from flask_socketio import SocketIO
from app.view import routes


app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is secret!'
socketio = SocketIO(app)

routes.create_endpoints(app, socketio)

#app.run(host='0.0.0.0',port=80,debug=True)
socketio.run(app, host='0.0.0.0', port=80, debug=True)
