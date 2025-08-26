# Gerenciador de tarefas

Digite ``python run.py`` para iniciar o gerenciador de tarefas(ou *gerenciador de atividades*)...

### Como utilizar:
- Vá em [tasks/template/base.py](tasks/templates/base.py), o arquivo possui uma template de como uma atividade pode ser inicializada...
- As atividades devem estar dentro de [tasks/python](tasks/python) e devem conter nomes legíveis e simples.

### Estrutura do Projeto:
- Em [tasks/template/base.py](tasks/templates/base.py), existe um código template que serve para ser reutilizado mais tarde, lá há algumas instruções para uso.
- Na pasta [tasks/python](tasks/python) ficam os arquivos que serão executado como atividades.
- Em [last.json](last.json) há um dicionário onde fica os dados dá sua última execução do programa.
- Em [task.py](task.py) está a base do código, pode editar se quiser :D