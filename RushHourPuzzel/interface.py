import pygame
import sys
import os
from copy import deepcopy
from game import RushHourPuzzle
from algoBFS import BFS
from Astar_algo import A
# ===================== CONFIG =====================
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
CELL_SIZE = 80
STEP_DELAY = 250  # ms
MARGIN_TOP = 100

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rush Hour Magic")
clock = pygame.time.Clock()

# ===================== COULEURS =====================
GRID_BG = (45, 25, 75)
WALL_COLOR = (0, 0, 0)
CAR_COLORS_UNIQUES = [
    (255, 128, 0), (0, 128, 255), (255, 105, 180), (144, 238, 144),
    (216, 191, 216), (175, 238, 238), (255, 250, 205), (255, 165, 0),
    (135, 206, 250), (199, 21, 133), (255, 215, 0), (64, 224, 208),
    (255, 69, 0), (0, 255, 127)
]
RED_CAR = (255, 0, 0)

try:
    TITLE_FONT = pygame.font.Font("assets/HarryP.ttf", 70)
    MENU_FONT = pygame.font.Font("assets/HarryP.ttf", 28)
    SMALL_FONT = pygame.font.Font("assets/HarryP.ttf", 20)
except:
    TITLE_FONT = pygame.font.SysFont(None, 70)
    MENU_FONT = pygame.font.SysFont(None, 28)
    SMALL_FONT = pygame.font.SysFont(None, 20)

# ===================== ASSETS =====================
def load_img(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception as e:
        print(f"Image non trouvée: {path} ({e})")
        return pygame.Surface(size if size else (50,50))

door_img = load_img("./assets/door.png", (120, 180))
home_icon_img = load_img("./assets/entree.png", (50, 50))
replay_icon_img = load_img("./assets/repeter.png", (50, 50))

# ===================== FONCTIONS =====================
def draw_board(puzzle, step=None, total=None, no_solution=False):
    screen.fill(GRID_BG)
    start_x = (WINDOW_WIDTH - puzzle.board_width * CELL_SIZE) // 2
    start_y = MARGIN_TOP

    # Couleurs uniques pour véhicules (aucun doublon)
    unique_colors = {}
    used_colors = set()
    for v in puzzle.vehicles:
        if v["id"] == "X":
            unique_colors["X"] = RED_CAR
        else:
            for color in CAR_COLORS_UNIQUES:
                if color not in used_colors:
                    unique_colors[v["id"]] = color
                    used_colors.add(color)
                    break

    for y in range(puzzle.board_height):
        for x in range(puzzle.board_width):
            val = puzzle.board[y][x]
            rect = pygame.Rect(start_x + x*CELL_SIZE, start_y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Fond subtil
            base_color = (50 + y*3, 50 + x*3, 90 + (x+y)*2)
            pygame.draw.rect(screen, base_color, rect)
            pygame.draw.rect(screen, (100, 80, 130), rect, 2, border_radius=6)

            if val == '#':
                wall_rect = rect.inflate(-20, -20)
                pygame.draw.rect(screen, WALL_COLOR, wall_rect, border_radius=4)
            elif val != '.':
                color = unique_colors.get(val, (150, 150, 255))
                car_rect = rect.inflate(-10, -10)
                pygame.draw.rect(screen, color, car_rect, border_radius=10)

    #  solution
    if step is not None and total is not None:
        txt = SMALL_FONT.render(f"Étape {step+1} / {total}", True, (255,255,255))
        screen.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, MARGIN_TOP-40))
    if no_solution:
        txt = TITLE_FONT.render("Aucune solution trouvée", True, (255,0,0))
        screen.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, WINDOW_HEIGHT//2 - 60))

def apply_action(puzzle, action):
    vid, direction = action
    new_puzzle = deepcopy(puzzle)
    for v in new_puzzle.vehicles:
        if v["id"] == vid:
            if direction == "left": v["x"] -= 1
            if direction == "right": v["x"] += 1
            if direction == "up": v["y"] -= 1
            if direction == "down": v["y"] += 1
            break
    new_puzzle.setBoard()
    return new_puzzle

def draw_menu(levels, hover_index, clicked_index=-1):
    screen.fill(GRID_BG)
    title_surface = TITLE_FONT.render("Rush Hour Puzzle", True, (255, 215, 0))
    screen.blit(title_surface, (WINDOW_WIDTH//2 - title_surface.get_width()//2, 40))

    door_width, door_height = 120, 180
    cols = 4
    spacing_x = 180
    spacing_y = 220
    start_x = (WINDOW_WIDTH - spacing_x*(cols-1) - door_width)//2
    start_y = 150

    for i, level in enumerate(levels):
        row = i // cols
        col = i % cols
        x = start_x + col*spacing_x
        y = start_y + row*spacing_y

        offset_y = -10 if hover_index == i else 0
        click_offset = 15 if clicked_index == i else 0
        screen.blit(door_img, (x, y + offset_y - click_offset))

        text = MENU_FONT.render(f"Niveau {i+1}", True, (255, 215, 0))
        screen.blit(text, (x + door_width//2 - text.get_width()//2,
                           y + door_height//2 - text.get_height()//2 + offset_y))

def draw_algo_menu(selected=None, show_astar_msg=False):
    screen.fill(GRID_BG)
    txt = TITLE_FONT.render("Choisissez l'algorithme", True, (255, 215, 0))

    screen.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, 120))

    bfs_rect = pygame.Rect(WINDOW_WIDTH//2-200, 270, 180, 80)
    astar_rect = pygame.Rect(WINDOW_WIDTH//2+20, 270, 180, 80)

    pygame.draw.rect(screen, (60,180,80) if selected==0 else (100,100,100), bfs_rect, border_radius=15)
    pygame.draw.rect(screen, (80,80,180) if selected==1 else (100,100,100), astar_rect, border_radius=15)

    bfs_txt = MENU_FONT.render("BFS", True, (255,255,255))
    astar_txt = MENU_FONT.render("A*", True, (255,255,255))

    screen.blit(bfs_txt, (bfs_rect.x + 60, bfs_rect.y + 25))
    screen.blit(astar_txt, (astar_rect.x + 60, astar_rect.y + 25))
    """if show_astar_msg:
        warn = MENU_FONT.render("Méthode A* pas encore ajoutée", True, (255,0,0))
        screen.blit(warn, (WINDOW_WIDTH//2 - warn.get_width()//2, 400))"""
    return bfs_rect, astar_rect

# ===================== MAIN =====================
def main():
    csv_dir = "./csv"
    levels = sorted([f for f in os.listdir(csv_dir) if f.endswith(".csv")])

    running = True
    in_menu = True
    in_algo_menu = False
    puzzle = None
    solution = None
    step = 0
    clicked_index = -1
    algo_choice = None
    solution_node = None
    last_step_time = pygame.time.get_ticks()
    no_solution = False
    show_astar_msg = False

    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        hover_index = -1

        if in_menu:
            cols = 4
            spacing_x = 180
            spacing_y = 220
            door_width, door_height = 120, 180
            start_x = (WINDOW_WIDTH - spacing_x*(cols-1) - door_width)//2
            start_y = 150
            for i in range(len(levels)):
                row = i // cols
                col = i % cols
                x = start_x + col*spacing_x
                y = start_y + row*spacing_y
                rect = pygame.Rect(x, y, door_width, door_height)
                if rect.collidepoint(mouse_pos):
                    hover_index = i

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if in_menu and event.type == pygame.MOUSEBUTTONDOWN and hover_index != -1:
                clicked_index = hover_index
                in_menu = False
                in_algo_menu = True
                algo_choice = None
                show_astar_msg = False

            if in_algo_menu and event.type == pygame.MOUSEBUTTONDOWN:
                bfs_rect, astar_rect = draw_algo_menu(algo_choice, show_astar_msg)
                if bfs_rect.collidepoint(mouse_pos):
                    algo_choice = 0
                    show_astar_msg = False
                elif astar_rect.collidepoint(mouse_pos):
                    algo_choice = 1
                    show_astar_msg = True
                # Validation au clic sur le bouton choisi
                if algo_choice == 0:
                    # Charger le niveau et choisir BFS
                    level_file = os.path.join(csv_dir, levels[clicked_index])
                    puzzle = RushHourPuzzle()
                    puzzle.setVehicles(level_file)
                    puzzle.setBoard()
                    solution_node = BFS(
                        puzzle,
                        lambda state: state.successorFunction(),
                        lambda state: state.isGoal()
                    )
                    solution = solution_node.getSolution() if solution_node else []
                    step = 0
                    no_solution = not solution
                    in_algo_menu = False
                    last_step_time = pygame.time.get_ticks()
                elif algo_choice == 1:
                    # A* pas encore demander 
                    level_file = os.path.join(csv_dir, levels[clicked_index])
                    puzzle = RushHourPuzzle()
                    puzzle.setVehicles(level_file)
                    puzzle.setBoard()
                    solution_node = A(
                        puzzle,
                        lambda state: state.successorFunction(),
                        lambda state: state.isGoal()
                    )
                    solution = solution_node.getSolution() if solution_node else []
                    step = 0
                    no_solution = not solution
                    in_algo_menu = False
                    last_step_time = pygame.time.get_ticks()

            if event.type == pygame.MOUSEBUTTONDOWN and not in_menu and not in_algo_menu and puzzle:
                board_bottom_y = MARGIN_TOP + puzzle.board_height*CELL_SIZE
                replay_rect = pygame.Rect(WINDOW_WIDTH//2 - 25, board_bottom_y + 20, 50, 50)
                home_rect = pygame.Rect(20, 20, 50, 50)
                if replay_rect.collidepoint(mouse_pos):
                    level_file = os.path.join(csv_dir, levels[clicked_index])
                    puzzle = RushHourPuzzle()
                    puzzle.setVehicles(level_file)
                    puzzle.setBoard()
                    if algo_choice == 0:
                        solution_node = BFS(
                            puzzle,
                            lambda state: state.successorFunction(),
                            lambda state: state.isGoal()
                        )
                        solution = solution_node.getSolution() if solution_node else []
                        step = 0
                        no_solution = not solution
                        last_step_time = pygame.time.get_ticks()
                    # le message reste affiche
                elif home_rect.collidepoint(mouse_pos):
                    in_menu = True
                    in_algo_menu = False
                    clicked_index = -1
                    puzzle = None
                    solution = None
                    step = 0
                    no_solution = False
                    show_astar_msg = False

        # Affichage
        if in_menu:
            draw_menu(levels, hover_index, clicked_index)
        elif in_algo_menu:
            draw_algo_menu(algo_choice, show_astar_msg)
        elif puzzle:
            if solution and step < len(solution) and not no_solution:
                now = pygame.time.get_ticks()
                if now - last_step_time > STEP_DELAY:
                    action = solution[step]
                    puzzle = apply_action(puzzle, action)
                    step += 1
                    last_step_time = now
            draw_board(puzzle, step, len(solution) if solution else 0, no_solution)
            screen.blit(home_icon_img, (20, 20))
            board_bottom_y = MARGIN_TOP + puzzle.board_height*CELL_SIZE
            screen.blit(replay_icon_img, (WINDOW_WIDTH//2 - 25, board_bottom_y + 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
