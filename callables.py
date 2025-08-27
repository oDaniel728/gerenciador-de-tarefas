import inspect
from random import randint
from typing import Any, Callable, Dict, Type, Union
import math

selfdef=Callable[[Any], Any]

add:    Callable[[Any], selfdef] = lambda x: lambda self: self +  x
sub:    Callable[[Any], selfdef] = lambda x: lambda self: self -  x
mul:    Callable[[Any], selfdef] = lambda x: lambda self: self *  x
div:    Callable[[Any], selfdef] = lambda x: lambda self: self /  x
mod:    Callable[[Any], selfdef] = lambda x: lambda self: self %  x
exp:    Callable[[Any], selfdef] = lambda x: lambda self: self ** x
sqrt:   Callable[[],    selfdef] = lambda: lambda self: math.sqrt(self)
intdiv: Callable[[Any], selfdef] = lambda x: lambda self: self // x

say:    Callable[[str], selfdef] = lambda message: lambda self: print(message) or self
run:    Callable[[str], selfdef] = lambda code: lambda self: exec(code, {**globals(), "self": self}, locals()) or self

randn: Callable[[int, int, Callable[[int, Any], int] | None], selfdef] = lambda min, max, then: lambda self: (then or (lambda x, y: x))(randint(min, max), self)
randf: Callable[[float, float, Callable[[float, Any], float] | None], selfdef] = lambda min, max, then: lambda self: (then or (lambda x, y: x))(randint(int(min * 100000), int(max * 100000)) / 100000, self)