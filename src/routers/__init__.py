from .admin import router as admin_router
from .unknown import router as echo_router
from .shift import router as event_router
from .info import router as info_router
from .start import router as start_router
from .utils import router as utils_router

all_routers = [
                  admin_router,
                  event_router,
                  info_router,
                  start_router,
                  utils_router,
              ] + [echo_router]

__all__ = ("all_routers",)
