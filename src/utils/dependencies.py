from typing import Annotated

from .unitofwork import IUnitOfWork, UnitOfWork

IOWDep: Annotated[IUnitOfWork, UnitOfWork]
