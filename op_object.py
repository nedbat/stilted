"""Built-in object model operators for stilted."""

from estate import operator, ExecState
from dtypes import from_py, Name

@operator
def cvlit(estate: ExecState) -> None:
    estate.ohas(1)
    estate.ostack[-1].literal = True

@operator
def cvx(estate: ExecState) -> None:
    estate.ohas(1)
    estate.ostack[-1].literal = False

@operator("type")
def type_(estate: ExecState) -> None:
    obj = estate.opop()
    estate.opush(Name(literal=False, value=obj.typename + "type"))

@operator
def xcheck(estate: ExecState) -> None:
    obj = estate.opop()
    estate.opush(from_py(not obj.literal))
