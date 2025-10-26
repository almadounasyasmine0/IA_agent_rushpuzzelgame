import csv

class RushHourPuzzle:
    def __init__(self):
        self.board_height = None
        self.board_width = None
        self.vehicles = []
        self.walls = []
        self.vagent = None  

    def setVehicles(self, csv_path):
        with open(csv_path, "r", encoding="utf-8") as fichier:
            lecteur = csv.reader(fichier)
            lignef = next(lecteur)
            self.board_height = int(lignef[0])
            self.board_width  = int(lignef[1])
            self.vehicles = []
            self.walls = []
            for ligne in lecteur:
                if ligne[0].strip() == "#":
                    self.walls.append({"x": int(ligne[1]), "y": int(ligne[2])})
                else:
                    thisdict = {
                        "id": ligne[0],
                        "x": int(ligne[1]),
                        "y": int(ligne[2]),
                        "orientation": ligne[3],
                        "length": int(ligne[4])
                    }
                    self.vehicles.append(thisdict)

    def setBoard(self, show=False):
       
        board = [['.' for _ in range(self.board_width)] for _ in range(self.board_height)]

        # Placer wals
        for wall in self.walls:
            x = wall["x"]
            y = wall["y"]
            board[y][x] = '#'

        # Placer voituress
        for vehicle in self.vehicles:
            x = vehicle["x"]
            y = vehicle["y"]
            length = vehicle["length"]
            orientation = vehicle["orientation"]
            vid = vehicle["id"]
            if vid == "X":
                self.vagent = {
                    "id": "X",
                    "x": x,
                    "y": y,
                    "orientation": orientation,
                    "length": length
                }
            if orientation.upper() == "H":
                for i in range(length):
                    board[y][x + i] = vid
            else:  # "V"
                for i in range(length):
                    board[y + i][x] = vid

        self.board = board
        if show:
            for row in board:
                print(' '.join(row))

    def isGoal(self):
        
        if not self.vagent:
            return False  # Voiture rouge findit

        x = self.vagent["x"]
        y = self.vagent["y"]
        orientation = self.vagent["orientation"]
        length = self.vagent["length"]

        if orientation.upper() == "H":
            goal_x = self.board_width - 1 # une pourque python debute par 0 et l'autre pourqu'il revient a la casse precidente
            goal_y = self.board_height // 2 - 1 # selon les reprisentation des exemple de la prof
            red_car_head_x = x + length - 1
            red_car_y = y
            if red_car_head_x == goal_x and red_car_y == goal_y:
                return True
        return False
    
  
    def successorFunction(self):
   
     successors = []

     for idx, vehicle in enumerate(self.vehicles):
         x = vehicle["x"]
         y = vehicle["y"]
         orientation = vehicle["orientation"].upper()
         length = vehicle["length"]
         vid = vehicle["id"]

         # savoir l'ort de voiture
         if orientation == "H":
             # Dplc droite
             if x + length < self.board_width and self.board[y][x + length] == '.':
                 #  copie  des v et du p
                 new_vehicles = [v.copy() for v in self.vehicles]
                 new_vehicles[idx]["x"] += 1
                 new_puzzle = RushHourPuzzle()
                 new_puzzle.board_height = self.board_height
                 new_puzzle.board_width = self.board_width
                 new_puzzle.vehicles = new_vehicles
                 new_puzzle.walls = [w.copy() for w in self.walls]
                 new_puzzle.setBoard()
                 action = (vid, "right")
                 successors.append((action, new_puzzle))

             # deplacer gauche 
             if x - 1 >= 0 and self.board[y][x - 1] == '.':
                new_vehicles = [v.copy() for v in self.vehicles]
                new_vehicles[idx]["x"] -= 1
                new_puzzle = RushHourPuzzle()
                new_puzzle.board_height = self.board_height
                new_puzzle.board_width = self.board_width
                new_puzzle.vehicles = new_vehicles
                new_puzzle.walls = [w.copy() for w in self.walls]
                new_puzzle.setBoard()
                action = (vid, "left")
                successors.append((action, new_puzzle))

         else:  # 'V'
            #  bas 
            if y + length < self.board_height and self.board[y + length][x] == '.':
                new_vehicles = [v.copy() for v in self.vehicles]
                new_vehicles[idx]["y"] += 1
                new_puzzle = RushHourPuzzle()
                new_puzzle.board_height = self.board_height
                new_puzzle.board_width = self.board_width
                new_puzzle.vehicles = new_vehicles
                new_puzzle.walls = [w.copy() for w in self.walls]
                new_puzzle.setBoard()
                action = (vid, "down")
                successors.append((action, new_puzzle))

            #  haut 
            if y - 1 >= 0 and self.board[y - 1][x] == '.':
                new_vehicles = [v.copy() for v in self.vehicles]
                new_vehicles[idx]["y"] -= 1
                new_puzzle = RushHourPuzzle()
                new_puzzle.board_height = self.board_height
                new_puzzle.board_width = self.board_width
                new_puzzle.vehicles = new_vehicles
                new_puzzle.walls = [w.copy() for w in self.walls]
                new_puzzle.setBoard()
                action = (vid, "up")
                successors.append((action, new_puzzle))

     return successors            
    def equals(self, other):
        if not isinstance(other, RushHourPuzzle):
            return False
        if self.board_height != other.board_height or self.board_width != other.board_width:
            return False
        if self.vehicles != other.vehicles:
            return False
        if self.walls != other.walls:
            return False
        return True
def equals(self, other):
    if not isinstance(other, RushHourPuzzle):
        return False
    if self.board_height != other.board_height or self.board_width != other.board_width:
        return False
    if self.vehicles != other.vehicles:
        return False
    if self.walls != other.walls:
        return False
    return True