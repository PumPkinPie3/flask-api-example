def cli_handler(app):
    import click
    from sqlalchemy import create_engine
    from app.models import Base

    @app.cli.command(short_help='Create database')
    def db_create():
        uri, dbname = app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)
        mysql_engine = create_engine(uri)
        mysql_engine.execute('CREATE DATABASE IF NOT EXISTS `{}`;'.format(dbname))
        click.echo('Create {} in {}'.format(dbname, uri.rsplit('@', 1)[1]))

    @app.cli.command(short_help='Initialize the database')
    def db_init():
        click.echo('Create tables in {}'.format(app.config['MYSQL_DATABASE']))
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        mysql_engine = create_engine(uri)
        Base.metadata.create_all(bind=mysql_engine)
