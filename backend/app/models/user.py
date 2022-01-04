from flask import url_for

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import PaginatedAPIMixin

class User(PaginatedAPIMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键
    id = db.Column(db.Integer, doc='手机号码', primary_key=True)
    username = db.Column(db.String(64), doc='昵称', index=True, default='Wanted User', nullable=False, unique=True)
    email = db.Column(db.String(120), doc='email', index=True, unique=True)
    password_hash = db.Column(db.String(128), doc='密码', nullable=False)  # 不保存原始密码

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data


    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])