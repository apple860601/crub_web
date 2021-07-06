import os
import click
from .app import create_app,db
from .app.model import User,Role,Shop,Itemname,Price
from flask_migrate import Migrate, migrate

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate=Migrate(app,db)
# db.create_all()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role,Shop=Shop,Itemname=Itemname,Price=Price)

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
    db.create_all()
    app.run()