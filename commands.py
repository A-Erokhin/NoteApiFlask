import click
from api import app, db
from api.models.user import UserModel


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:")
    if username == '':
        username = 'admin'
    password = input("Password[default 'admin']:")
    if password == '':
        password = 'admin'
    user = UserModel(username, password, role="admin", is_staff=True)
    user.save()
    if not user.id:
        ("Enter unique username")
    else:
        print(f"Superuser create successful! id={user.id}")


@app.cli.command('printuserslist')
def print_users_list():
    """
    Print all users
    """
    users = UserModel.query.all()
    for num, user in enumerate(users, 1):
        print(f"{num}. User id: {user.id} {user.username}")


@app.cli.command('my-command')
@click.argument('param')
def my_command(param):
    """
    Demo command with param
    """
    print(f"Run my_command with param {param}")



@app.cli.command('remove-user')
@click.argument('username', default="")
@click.option("--all", default=False, is_flag=True)
def remove_user(username, all):

    if all:
        UserModel.query.delete()
        db.session.commit()
        return

    ...

    # username = input("Username: ")
    # user = UserModel.query.get(username)
    # if not user:
    #     print(f"User {username} not found")
    # else:
    #     user.delete()
    #     print(f"User {username} deleted successful!")
