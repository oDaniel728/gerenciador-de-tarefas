from typing import Callable, Literal, TypeAlias
import task as t
import importlib.util
import os
import json

json_file: str = "./last.json"
last_keys: TypeAlias = Literal["last_task", "last_method"]
last_data: dict[last_keys, str] = {"last_task": "", "last_method": ""}

# cria o arquivo se não existir
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
# lista apenas arquivos .py
files: list[str] = [f for f in os.listdir(folder) if f.endswith(".py")]
# dict[filename, BaseTask]
tasks: dict[str, t.BaseTask] = {}
# limpar o terminal
cls: Callable[[], int] = lambda: os.system("cls")
# cls: Callable[[], int] = lambda: 1
cls()

for file in files:
    module_name = file[:-3]  # tira o .py
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

# --- Lista de tarefas numeradas ---
enabled_tasks = [(name, task) for name, task in tasks.items() if task.enabled]
task_index_to_name = {str(i): name for i, (name, _) in enumerate(enabled_tasks, start=1)}

print("Tarefas disponíveis:")
for idx, (task_name, task_instance) in enumerate(enabled_tasks, start=1):
    print(f"[{idx}]: {task_name}")
    if task_instance.description:
        print(f"    {task_instance.description}")

# --- input da tarefa ---
last_task = get_last("last_task")
desired_task_input = input(f"Escolha a tarefa [{last_task}] >>> ").strip()
if not desired_task_input:
    desired_task = last_task
else:
    # Verifica se é um número ou nome
    desired_task = task_index_to_name.get(desired_task_input, desired_task_input)

if not desired_task or desired_task not in tasks:
    print("Tarefa não encontrada...")
    exit()

set_last("last_task", desired_task)
task: t.BaseTask = tasks[desired_task]
cls()

if (len(task.exercise_list.__exercises__.keys()) == 1):
    maindef: t.TaskMethod = list(task.exercise_list.__exercises__.values())[0]
    if maindef.__name__ == "main":
        task.run()
        exit()

# --- Lista de métodos numerados ---
print("Funções disponíveis nessa task:")
exercise_names = list(task.exercise_list.__exercises__.keys())
method_index_to_name = {str(i): name for i, name in enumerate(exercise_names, start=1)}

for idx, ex_name in enumerate(exercise_names, start=1):
    desc: str = task._descriptions.get(ex_name, "")
    print(f"[{idx}]: {ex_name}")
    if desc:
        print(f"    {desc}")

# --- input do método ---
last_method = get_last("last_method")
desired_func_input = input(f"Digite a função para rodar (default: {last_method or 'main'}) >>> ").strip()
if not desired_func_input:
    desired_func = last_method or "main"
else:
    # Verifica se é um número ou nome
    desired_func = method_index_to_name.get(desired_func_input, desired_func_input)

if not desired_func:
    desired_func = "main"

set_last("last_method", desired_func)

if task.has(desired_func):
    cls()
    task.run(desired_func)
else:
    print("Função não encontrada...")