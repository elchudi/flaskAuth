from flask import Flask
from functools import wraps
from flask import request, Response
from flask import jsonify

app = Flask(__name__)

users = [
    {'id':'1', 'username':'juanle', 'password':'123456', 'platform':'Android', 'quality':'High', 'accessibility':'1', 'recommender':'auto'},
    {'id':'2', 'username':'user2', 'password':'123456', 'platform':'iOS', 'quality':'Low', 'accessibility':'1', 'recommender':'random'},
    {'id':'3', 'username':'user3', 'password':'123456', 'platform':'iOS', 'quality':'Low', 'accessibility':'0', 'recommender':'random'},
]

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    for user in users:
        print 'check'
        print username
        if user['username'] == username and user['password'] == password:
            return True
    return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        username = request.args.get('username', '')
        password = request.args.get('password', '')
        print 'requires'
        print username
        print password
        
        if not check_auth(username, password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/login')
@requires_auth
def login():
    username = request.args.get('username', '')
    for user in users:
        if user['username'] == username:
            return jsonify(user)
    return 'OK'

@app.route('/user/<user_id>')
def user(user_id):  
    for user in users:
        if user_id == user['id']:
            return jsonify(user)
    return 'Not Found'

@app.route('/update/<user_id>')
def update(user_id):  
    for user in users:
        if user_id == user['id']:
            platform = request.args.get('platform', '')
            accesibility = request.args.get('accesibility', '')
            quality = request.args.get('quality', '')
            recommender = request.args.get('recommender', '')
            user['platform'] = platform
            user['accesibility'] = accesibility
            user['quality'] = quality
            user['recommender'] = recommender
            return jsonify(user)
    return 'Not Found'

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
