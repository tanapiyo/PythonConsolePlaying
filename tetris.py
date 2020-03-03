import numpy as np

WIDTH = 6
HEIGHT = 20

def main():
    screen = np.zeros(HEIGHT + 2, WIDTH + 2) #枠があるので2ずつ追加
    screen#の1列めと1行め、-1も両方を◾️にする
    tetriminos = []
    #下にくるまでwhile, sleepしてテトリスのyを落とす、drawする
    #新しいテトリス投入

def start_new_game():
    pass

def draw_tetrimino():
    for i in range(HEIGHT+2):


def is_collided():
    pass

def is_aligned():
    pass #ループを回してallならTrue

def is_gameover():
    pass


@dataclasses.
class TetriminoParent():
#   mi.append(np.array([[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]])) 
#   mi.append(np.array([[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]])) 
#   mi.append(np.array([[1,0,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]])) 
#   mi.append(np.array([[0,0,0,1],[0,1,1,1],[0,0,0,0],[0,0,0,0]])) 
#   mi.append(np.array([[0,0,1,0],[0,1,1,1],[0,0,0,0],[0,0,0,0]])) 
#   mi.append(np.array([[1,1,0,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]])) 
#   mi.append(np.array([[0,0,1,1],[0,1,1,0],[0,0,0,0],[0,0,0,0]])) 

class Tetrimino(TetriminoParent):
    def __init__():
        self.x = (WIDTH+2)/2
        self.y = 0
        self.rotation = 0#rand() % N_TETRIS
    
    def rotate():
        pass

    def move_left():
        pass

    def move_right():
        pass

    def move_down():
        pass

if __name__ == "__main__":
    while True:
        pass