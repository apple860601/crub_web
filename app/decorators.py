from functools import wraps
from flask import abort
from flask_login import current_user
from .model import Permission

def permission_required(permission):
    #檢查權限用的裝飾器
    def decorator(f):
        @wraps(f)
        def decorator_function(*args,**kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kwargs)
        return decorator_function
    return decorator

def admin_required(f):
    #檢查使用者是否為管理者
    return permission_required(Permission.ADMIN)(f)