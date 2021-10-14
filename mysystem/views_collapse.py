from mysystem import db
from flask.helpers import url_for
from werkzeug.utils import redirect
# from mysystem.models import User
# from mysystem.models import Todo

# 模型 models 要改成需要的，db.create_all()才能自动创建其中的表
# 本工程是用 commands.py 模块中用户注册函数包含的 db.create_all() 功能，所有 commands.py 模块中的 import 也要改一下
from mysystem.models01 import User
from mysystem.models01 import Plan
from mysystem.models01 import SubPlan
import sys
from flask import render_template, session, request
from mysystem import app  # 这个下划线错误提示不用管
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, length
from flask_login import login_user, logout_user, current_user, login_required
from mysystem import login_manager

plan_add = ""

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(6, 100)])
    remember_pwd = BooleanField('remember')
    login = SubmitField('login')

class TodoForm(FlaskForm):
    body = StringField('body', validators=[DataRequired(), Length(5, 100)])
    # bodys = StringField('bodys', validators=[DataRequired(), Length(5, 100)])
    submit = SubmitField('submit')

# # 子计划追加窗体
# class SubTodoForm(FlaskForm):
#     body = StringField('body', validators=[DataRequired(), Length(5, 100)])
#     submit = SubmitField('submit')

# 加载当前用户
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@app.route('/login', methods=['GET'])
def login():
    login_form = LoginForm()  # 实例登录窗体
    # 将表单实例返回给前端，表单名叫:form，可以取其它名，但要与 login.html 文件一致
    return render_template('login.html', form=login_form)

@app.route('/userlogin', methods=['POST'])
def userlogin():
    login_form = LoginForm()
    if login_form.validate_on_submit():  # 判断前端校验，如密码长度，用户名不为空等
        # 传过来的账号密码
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        # return render_template('index.html', title='个人娱乐系统！', username=username)
        if user:
            if username == user.username and user.check_password(password):
                # 登录成功
                session['user_id'] = user.id
                # 判断是否记住密码
                remember_pwd = login_form.remember_pwd.data
                if remember_pwd:
                    login_user(user, remember=True)
                else:
                    login_user(user)
                return render_template('index.html', title='个人娱乐系统！', username=username)
            else:
                # 用户名或密码不正确
                return render_template('login.html', form=login_form, errormsg='用户名或密码不正确!')
        else:
            return render_template('login.html', form=login_form, errormsg='用户不存在!')

@app.route('/logout', methods=['GET'])
def logout():
    # del session['user_id']
    logout_user()
    return redirect(url_for('login'))

@app.route('/todolist/<int:is_done>/', methods=['GET', 'POST'])
@login_required
def todo_list(is_done):
    user = User.query.filter_by(id=session['user_id']).first_or_404()
    user = current_user
    page_num = 6
    page = request.args.get('page', 1, type=int)
    # pagination = SubPlan.query.with_parent(user).paginate(page, per_page=page_num)
    plan = Plan.query.with_parent(user)
    subplans = SubPlan.query.with_parent(plan)
    # todos = pagination.items
    # todos = SubPlan.query

    todo_form = TodoForm()
    # sub_todo = SubTodoForm()
    return render_template('views_collapse.html', sub_plans=subplans, is_done=is_done, todo=plan, form=todo_form)

@app.route('/todo/add/<int:plan_id>', methods=['POST'])
@login_required
def add_todo(plan_id):
    body = request.form.get('todo')
    user_id = current_user.get_id()
    sub_plan = SubPlan(body=body, user_id=user_id, plan_id=plan_id)
    db.session.add(sub_plan)
    db.session.commit()
    todo_id = sub_plan.plan_id
    return f"""
                <div class="card-body border border-light">
                    <p class="card-text d-inline">{body}</p>
                    <input type="checkbox" data-todo-id="{todo_id}" value="{plan_id}" class="btn-check d-inline float-right"
                                                                                autocomplete="off">
                </div>
        
    """

@app.route('/collapsetest', methods=['GET'])
def todo_list_test():
    todo = Plan.query
    subplans = SubPlan.query
    todo_form = TodoForm()  # 实例窗体
    return render_template('todolist_collapse02.html', sub_plans=subplans, todos=todo, form=todo_form)

# 新增任务路由
@app.route('/todoadd', methods=['GET', 'POST'])
@login_required
def todo_add():
    todo_form = TodoForm()
    return render_template('addplan.html', form=todo_form, forms=todo_form)

# 在前端窗体中绑定这个路由<form action="/todolist/add" method="POST"> ... </form>
# @app.route('/todolist/add', methods=['POST'])
# def add_todo():
#     todo_form = TodoForm()  # 实例窗体    
#     plan = Plan(body=todo_form.body.data, user_id=session['user_id'])  # 进而获得用户窗体中输入的数据存入数据库
#     db.session.add(plan)
#     db.session.commit()
#     global plan_add
#     plan_add = Plan.query.filter_by(body=todo_form.body.data).first_or_404()
#     return todo_add()

# 创建子计划
@app.route('/todolist/adds', methods=['POST'])
def add_todos():
    todo_form = TodoForm()  # 实例窗体
    subP = SubPlan(body=todo_form.body.data, user_id=session['user_id'], plan_id=plan_add.id)
    db.session.add(subP)
    db.session.commit()
    return todo_add()

@app.route('/api/todo/<int:todo_id>/', methods=['POST'])
def change_todo(todo_id):
    todo = SubPlan.query.get_or_404(todo_id)
    todo.change_status()
    return '{"status": 200}'

@app.route('/search')
def search():
    user = User.query.filter_by(id=session['user_id']).first_or_404()
    try:
        s = request.args.get('s')
        page = request.args.get('page', 1, type=int)
        page_num = 5

        pagination = Plan.query.with_parent(user)\
            .whooshee_search(s).\
                filter_by(is_done=0).\
                    paginate(page, per_page=page_num)
    except:
        pagination = Plan.query.with_parent(user).\
                paginate(page, per_page=page_num)

    todos = pagination.items
    todo_form = TodoForm()
    return render_template('todolist.html', form=todo_form, pagination=pagination, todolist=todos, is_done=0)

@app.route('/')
def test():
    return render_template('test1.html')

if __name__ == "__main__":
    app.run(debug=True)