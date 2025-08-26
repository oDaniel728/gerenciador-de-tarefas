from typing import Callable
TaskMethod = Callable[[], None]
ExerciseDict = dict[str, TaskMethod]

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
        func = self.get(name)
        if callable(func):
            return func()
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
                self._descriptions[ex_name] = ex_desc  # armazena a descrição separadamente
        
    def run(self, name: str = "main"):
        self.exercise_list.run(name)
    
    def has(self, name: str = "main") -> bool:
        return self.exercise_list.has(name)
        
    def __del__(self):
        del self.tasks[self.name]
        del self