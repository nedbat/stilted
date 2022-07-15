"""Built-in stack operators for stilted."""

from estate import builtin, builtin_with_name, ExecState


@builtin
def copy(estate: ExecState) -> None:
    if isinstance(estate.ostack[-1], int):
        n, = estate.opop(1)
        if n:
            estate.ostack.extend(estate.ostack[-n:])

@builtin_with_name("def")
def def_(estate: ExecState) -> None:
    name, val = estate.opop(2)
    estate.dstack[name.name] = val

@builtin
def dup(estate: ExecState) -> None:
    estate.ostack.append(estate.ostack[-1])

@builtin
def exch(estate: ExecState) -> None:
    a, b = estate.opop(2)
    estate.ostack.append(b)
    estate.ostack.append(a)

@builtin
def index(estate: ExecState) -> None:
    n, = estate.opop(1)
    estate.ostack.append(estate.ostack[-(n + 1)])

@builtin
def pop(estate: ExecState) -> None:
    estate.opop(1)

@builtin
def roll(estate: ExecState) -> None:
    n, j = estate.opop(2)
    vals = estate.opop(n)
    vals = vals[-j:] + vals[:-j]
    estate.ostack.extend(vals)
