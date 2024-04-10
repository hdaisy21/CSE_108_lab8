from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
#from models import User, Admins, teacher, enrolled, classes


app = Flask(__name__)
CORS(app)



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

@app.route('/student/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify(error="User not found"), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="User deleted successfully"), 200

@app.route('/teacher/<id>', methods=['DELETE'])
def delete_teacher(id):
    teacher = teacher.query.get(id)
    if not teacher:
        return jsonify(error="User not found"), 404
    
    db.session.delete(teacher)
    db.session.commit()
    return jsonify(message="teacher deleted successfully"), 200

@app.route('/admins/<id>', methods=['DELETE'])
def delete_Admin(id):
    admins= Admins.query.get(id)
    if not admins:
        return jsonify(error="Admin not found"), 404
    
    db.session.delete(admins)
    db.session.commit()
    return jsonify(message="Admin deleted successfully"), 200

def is_logged_in():
    return current_user.is_authenticated

#student
@app.route('/user/<id>/courses', methods=['GET'])
def get_user_courses(id):
    user = User.query.get(id)
    if not user:
        return jsonify(error="User not found"), 404
    user_courses = [course.name for course in user.enrolled_courses]
    return jsonify(courses=user_courses), 200

@app.route('/classes', methods=['GET'])
def get_all_classes():
    all_classes = classes.query.all()
    class_list = [{'name': cls.name, 'teacher': cls.teacher_name, 'capacity': cls.capacity, 'students_enrolled': len(cls.students)} for cls in all_classes]
    return jsonify(classes=class_list), 200

@app.route('/available_classes', methods=['GET'])
def get_available_classes():
    all_classes = classes.query.all()
    available_classes = [{'name': cls.name, 'teacher': cls.teacher_name, 'capacity': cls.capacity, 'students_enrolled': len(cls.students)} for cls in all_classes if len(cls.students) < cls.capacity]
    return jsonify(classes=available_classes), 200



# Add route to remove a user from a class
@app.route('/unenroll', methods=['POST'])
@login_required
def unenroll_from_class():
    if not is_logged_in():
        return jsonify(error="You must be logged in to access this resource"), 401
    
    data = request.json
    class_name = data.get('class_name')

    # Check if the class exists
    cls = classes.query.filter_by(name=class_name).first()
    if not cls:
        return jsonify(error="Class not found"), 404
    
    # Check if the user is enrolled in the class
    if cls in current_user.enrolled_courses:
        # Remove the user from the class
        current_user.enrolled_courses.remove(cls)
        db.session.commit()
        return jsonify(message="Successfully unenrolled from class"), 200
    else:
        return jsonify(error="You are not enrolled in this class"), 400

#teacher
@app.route('/my_courses', methods=['GET'])
@login_required
def get_teacher_courses():
    if not is_logged_in():
        return jsonify(error="You must be logged in to access this resource"), 401
    
    if current_user.role != 'teacher':
        return jsonify(error="You must be a teacher to access this resource"), 403
    
    teacher_courses = [{'name': cls.name, 'capacity': cls.capacity, 'students_enrolled': len(cls.students)} for cls in current_user.class_relation]
    return jsonify(courses=teacher_courses), 200


@app.route('/enroll', methods=['POST'])
@login_required
def enroll_in_class():
    if not is_logged_in():
        return jsonify(error="You must be logged in to access this resource"), 401
    
    data = request.json
    class_name = data.get('class_name')

    # Check if the class exists
    cls = classes.query.filter_by(name=class_name).first()
    if not cls:
        return jsonify(error="Class not found"), 404
    
    # Check if the class has reached capacity
    if len(cls.students) >= cls.capacity:
        return jsonify(error="Class has reached its capacity"), 400
    
    # Enroll the user in the class
    current_user.enrolled_courses.append(cls)
    db.session.commit()
    return jsonify(message="Successfully enrolled in class"), 200
    

# Create the database tables
with app.app_context():
    db.create_all()

#Initialize Flask-Admin
admin = Admin(app)

# Register views for your models with Flask-Admin
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Admins, db.session))
admin.add_view(ModelView(teacher, db.session))
admin.add_view(ModelView(enrolled, db.session))
admin.add_view(ModelView(classes, db.session))  

# @app.route('/admin')
# def admin():

#     return render_template('admin_dashboard.html')


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