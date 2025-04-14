import os
import json
import logging
import subprocess
import tempfile
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///pythonlearning.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with app
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after db initialization to avoid circular imports
from models import User, UserProgress

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables within app context
with app.app_context():
    db.create_all()

# Helper function to load lesson content
def load_lesson(lesson_name):
    try:
        with open(f'lessons/{lesson_name}.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading lesson {lesson_name}: {e}")
        return None

# Routes
@app.route('/')
def home():
    topics = [
        {"id": "syntax", "title": "Python Syntax", "description": "Learn the basic syntax of Python programming language."},
        {"id": "data_types", "title": "Data Types", "description": "Explore Python's built-in data types like strings, numbers, lists, and dictionaries."},
        {"id": "loops", "title": "Loops", "description": "Master the art of repetition with for and while loops."},
        {"id": "functions", "title": "Functions", "description": "Learn how to create reusable blocks of code with functions."}
    ]
    
    if current_user.is_authenticated:
        # Get user progress
        user_progress = UserProgress.query.filter_by(user_id=current_user.id).all()
        completed_lessons = {progress.lesson_id for progress in user_progress}
    else:
        completed_lessons = set()
    
    return render_template('home.html', topics=topics, completed_lessons=completed_lessons)

@app.route('/lesson/<lesson_id>')
def lesson(lesson_id):
    lesson_data = load_lesson(lesson_id)
    if not lesson_data:
        flash('Lesson not found!', 'danger')
        return redirect(url_for('home'))
    
    # Check if the user has completed this lesson
    completed = False
    if current_user.is_authenticated:
        progress = UserProgress.query.filter_by(
            user_id=current_user.id, 
            lesson_id=lesson_id
        ).first()
        completed = bool(progress)
    
    return render_template('lesson.html', 
                          lesson=lesson_data, 
                          lesson_id=lesson_id,
                          completed=completed)

@app.route('/practice/<lesson_id>')
def practice(lesson_id):
    lesson_data = load_lesson(lesson_id)
    if not lesson_data:
        flash('Lesson not found!', 'danger')
        return redirect(url_for('home'))
    
    return render_template('practice.html', 
                          lesson=lesson_data, 
                          lesson_id=lesson_id)

@app.route('/execute_code', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp_path = temp.name
            temp.write(code.encode('utf-8'))
        
        # Execute the code in a subprocess with timeout
        result = subprocess.run(
            ['python', temp_path], 
            capture_output=True, 
            text=True, 
            timeout=5  # 5 second timeout for safety
        )
        
        # Clean up the temp file
        os.unlink(temp_path)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr
            })
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Execution timed out. Your code took too long to run.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/verify_exercise', methods=['POST'])
def verify_exercise():
    code = request.form.get('code', '')
    lesson_id = request.form.get('lesson_id', '')
    exercise_id = request.form.get('exercise_id', '')
    
    lesson_data = load_lesson(lesson_id)
    if not lesson_data:
        return jsonify({
            'success': False,
            'error': 'Lesson not found'
        })
    
    # Find the exercise
    exercise = None
    for ex in lesson_data.get('exercises', []):
        if ex.get('id') == exercise_id:
            exercise = ex
            break
    
    if not exercise:
        return jsonify({
            'success': False,
            'error': 'Exercise not found'
        })
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
        temp_path = temp.name
        # Write user code
        temp.write(code.encode('utf-8'))
        # Write test code from exercise
        test_code = exercise.get('test_code', '')
        if test_code:
            temp.write(f"\n\n# Test code\n{test_code}".encode('utf-8'))
    
    try:
        # Execute the code with test
        result = subprocess.run(
            ['python', temp_path], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        # Clean up
        os.unlink(temp_path)
        
        if result.returncode == 0:
            # Mark lesson as completed for the user
            if current_user.is_authenticated:
                # Check if progress already exists
                progress = UserProgress.query.filter_by(
                    user_id=current_user.id, 
                    lesson_id=lesson_id
                ).first()
                
                if not progress:
                    progress = UserProgress(
                        user_id=current_user.id,
                        lesson_id=lesson_id,
                        completed=True
                    )
                    db.session.add(progress)
                    db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Great job! Exercise completed successfully.',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Test failed: {result.stderr}'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/mark_completed/<lesson_id>', methods=['POST'])
@login_required
def mark_completed(lesson_id):
    # Check if progress already exists
    progress = UserProgress.query.filter_by(
        user_id=current_user.id, 
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            completed=True
        )
        db.session.add(progress)
        db.session.commit()
        flash('Lesson marked as completed!', 'success')
    else:
        flash('Lesson already completed!', 'info')
    
    return redirect(url_for('lesson', lesson_id=lesson_id))

@app.route('/profile')
@login_required
def profile():
    topics = [
        {"id": "syntax", "title": "Python Syntax"},
        {"id": "data_types", "title": "Data Types"},
        {"id": "loops", "title": "Loops"},
        {"id": "functions", "title": "Functions"}
    ]
    
    # Get user progress
    user_progress = UserProgress.query.filter_by(user_id=current_user.id).all()
    completed_lessons = {progress.lesson_id for progress in user_progress}
    
    # Calculate progress percentage
    total_lessons = len(topics)
    completed_count = len(completed_lessons)
    progress_percentage = (completed_count / total_lessons) * 100 if total_lessons > 0 else 0
    
    return render_template('profile.html', 
                          user=current_user, 
                          topics=topics,
                          completed_lessons=completed_lessons,
                          progress_percentage=progress_percentage)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return render_template('register.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
