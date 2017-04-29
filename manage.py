#coding:utf-8
import os
import sys
reload(sys)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "libs"))
from app import create_app,db

from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

def make_shell_context():
    #使用shell命令时，存在的上下文数据
    return dict(app=app, db = db)

manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()

