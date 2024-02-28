from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')  # Convert password to bytes
        self.password_hash = bcrypt.hashpw(password_bytes, self.password_hash)


    def check_password(self, password):
        password_bytes = password.encode('utf-8')  # Convert password to bytes
        return bcrypt.checkpw(password_bytes, self.password_hash)


    def __repr__(self):
        return f'<User {self.email}>'


class LogEntry(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    prompt = db.Column(db.String)
    response = db.Column(db.String)