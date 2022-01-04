from hashlib import md5

import jwt
from flask import url_for, current_app
from datetime import datetime, timedelta
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    task_post = db.relationship(
        "Task",  # 映射表格
        backref="task_author"  # 自定义名称
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        '''头像'''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'location': self.location,
            'about_me': self.about_me,
            'member_since': self.member_since.isoformat() + 'Z',
            'last_seen': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'name', 'location', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def get_jwt(self, expires_in=3600):
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'name': self.name if self.name else self.username,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError as e:
            return None
        return User.query.get(payload.get('user_id'))


class Task(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(64), index=True)
    discription = db.Column(db.Text())
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    finish_time = db.Column(db.DateTime(), default=datetime.utcnow)
    IsFinished = db.Column(db.Boolean, default=False)
    img_member = db.relationship(
        "Image",  # 映射表格
        backref="in_task"  # 自定义名称
    )

    def __repr__(self):
        return '<Task {}>'.format(self.title)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'creator_id': self.creator_id,
            'title': self.title,
            'discription': self.discription,
            'create_time': self.create_time.isoformat() + 'Z',
            'finish_time': self.finish_time.isoformat() + 'Z',
            'IsFinished': self.IsFinished,
        }
        return data

    def from_dict(self, data, author, new_task=False):
        for field in ['title', 'discription']:
            if field in data:
                setattr(self, field, data[field])
        setattr(self, 'creator_id', author)


class Imagetotag(db.Model):
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    tag_count = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.String(20))
    x1 = db.Column(db.String(20))
    y = db.Column(db.String(20))
    y1 = db.Column(db.String(20))
    image = db.relationship("Image", back_populates="tags")
    tag = db.relationship("Tag", back_populates="images")

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250), index=True, unique=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    tags = db.relationship("Imagetotag", back_populates="image")
    def __repr__(self):
        return '<Task {}>'.format(self.address)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), index=True, unique=True)
    uuid = db.Column(db.String(50), unique=True)
    images = db.relationship("Imagetotag", back_populates="tag")
    def __repr__(self):
        return '<Tag {}>'.format(self.tag)

    def to_dict(self):
        data = {
            'id': self.id,
            'tag_name': self.tag_name,
            'uuid': self.uuid
        }
        return data
