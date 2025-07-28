from .posts import router as posts_router
from .users import router as users_router
from .auth import router as auth_router

__all__ = ["posts_router", "users_router", "auth_router"]