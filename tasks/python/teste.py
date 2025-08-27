from task import BaseTask, Integer, Number, exercise
import callables as c
def main():
    num: Integer = Integer("num", 0)
    num\
    .do( lambda self: self + 1 )\
    .doif( lambda self: self % 2 == 0, 
        lambda self: self + 2
    ).doif( lambda self: self % 2 != 0, 
        lambda self: self + 3
    ).doforeach( lambda self: [self], 
        lambda i, v, self: (
            print(self),
            self
        )[1]
    )
    return 0
class Task(BaseTask):
    """Primeiro teste: inputs com try catch"""
    def __init__(self):
        super().__init__("teste")
        self.enabled = True
    @exercise(desc="")
    def main(self): main()