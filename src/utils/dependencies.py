from typing import Annotated

from .unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, UnitOfWork]
