import click
from click.termui import prompt
from mysystem import app, db
from mysystem.models01 import User

# 注册命令
@app.cli.command()
@click.option('--username', prompt=True)
@click.option('--password', hide_input=True, prompt=True)
def register(username, password):
    db.create_all()
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo('注册成功！')

# 登录命令
@app.cli.command()
@click.option('--username', prompt=True)
@click.option('--password', hide_input=True, prompt=True)
def login(username, password):
    user = User.query.first()
    if user:
        if username == user.username and user.check_password(password):
            click.echo('成功登录！')
        else:
            click.echo('用户名或密码错误！！！')