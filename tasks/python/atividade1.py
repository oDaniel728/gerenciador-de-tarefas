from task import BaseTask, ExerciseList, exercise

def main():
    xp_per_enemy: int = 50
    bonus_xp: int = 20

    enemies_defeated: int = int(input("Quantos inimigos foram derrotados? "))
    total_xp: int = (xp_per_enemy * enemies_defeated) + bonus_xp

    print(f"Você adiquiriu {total_xp}xp!");  
class Task(BaseTask):
    """Variáveis"""
    def __init__(self):
        super().__init__("atividade1")
        
    @exercise(desc="função principal;")
    def main(self): main()