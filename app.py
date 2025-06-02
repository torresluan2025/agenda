from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key' # Replace with a real secret key in production
db = SQLAlchemy(app)

def init_db():
    with app.app_context():
        db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=True)
    owner_name = db.Column(db.String(100), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # Will store as plain text initially
    domain = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'register_submit' in request.form:
            company_name = request.form.get('company_name')
            owner_name = request.form.get('owner_name')
            telephone = request.form.get('telephone')
            username = request.form.get('username')
            password = request.form.get('password') # Store plain text for now
            domain = request.form.get('domain')

            # Basic validation
            if not username or not password or not domain:
                flash('Username, password, and domain are required for registration.', 'danger')
                return redirect(url_for('home'))

            # Check if username or domain already exists
            existing_user_username = User.query.filter_by(username=username).first()
            existing_user_domain = User.query.filter_by(domain=domain).first()

            if existing_user_username:
                flash('Username already exists. Please choose a different one.', 'warning')
                return redirect(url_for('home'))
            
            if existing_user_domain:
                flash('Domain already registered. Please choose a different one.', 'warning')
                return redirect(url_for('home'))

            new_user = User(
                company_name=company_name,
                owner_name=owner_name,
                telephone=telephone,
                username=username,
                password=password, # In a real app, HASH THIS PASSWORD!
                domain=domain
            )
            db.session.add(new_user)
            try:
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('home')) 
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred during registration: {e}', 'danger')
                return redirect(url_for('home'))
        elif 'login_submit' in request.form:
            username = request.form.get('username')
            password = request.form.get('password') # Plain text for now

            if not username or not password:
                flash('Username and password are required for login.', 'danger')
                return redirect(url_for('home'))

            user = User.query.filter_by(username=username).first()

            if user and user.password == password: # In a real app, compare HASHED passwords!
                flash(f'Welcome back, {user.username}!', 'success')
                # For now, just redirect to home. Later, this could be a user dashboard.
                # Session management (e.g., flask_login) would go here.
                return redirect(url_for('home'))
            else:
                flash('Login unsuccessful. Please check username and password.', 'danger')
                return redirect(url_for('home'))
        
    return render_template('index.html')

if __name__ == '__main__':
    # If 'init-db' is passed as a command-line argument, initialize the DB
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        init_db()
        print("Database initialized.")
    else:
        # Otherwise, run the development server as usual
        app.run(debug=True)
