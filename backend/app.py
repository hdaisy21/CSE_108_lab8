from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Users{self.username}>'


# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/')
def welcome():
    return "Welcome to my backend on Flask!"

@app.route('/users', methods=['GET'])
def list_users():
    users = Users.query.all()
    user_list = [{'username': user.username} for user in users]
    return jsonify(users=user_list)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(error="Both username and password are required"), 400

    user = Users.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify(message="Login successful"), 200
    else:
        return jsonify(error="Invalid username or password"), 401

@app.route('/user', methods=['POST'])
def submit():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(error="Both username and password are required"), 400

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(error="Username already exists"), 409

    new_user = Users(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify("User successfully registered"), 200


if __name__ == '__main__':
    app.run()