from exts import db
import apps
app = apps.create_app()

# 导入manager类
from flask_script import Manager,Server
# 导入数据库迁移类和数据库迁移指令类
from flask_migrate import Migrate
# 构建指令，设置当前Flask的app实例受指令控制（即将指令绑定给指定app实例）
manage = Manager(app)
manage.add_command('runserver', Server(user_debugger=True))
# 第1个参数时Flask实例， 第2个参数时Sqlalchemy数据库实例， 创建数据库迁移工具对象
migrate = Migrate(app, db, render_as_batch=True)


if __name__ == '__main__':
    manage.run()