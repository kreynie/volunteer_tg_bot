from typing import TypeVar

from .unitofwork import IUnitOfWork

UOWDep = TypeVar("UOWDep", bound=IUnitOfWork)
