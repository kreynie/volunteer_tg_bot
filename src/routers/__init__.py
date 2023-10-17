from .admin import router as admin_router
from .echo import router as echo_router
from .event import router as event_router
from .help import router as help_router
from .start import router as start_router
from .utils import router as utils_router

all_routers = [
                  admin_router,
                  event_router,
                  help_router,
                  start_router,
                  utils_router,
              ] + [echo_router]

__all__ = ("all_routers",)
