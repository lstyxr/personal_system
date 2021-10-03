from datetime import datetime
from flask_whooshee import Whooshee

from sqlalchemy.orm import backref

# 注意以下都是从自己系统中导入的
from mysystem import db
from mysystem import whooshee

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

# 1. 用户表
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    hash_password = db.Column(db.String(120), nullable=False)
    plans = db.relationship("Plan", backref="user", lazy="dynamic")  # 与 Plan 类建立关联

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

# 2.总计划表
@whooshee.register_model('body')
class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    create_at = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 与用户 user.id 约束
    sub_plans = db.relationship("SubPlan", backref="plan", lazy="dynamic")  # 与子计划类 SubPlan 建立关联


# 3.子计划表
class SubPlan(db.Model):
    __tablename__ = 'sub_plan'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.now)
    finish_time = db.Column(db.DateTime, default=datetime.now)
    is_done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 与用户 user.id 约束
    plan_id = db.Column(db.Integer, db.ForeignKey("plan.id"))  # 与总计划 plan.id 约束

    def change_status(self):
        if self.is_done is True:
            self.is_done = False
        else:
            self.is_done = True
        self.finish_time = datetime.now()
        db.session.add(self)
        db.session.commit()