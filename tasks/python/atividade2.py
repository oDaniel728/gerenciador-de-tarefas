from task import BaseTask, ExerciseList, exercise
import re
from typing import Callable, Tuple

def format_number(n: int, show_binary: bool = False, show_hex: bool = False) -> str:
    """Formata um número com representações adicionais conforme solicitado."""
    parts = [str(n)]
    if show_binary:
        parts.append(f"bin: {bin(n)}")
    if show_hex:
        parts.append(f"hex: {hex(n)}")
    return " | ".join(parts)

def get_operation_result(a: int, b: int, operation: Callable[[int, int], int], symbol: str) -> Tuple[str, str]:
    """Calcula e formata o resultado de uma operação bit a bit."""
    result = operation(a, b)
    formatted_a = format_number(a)
    formatted_b = format_number(b)
    formatted_result = format_number(result)
    return (f"{formatted_a} {symbol} {formatted_b}", formatted_result)

def main():
    # Entrada de dados com validação
    try:
        a = int(input("Digite um número: "))
        b = int(input("Digite outro número: "))
    except ValueError:
        print("Por favor, digite números inteiros válidos.")
        return

    # Menu de operações
    print("""
Operações disponíveis:
    [1]: OR (|)
    [2]: AND (&)
    [3]: XOR (^)
    [4]: Deslocamento à direita (>>)
    [5]: Deslocamento à esquerda (<<)

Flags de formatação:
    [B]: Mostrar em binário
    [H]: Mostrar em hexadecimal

Exemplos de entrada:
    "1" - Apenas operação OR
    "1B" - OR com binário
    "23H" - AND e XOR com hexadecimal
    "1B3H" - OR com binário e XOR com hexadecimal
""")

    # Entrada do usuário e validação com regex
    op_input = input("> ").strip().upper()
    if not re.fullmatch(r'^[1-5BHbh]+$', op_input):
        print("Entrada inválida. Use apenas números 1-5 e letras B/H.")
        return

    # Extrair flags e operações
    binary = 'B' in op_input.upper()
    hexadecimal = 'H' in op_input.upper()
    operations = re.findall(r'[1-5]', op_input)

    # Dicionário de operações
    op_dict = {
        '1': (lambda x, y: x | y, "|"),
        '2': (lambda x, y: x & y, "&"),
        '3': (lambda x, y: x ^ y, "^"),
        '4': (lambda x, y: x >> y, ">>"),
        '5': (lambda x, y: x << y, "<<")
    }

    # Executar operações selecionadas
    for op_code in operations:
        if op_code in op_dict:
            operation, symbol = op_dict[op_code]
            expression, result = get_operation_result(a, b, operation, symbol)
            
            # Formatar saída com as representações solicitadas
            formatted_result = format_number(operation(a, b), binary, hexadecimal)
            print(f"{expression} = {formatted_result}\n")
        else:
            print(f"Operação inválida: {op_code}")

class Task(BaseTask):
    """Operadores de bits"""
    def __init__(self):
        super().__init__("atividade2")
        
    @exercise(desc="função principal;")
    def main(self): main()