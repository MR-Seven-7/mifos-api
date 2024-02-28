from flask import Flask, request, jsonify, session
from models import User, db, LogEntry
from config import Config
from flask_cors import CORS
import google.generativeai as genai


genai.configure(api_key='AIzaSyBaafmbVClFxg_PED6sIV_gSKiioYDZPYU')

ai = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

app.secret_key = 'secret_key'

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401

        session['user_id'] = user.id
        return jsonify({'message': 'Login successful!'}), 200

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return jsonify({'error': 'Email already exists'}), 400

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registration successful!'}), 201

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/prompt', methods=['GET'])
def prompt():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        prompt = request.form['prompt']
        response = ai.generate_content(prompt)
        log_entry = LogEntry(prompt=prompt, response=response.text, user_id=session['user_id'])
        db.session.add(log_entry)
        db.session.commit()
        return jsonify({'response': response.text, "id":session['user_id']})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
