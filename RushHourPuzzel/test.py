from game import RushHourPuzzle
from algoBFS import BFS

def main():
    # 1. Initialiser le puzzle RushHour
    puzzle = RushHourPuzzle()
    puzzle.setVehicles("../csv/2-d.csv")  # Adapte le chemin à ton fichier CSV !
    puzzle.setBoard(show=True)

    # 2. Exécuter BFS
    result = BFS(
        puzzle,
        lambda state: state.successorFunction(),  # successorsFn
        lambda state: state.isGoal()              # isGoal
    )

    # 3. Afficher le résultat
    if result:
        print("✅ Solution trouvée !")
        print("Actions :", result.getSolution())
        print("Affichage des états :")
        for idx, state in enumerate(result.getPath()):
            print(f"\n--- Étape {idx} ---")
            state.setBoard(show=True)
    else:
        print("❌ Aucune solution trouvée.")

if __name__ == "__main__":
    main()