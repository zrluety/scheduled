import click

from scheduled import main


@click.command()
@click.argument("profile")
@click.argument("src")
@click.argument("dst")
def cli(profile, src, dst):
    main.run(profile, src, dst)


# @click.command()
# @click.option('-d', '--debug', is_flag=True, default=False, help="Run program in debug mode")
# @click.argument('src')
# @click.argument('profile')
# @click.argument('scheduled')
# @click.argument('dst')
# @click.argument('user')
# def run_app(debug, src, profile, scheduled, dst, user):
#     session = Session(src, profile, scheduled, dst, user, debug)
#     session.run()
