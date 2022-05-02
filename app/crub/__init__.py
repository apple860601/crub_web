from ..model import Permission
from flask import Blueprint
crub=Blueprint('crub',__name__)
from . import views,errors

@crub.app_context_processor
def inject_permission():
    return dict(Permission=Permission)