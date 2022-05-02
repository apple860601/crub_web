import os
import click
from .app import create_app,db
from .app.model import User,Role,Shop,Itemname,Price,Permission
from flask_migrate import Migrate, migrate

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate=Migrate(app,db)
# shopee=Shop(shop="shopee",URLform="https://shopee.tw/product/",IURLform="https://cf.shopee.tw/file/")
# PChome=Shop(shop="PChome",URLform="http://24h.pchome.com.tw/prod/",IURLform="https://e.ecimg.tw")
# ruten=Shop(shop="ruten",URLform="https://goods.ruten.com.tw/item/show?",IURLform="https://img.ruten.com.tw/")
# Administrator=Role(permissions=Permission.ADMIN,name="admin")
# moderate=Role(permissions=Permission.MODERATE,name="moderate")
# users=Role(permissions=Permission.WRITE,name="user")
# db.session.add_all([shopee,PChome,ruten,Administrator,moderate,users])
# db.session.commit()

# admin=User(name=os.environ.get("ADMIN_NAME"),
#         email=os.environ.get("FLASKY_ADMIN"),
#         password=os.environ.get("ADMIN_PASSWORD"),
#         location=os.environ.get("ADMIN_LOCATION"),
#         confirm=True,
#         role_id=Administrator
#         )
# db.session.add(admin)
# db.session.commit()

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