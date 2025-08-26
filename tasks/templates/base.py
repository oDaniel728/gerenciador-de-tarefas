from task import BaseTask, exercise

# função principal
def main():
    return 0 # somente um placeholder
# (recomendo que haja somente uma classe por arquivo)
class Task(BaseTask):
    """descrição"""
    # a inicialização da classe:
    def __init__(self):
        # chama o construtor da classe BaseTask
        super().__init__("base") # "base" seria o nome da função
        self.enabled = False
        # se enabled for True, ele é mostrado;
        # se for False, ele é escondido,
        # mas ainda é válido.
    
    # insere a função na lista de tarefas:
    @exercise(desc="descrição da função")
    # função(não obigatória)
    def main(self): main()
    # caso haja somente a função main, ela é executada
    # automaticamente...