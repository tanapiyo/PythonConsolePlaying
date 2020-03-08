import numpy as np
from enum import Enum
import readchar
import sys
import time

WIDTH = 6
HEIGHT = 20

class Game():
    def __init__(self):
        #スクリーンの初期化
        self.screen_size = [WIDTH+2, HEIGHT+2]#枠があるので2ずつ追加
        self.screen = self.init_board()

        #テトリミノの初期化
        self.tetriminos = [self.__create_next_tetrimino()]
        self.__reflect_tetrimino_to_screen()
        print(self.screen)
        self.draw()

    def init_board(self):
        screen = np.zeros(self.screen_size, dtype=np.int)
        #枠は2で埋める
        screen[0] = 2
        screen[-1] = 2 
        screen[:,0] = 2 #列の指定 
        screen[:,-1] = 2
        return screen

    def __is_collided():
        pass

    '''
    横一列揃っているかの判定
    '''
    def __is_aligned(screen):
        for line in self.screen:
            if np.all(line[1:-2]):#壁を除く要素が全て1、つまりブロックなら
                return True
        return False

    def __is_gameover():
        pass

    def __create_next_tetrimino(self):
        rotation = np.random.randint(4)
        kind = np.random.randint(7)
        tetorimino = Tetrimino(rotation, kind)
    
    def do_game_loop(self):
        if __is_gameover():
            return False
        pass#テトリミノ落とす＋新しいの作る

    '''
    数値をそれっぽく描画する
    '''
    def draw(self):
        #self.tetriminosをscreenに描画
        print(self.screen)
    
    '''
    self.tetriminosをself.screenに反映する
    '''
    def __reflect_tetrimino_to_screen(self):
        for tetrimino in self.tetriminos:
            print(tetrimino)

    '''
    テトリミノ操作
    '''
    def move_left(self):
        if not __is_collided:
            self.tetriminos[-1].move_left()
    
    def move_right(self):
        if not __is_collided:
            self.tetriminos[-1].move_right()
    
    def move_down(self):
        if not __is_collided:
            self.tetriminos[-1].move_down()

class TetriminoKind():
    def __init__(self):
        self.tetrimino_list = [np.array([[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]]),#I
        np.array([[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]),#O
        np.array([[1,0,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]]),#J
        np.array([[0,0,0,1],[0,1,1,1],[0,0,0,0],[0,0,0,0]]),#L
        np.array([[0,0,1,0],[0,1,1,1],[0,0,0,0],[0,0,0,0]]),#T
        np.array([[1,1,0,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]]),#S
        np.array([[0,0,1,1],[0,1,1,0],[0,0,0,0],[0,0,0,0]])]#Z
  

class Tetrimino():
    def __init__(self, rotation, kind):
        tetrimino_kind = TetriminoKind()
        self.x = (WIDTH+2)/2 - 2 #左上
        self.y = 0
        self.tetorimino = tetrimino_kind.tetrimino_list[kind]
        self.rotate(rotation)#回転させる
        
    def rotate(self, rotation):#テトリミノ自体を回転して返す
        print(vars(self))
        for i in range(rotation):
            self.tetorimino = np.rot90(self.tetorimino, -1)

    def move_left():
        self.x = self.x - 1

    def move_right():
        self.x = self.x + 1

    def move_down():
        self.y = self.y + 1

    

if __name__ == "__main__":
    game = Game()#ゲームの初期化
    while True:#1秒ごとに描画
        kb = readchar.readchar()
        sys.stdout.write(kb)
        
        #キー入力があればテトリミノの操作処理
        if kb == "AA":#上
            break
        elif kb == "BB":#下
            pass
        elif kb == "CC":#右
            pass
        elif kb == "DD":#左
            pass
        elif kb == "q":#for debug
            break
        
        #描画処理
        game.draw()
        #テトリミノを落とす・新しいテトリミノを作る
        is_gamecontinue = game.do_game_loop()

        if not is_gamecontinue:
            break

        time.sleep(0.5)
    
    print("Game Over!")