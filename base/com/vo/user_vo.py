from base import db, app
from datetime import datetime


class UserVO(db.Model):
    __tablename__ = 'login'

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255), nullable=False)
    password = db.Column('password', db.String(255), nullable=False)
    role = db.Column('role', db.String(255), nullable=False, default='admin')
    is_deleted = db.Column('is_deleted', db.Boolean, nullable=False, default=False)
    created_on = db.Column('created_at', db.String(255), nullable=False)
    updated_on = db.Column('updated_at', db.String(255), nullable=False)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'is_deleted': self.is_deleted,
            'created_on': self.created_on,
            'updated_on': self.updated_on
        }

    @staticmethod
    def get(user_id):
        return UserVO(user_id)

    def get_id(self):
        return str(self.user_id)


with app.app_context():
    db.create_all()