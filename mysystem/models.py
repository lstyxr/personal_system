from datetime import datetime
from flask_whooshee import Whooshee

from sqlalchemy.orm import backref

# 注意以下都是从自己系统中导入的
from mysystem import db
from mysystem import whooshee

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'my_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    admin_password = db.Column(db.String(120), nullable=False)
    todos = db.relationship("Todo", backref='my_user')  # 与 Todo 类建立关联

    def set_password(self, password):
        self.admin_password = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.admin_password, password)

@whooshee.register_model('description')
class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    is_done = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    done_time = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('my_user.id'))  # 添加用户ID关联

    # 改变任务状态：未完成 --> 完成状态
    def change_status(self):
        if self.is_done is True:
            self.is_done = False
        else:
            self.is_done = True
        self.done_time = datetime.now()
        db.session.add(self)
        db.session.commit()