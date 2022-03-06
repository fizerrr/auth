from functools import wraps
from flask import Flask, request,make_response,jsonify
import jwt
import datetime 

app = Flask(__name__)


app.config.update(
    TESTING=True,
    SECRET_KEY='U,+Hes3*F_D3*3c:#}?Y$SM:t$G!_G!gV)!A;mFX+c!>EuAF[T'
)

print(app.config['SECRET_KEY'])

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify(message='token is missing'), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
        except:
            return jsonify(message='token is invalid'), 403
        
        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected ')
def unproctected():
    return jsonify(message='unprotected')

@app.route('/protected ')
@token_required
def proctected():
    return jsonify(message='protected but you have permission')
    

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'admin' and auth.username == 'admin' :
        token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30) }, app.config['SECRET_KEY'],algorithm="HS256")
        return jsonify(token)
    return make_response('Could not verify',401, {'WWW-Authenticate' : 'Basic realm="Login Required'})



if __name__ == '__main__':
    app.run(debug=True)

