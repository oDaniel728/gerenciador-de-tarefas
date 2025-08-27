from typing import Callable, Literal, TypeAlias, Optional
import task as t
import importlib.util
import os
import json
import argparse

json_file: str = "./last.json"
last_keys: TypeAlias = Literal["last_task", "last_method"]
last_data: dict[last_keys, str] = {"last_task": "", "last_method": ""}

# Cria o arquivo se não existir
if not os.path.exists(json_file):
    with open(json_file, "w") as f:
        json.dump(last_data, f)

def set_last(key: last_keys, new: str) -> None:
    global last_data
    with open(json_file, "r") as f:
        last_data = json.load(f)
    last_data[key] = new
    with open(json_file, "w") as f:
        json.dump(last_data, f)

def get_last(key: last_keys) -> str:
    global last_data
    with open(json_file, "r") as f:
        last_data = json.load(f)
    return last_data.get(key, "")

folder: str = "./tasks/python/"
files: list[str] = [f for f in os.listdir(folder) if f.endswith(".py")]
tasks: dict[str, t.BaseTask] = {}
cls: Callable[[], int] = lambda: os.system("cls" if os.name == "nt" else "clear")

def load_tasks() -> None:
    global tasks
    tasks = {}  # Limpa o dicionário antes de recarregar
    for file in files:
        module_name = file[:-3]
        file_path = os.path.join(folder, file)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec:
            continue
        module = importlib.util.module_from_spec(spec)
        if not spec.loader:
            continue
        spec.loader.exec_module(module)
        if hasattr(module, "Task"):
            task_instance: t.BaseTask = module.Task()
            tasks[task_instance.name] = task_instance

def get_task_by_name_or_index(task_input: str) -> Optional[str]:
    # Verifica se é um número
    if task_input.isdigit():
        return task_index_to_name.get(task_input)
    return task_input if task_input in tasks else None

def get_method_by_name_or_index(method_input: str) -> Optional[str]:
    # Verifica se é um número
    if method_input.isdigit():
        return method_index_to_name.get(method_input)
    return method_input if method_input in task.exercise_list.__exercises__ else None

def run_interactive() -> None:
    global task_index_to_name, method_index_to_name, task
    
    # Carrega as tarefas
    load_tasks()
    
    cls()
    enabled_tasks = [(name, task) for name, task in tasks.items() if task.enabled]
    task_index_to_name = {str(i): name for i, (name, _) in enumerate(enabled_tasks, start=1)}
    
    print("Tarefas disponíveis:")
    for idx, (task_name, task_instance) in enumerate(enabled_tasks, start=1):
        print(f"[{idx}]: {task_name}")
        if task_instance.description:
            print(f"    {task_instance.description}")
    
    last_task = get_last("last_task")
    desired_task_input = input(f"Escolha a tarefa [{last_task}] >>> ").strip()
    
    if not desired_task_input:
        desired_task = last_task
    else:
        desired_task = get_task_by_name_or_index(desired_task_input)
    
    if not desired_task or desired_task not in tasks:
        print("Tarefa não encontrada...")
        exit()
    
    set_last("last_task", desired_task)
    task = tasks[desired_task]
    cls()
    
    if len(task.exercise_list.__exercises__.keys()) == 1:
        maindef: t.TaskMethod = list(task.exercise_list.__exercises__.values())[0]
        if maindef.__name__ == "main":
            task.run()
            exit()
    
    print("Funções disponíveis nessa task:")
    exercise_names = list(task.exercise_list.__exercises__.keys())
    method_index_to_name = {str(i): name for i, name in enumerate(exercise_names, start=1)}
    
    for idx, ex_name in enumerate(exercise_names, start=1):
        desc: str = task._descriptions.get(ex_name, "")
        print(f"[{idx}]: {ex_name}")
        if desc:
            print(f"    {desc}")
    
    last_method = get_last("last_method")
    desired_func_input = input(f"Digite a função para rodar (default: {last_method or 'main'}) >>> ").strip()
    
    if not desired_func_input:
        desired_func = last_method or "main"
    else:
        desired_func = get_method_by_name_or_index(desired_func_input)
    
    if not desired_func:
        desired_func = "main"
    
    set_last("last_method", desired_func)
    
    if task.has(desired_func):
        cls()
        task.run(desired_func)
    else:
        print("Função não encontrada...")

def run_with_args(args: argparse.Namespace) -> None:
    global task_index_to_name, method_index_to_name, task
    
    # Carrega tarefas
    load_tasks()
    enabled_tasks = [(name, task) for name, task in tasks.items() if task.enabled]
    task_index_to_name = {str(i): name for i, (name, _) in enumerate(enabled_tasks, start=1)}
    
    # Determina a tarefa
    if args.latest:
        desired_task = get_last("last_task")
        desired_func = get_last("last_method") or "main"
    else:
        task_input = args.task or args.task_positional
        desired_task = get_task_by_name_or_index(task_input) if task_input else None
        
        if not desired_task:
            print("Tarefa não encontrada...")
            exit()
        
        set_last("last_task", desired_task)
        task = tasks[desired_task]
        
        # Determina a função
        exercise_names = list(task.exercise_list.__exercises__.keys())
        method_index_to_name = {str(i): name for i, name in enumerate(exercise_names, start=1)}
        
        func_input = args.func or args.func_positional or "main"
        desired_func = get_method_by_name_or_index(func_input) if func_input else "main"
        
        if not desired_func:
            desired_func = "main"
        
        set_last("last_method", desired_func)
    
    # Executa a tarefa
    if desired_task and desired_task in tasks:
        task = tasks[desired_task]
        if task.has(desired_func):
            cls()
            task.run(desired_func)
        else:
            print(f"Função '{desired_func}' não encontrada na tarefa '{desired_task}'")
    else:
        print(f"Tarefa '{desired_task}' não encontrada")

def main():
    parser = argparse.ArgumentParser(description="Executa tarefas de Python")
    
    # Argumentos posicionais
    parser.add_argument("task_positional", nargs="?", default=None, help="Nome ou número da tarefa")
    parser.add_argument("func_positional", nargs="?", default=None, help="Nome da função (padrão: main)")
    
    # Argumentos opcionais
    parser.add_argument("--task", "-t", default=None, help="Nome ou número da tarefa")
    parser.add_argument("--def", "-f", dest='func', default=None, help="Nome da função (padrão: main)")
    parser.add_argument("--latest", "-l", action="store_true", default=False, help="Usa a última tarefa e função executadas")
    
    args = parser.parse_args()
    
    # Garante que todos os atributos existam com valores padrão
    if not hasattr(args, 'func'):
        args.func = None
    if not hasattr(args, 'task'):
        args.task = None
    if not hasattr(args, 'latest'):
        args.latest = False
    
    # Verifica se deve usar modo interativo
    if not any([args.task, args.task_positional, args.func, args.func_positional, args.latest]):
        run_interactive()
    else:
        run_with_args(args)

if __name__ == "__main__":
    main()