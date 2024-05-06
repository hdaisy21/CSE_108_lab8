from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import secrets


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    username = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False) 
    salt = db.Column(db.String(32), nullable=False) 
    
    def __repr__(self):
        return '<User %r>' % self.username



# Create the application context
with app.app_context():
    # Create all tables
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route to handle login
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
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password + user.salt):
            login_user(user)
            return jsonify(name=user.name)
    else:
        return jsonify(error="Invalid username or password"), 401
    


# Route to handle logout
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
    
    
    if not username or not password or not name:
        return jsonify(error="Name, username, and password are required"), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(error="Username already exists"), 409

    salt = secrets.token_hex(16)  # Generate a random salt
    hash = generate_password_hash(password + salt)  # Hash password with salt
    new_user = User(name=name, username=username, password=hash, salt=salt)  # Store salt in the database
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User successfully registered"), 200

@app.route('/protected')
@login_required
def protected_route():
    return jsonify(message="You've accessed the protected route!")


if __name__ == '__main__':
   app.run(debug=True)



