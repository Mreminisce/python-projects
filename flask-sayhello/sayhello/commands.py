import click

from sayhello import app, db
from sayhello.models import Message


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages, default is 20.')
def forge(count):
    from faker import Faker  # 导入 Faker 库，可以自动生成虚拟数据

    db.drop_all()
    db.create_all()

    fake = Faker()           # 实例化 Faker 库，可以传入 'zh_CN' 等参数
    click.echo('Working...') # 在命令行中返回的字符串

    for i in range(count):
        message = Message(
            name=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(message)

    db.session.commit()
    click.echo('Created %d fake messages.' % count)
