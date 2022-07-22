"""Built-in object model operators for stilted."""

from estate import operator, ExecState
from dtypes import from_py

@operator
def cvlit(estate: ExecState) -> None:
    estate.ohas(1)
    estate.ostack[-1].literal = True

@operator
def cvx(estate: ExecState) -> None:
    estate.ohas(1)
    estate.ostack[-1].literal = False

@operator
def xcheck(estate: ExecState) -> None:
    obj = estate.opop(1)[0]
    estate.opush(from_py(not obj.literal))
