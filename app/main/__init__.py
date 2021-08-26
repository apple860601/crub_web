from ..model import Permission
from flask import Blueprint
main=Blueprint('main',__name__)
from . import views,errors

@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)