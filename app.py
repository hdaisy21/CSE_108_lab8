from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
CORS(app)

# admin = Admin(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    username = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False)  
    role = db.Column(db.String(100), nullable=False) 
    enrolled = db.relationship('enrolled', backref='User', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.username
    


class Admins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) 
    username = db.Column(db.String(100), nullable=False) 
    password = db.Column(db.String(100), nullable=False) 
    role = db.Column(db.String(100), nullable=False) 
    


class teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False) 
    role = db.Column(db.String(100), nullable=False)
    class_relation = db.relationship('classes', backref='teacher', lazy=True) 

class enrolled(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('user.username'))  # Corrected ForeignKey definition
    class_name = db.Column(db.String(100), db.ForeignKey('classes.name'))
    grade = db.Column(db.Float)
    

class classes(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher_name = db.Column(db.String(100), nullable=False)
    enroll = db.relationship('enrolled', backref='classes', lazy=True)
    capacity = db.Column(db.Integer)

    

# Create the database tables
with app.app_context():
    db.create_all()




@app.route('/')
def welcome():
    return redirect(url_for('login'))
@app.route('/register')
def register():
    return render_template('createAccount.html')
    
@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    user_list = [{'username': users.username, 'password': users.password} for user in users]
    return jsonify(users=user_list)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html') 
    
    elif request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify(error="Both username and password are required"), 400
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            print(user.role)
            return jsonify(role=user.role, name=user.name)
    else:
        return jsonify(error="Invalid username or password"), 401
    


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('logout_confirmation'))


@app.route('/logout_confirmation', methods=['GET'])
def logout_confirmation():
    return "<h1>You have been logged out successfully.</h1>"




@app.route('/user', methods=['POST'])
def submit():
    data = request.json
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    if not username or not password or not name or not role:
        return jsonify(error="One or more entries are not completed"), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(error="Username already exists"), 409

    new_user = User(username=username, password=password, name=name, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User successfully registered"), 200


if __name__ == '__main__':
    app.run()
