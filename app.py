from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__, template_folder='templates', static_folder="static")
CORS(app)

admin = Admin(app)


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
    
class adminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    username = db.Column(db.String(100), nullable=False) 
    password = db.Column(db.String(100), nullable=False) 
    role = db.Column(db.String(100), nullable=False) 
    
    
class teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False) 
    role = db.Column(db.String(100), nullable=False) 

# class enrolled(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(100), db.ForeignKey('users.username'))  # Define foreign key relationship
#     class_name = db.Column(db.String(100), db.ForeignKey('classes.name'))
#     grade = db.Column(db.Float)

# class classes(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
#     teacher_name = db.Column(db.String(100), nullable=False)
#     enroll = db.relationship('enrolled', backref='classes', lazy=True)
#     capacity = db.Column(db.Integer)

    

# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/')
def welcome():
    return render_template("login.html")

    
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
            return jsonify(role=user.role)
    else:
        return jsonify(error="Invalid username or password"), 401
    

# @app.route('/admin/dashboard', methods=['GET'])
# def admin_dashboard():
#     if current_user.role == 'admin':
#         return render_template('admin_dashboard.html')
#     else:
#         return redirect(url_for('login'))

# @app.route('/teacher/dashboard', methods=['GET'])
# @login_required
# def teacher_dashboard():
#     if current_user.role == 'teacher':
#         return render_template('teacher_dashboard.html')
#     else:
#         return redirect(url_for('login'))

# @app.route('/student/dashboard', methods=['GET'])
# @login_required
# def student_dashboard():
#     if current_user.role == 'student':
#         return render_template('student_dashboard.html')
#     else:
#         return redirect(url_for('login'))



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


#admin page stuff
#uses admin.html

@app.route('/admin')
def admin():

    return render_template("admin.html")


if __name__ == '__main__':
    app.run()
