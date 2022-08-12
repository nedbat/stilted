"""Built-in miscellaneous operators for Stilted."""

import time

from dtypes import from_py
from evaluate import operator, Engine


@operator
def usertime(engine: Engine) -> None:
    engine.opush(from_py(int(time.process_time() * 1000)))
