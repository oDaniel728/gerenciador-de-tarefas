import datetime
import inspect
import json
from operator import add
from typing import Any, Callable, Generic, Optional, Self, Union, TypeVar
from typing_extensions import TypeAliasType

TaskMethod = Callable[[], None]
ExerciseDict = dict[str, TaskMethod]

T = TypeVar("T")
U = TypeVar("U")

def nonedef() -> None:
	return None


# --- Decorator ---
def exercise(name: str | None = None, desc: str | None = None):
	"""
	Marca um método como exercício de task.
	Se não passar nome, usa o próprio nome da função.
	"""

	def wrapper(func):
		func._exercise_name = name or func.__name__
		func._exercise_desc = desc or ""
		return func

	return wrapper


class ExerciseList:
	def __init__(self, **list: TaskMethod):
		self.__exercises__: ExerciseDict = {}
		for name, func in list.items():
			self.set(name, func)

	def add(self, name: str, callable: TaskMethod):
		self.set(name, callable)

	def get(self, name: str) -> TaskMethod:
		return self.__exercises__.get(name, nonedef)

	def has(self, name: str) -> bool:
		return name in self.__exercises__

	def run(self, name: str = "main") -> None:
		start: datetime.datetime = datetime.datetime.now()
		func = self.get(name)

		if callable(func):
			func()
			end: datetime.datetime = datetime.datetime.now()
			diff: datetime.timedelta = end - start
			print(f"Programa terminado em {diff.total_seconds():.5f} segundos...")
		else:
			raise TypeError(f"'{name}' não é uma função executável.")

	def set(self, name: str, callable: TaskMethod) -> None:
		self.__exercises__[name] = callable

	def dlt(self, name: str) -> TaskMethod:
		task: TaskMethod = self.__exercises__[name]
		del self.__exercises__[name]
		return task

	@property
	def main(self) -> TaskMethod:
		return self.get("main")

	@main.setter
	def main(self, task: TaskMethod) -> None:
		return self.set("main", task)

	@main.deleter
	def main(self) -> TaskMethod:
		return self.dlt("main")


class BaseTask:
	tasks: "dict[str, BaseTask]" = {}

	def __init__(self, name: str = "", exercises: ExerciseList | None = None):
		self.name: str = name
		self.description: str = self.__doc__ or ""
		self.exercise_list: ExerciseList = exercises or ExerciseList()
		self._descriptions: dict[str, str] = {}
		self.tasks[name] = self
		self.enabled: bool = True
		# --- coleta automática dos métodos decorados com @exercise ---
		for attr_name in dir(self):
			attr: TaskMethod = getattr(self, attr_name)
			if callable(attr) and hasattr(attr, "_exercise_name"):
				ex_name = getattr(attr, "_exercise_name")
				ex_desc = getattr(attr, "_exercise_desc", "")
				self.exercise_list.set(ex_name, attr)  # mantém a função
				self._descriptions[ex_name] = (
					ex_desc  # armazena a descrição separadamente
				)

	def run(self, name: str = "main"):
		self.exercise_list.run(name)

	def has(self, name: str = "main") -> bool:
		return self.exercise_list.has(name)

	def __del__(self):
		del self.tasks[self.name]
		del self


# --- Esquema de Variáveis ---


class VariableStorage:
    path: str = "variables.json"
    def __init__(self, autosave: bool = False, log_changes: bool = False) -> None:
        self.__variables__: dict[str, Any] = {}
        self.autosave: bool = autosave
        self.log_changes: bool = log_changes
        self.load()  # Carrega automaticamente ao inicializar

    def _log(self, message: str) -> None:
        if self.log_changes:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}]: " + message)

    def set(self, key: str, value: Any) -> Self:
        self._log("set: {} = {}".format(key, value))
        self.__variables__[key] = value
        if self.path and self.autosave:
            self.save()  # Salva todas as variáveis
            
        return self

    def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        return self.__variables__.get(key, default)

    def dlt(self, key: str) -> Self:
        if key in self.__variables__:
            del self.__variables__[key]
            if self.path and self.autosave:
                self.save()  # Salva após deletar
        return self

    def has(self, key: str) -> bool:
        return key in self.__variables__

    def contains(self, value: Any) -> bool:
        return value in self.__variables__.values()

    def getkey(self, value: Any) -> str:
        if self.contains(value):
            for k, v in self.__variables__.items():
                if v == value:
                    self._log("get(key): {} (is) {}".format(k, v))
                    return k
        return ""

    def size(self) -> int:
        return len(self.__variables__)

    def setall(self, **kwargs: Any) -> Self:
        for k, v in kwargs.items():
            self.set(k, v)  # Usa set() para garantir logging e autosave
        return self

    def getall(self, *keys: str) -> list[Any]:
        r: list[Any] = []
        for k in keys:
            if self.has(k):
                value = self.get(k)
                r.append(value)
                self._log("get(only): {} = {}".format(k, value))
        return r

    def save(self, indent: bool = False) -> Self:
        with open(self.path, "w") as f:
            json.dump(self.__variables__, f, indent=(4 if indent else None))
            self._log("save: {}".format(json.dumps(self.__variables__, indent=4)))
        return self

    def load(self) -> Self:
        try:
            with open(self.path, "r") as f:
                content = f.read()
                if content.strip() == "":
                    self.__variables__ = {}
                else:
                    self.__variables__ = json.loads(content)
                self._log("load: {}".format(json.dumps(self.__variables__, indent=4)))
        except (FileNotFoundError, json.JSONDecodeError):
            self.__variables__ = {}
            self.save()  # Cria arquivo novo se não existir ou estiver corrompido
        return self

    def loadonly(self, *keys: str) -> Self:
        try:
            with open(self.path, "r") as f:
                content = f.read()
                if content.strip() == "":
                    return self
                loaded = json.loads(content)
                for k in keys:
                    if k in loaded:
                        self.__variables__[k] = loaded[k]
                        self._log("load(only): {} = {}".format(k, loaded[k]))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return self

    def saveonly(self, *keys: str) -> Self:
        nd: dict = {k: self.__variables__[k] for k in keys if k in self.__variables__}
        with open(self.path, "w") as f:
            json.dump(nd, f)
            self._log("save(only): {}".format(json.dumps(nd, indent=4)))
        return self

storage: VariableStorage = VariableStorage(autosave=True)

class Variable(Generic[T]):
    def __init__(self, name: str, value: T, overwrite: bool = False, storage: VariableStorage = storage) -> None:
        super().__init__()
        self.storage: VariableStorage = storage
        self.varname = name
        if overwrite:
            self.storage.set(self.varname, value)
        else:
            self.storage.get(self.varname, value)

    @property
    def value(self) -> T:
        return self.storage.get(self.varname) # type: ignore

    @value.setter
    def value(self, value):
        self.storage.set(self.varname, value)

    @property
    def name(self):
        return self.varname

    def __str__(self) -> str:
        return str(self.value)
    
    def expr(self, expr: Callable[[T], T] | None = None, _if: bool = True) -> T:
        if (_if):
            val: T = ((expr) or (lambda self: self))(self.value)
            if isinstance(val, tuple):
                if val[-1]:
                    return val[0]
        return self.value
    
    def do(self, expr: Callable[[T], T] = lambda self: self) -> Self:
        val: T = self.expr(expr)
        self.value = val
        return self

    def doif(self, If: bool | Callable[[T], bool] = lambda self: True, exprif: Callable[[T], T] = lambda self: self, exprelse: Callable[[T], T] = lambda self: self) -> Self:
        if (If(self.value) if isinstance(If, Callable) else If):
            self.do(exprif)
        else:
            self.do(exprelse)
        return self
    
    def doforeach(self, foreach: list[U] | Callable[[T], list[U]] = [None], expr: Callable[[int, U, T], T] = lambda i, v, self: self) -> Self:
        for i, v in enumerate(foreach(self.value) if isinstance(foreach, Callable) else foreach):
            val: T = expr(i, v, self.value)
            self.value = val
        return self
    def print(self) -> Self:
        print(self.value)
        return self
    
    def __call__(self, expr: Callable[[T], T]) -> Self:
        return self.do(expr)

integer = 0
Integer = Variable[int]
string = ""
String = Variable[str]
boolean = False
Boolean = Variable[bool]
num = TypeAliasType("num", Union[int, float])
number = floating = 0.0
Number = Floating = Variable[num]
nil = None
Nil = Variable[None]