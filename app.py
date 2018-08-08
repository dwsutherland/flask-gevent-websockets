from gevent import monkey
monkey.patch_all()

import cgi
import redis
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['DEBUG'] = True
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/pymeetups/')
def pymeetups():
    return render_template('pymeetups.html')

@socketio.on('connect', namespace='/fgwebsockets')
def ws_conn():
    c = db.incr('user_count')
    socketio.emit('msg', {'count': c}, namespace="/fgwebsockets")

@socketio.on('disconnect', namespace='/fgwebsockets')
def ws_conn():
    c = db.decr('user_count')
    socketio.emit('msg', {'count': c}, namespace="/fgwebsockets")

@socketio.on('city', namespace='/fgwebsockets')
def ws_city(message):
    socketio.emit('city', {'city': cgi.escape(message['city'])},
                    namespace='/fgwebsockets')

if __name__ == '__main__':
    socketio.run(app)

