from .admin import bp as admin_bp
from .auth import bp as auth_bp
from .public import bp as public_bp
__all__ = ["admin_bp", "auth_bp", "public_bp"]