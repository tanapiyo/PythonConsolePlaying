import numpy as np
from enum import Enum
import readchar
import sys
import time

WIDTH = 6
HEIGHT = 20
MAX_TETRIMINO_SIZE = 4

class Game():
    def __init__(self):
        #スクリーンの初期化
        #self.screen_size = [WIDTH+2, HEIGHT+2]#枠があるので2ずつ追加
        self.screen_size = [WIDTH+2, HEIGHT+1]
        self.screen = self.init_board()

        #テトリミノの初期化
        self.tetriminos = [self.__create_next_tetrimino()]
        self.__reflect_tetrimino_to_screen()
        self.draw()

    '''
    スクリーンの作成と壁の作成
    '''
    def init_board(self):
        screen = np.zeros(self.screen_size, dtype=np.int)
        #枠は2で埋める
        #screen[0] = 2
        screen[-1] = 2 
        screen[:,0] = 2 #列の指定 
        screen[:,-1] = 2
        return screen

    '''
    テトリミノを固定するかの判定
    '''
    def __is_collided(self):
        #テトリミノの下が壁もしくはテトリミノかどうかの判定
        for i in range(MAX_TETRIMINO_SIZE):
            if self.screen[self.tetriminos[-1].y][self.tetriminos[-1].x+i] == 2:
                return True
            if self.screen[self.tetriminos[-1].y][self.tetriminos[-1].x+i] == 1:
                return True
        return False

    '''
    テトリミノを動かすことができるかの判定
    '''
    def __can_move(self, direction):
        if direction == "left":
            if self.screen[self.tetriminos[-1].y][self.tetriminos[-1].x-1] in [1,2]:
                return False
            return True
        elif direction == "right":
            if self.screen[self.tetriminos[-1].y][self.tetriminos[-1].x+1] in [1,2]:
                return False
            return True
        elif direction == "down":
            for i in range(MAX_TETRIMINO_SIZE):
                if self.screen[self.tetriminos[-1].y+1][self.tetriminos[-1].x+i] in [1,2]:
                    return False
            return True

    '''
    横一列揃っているかの判定
    '''
    def __is_aligned(screen):
        for line in self.screen:
            if np.all(line[1:-2]):#壁を除く要素が全て1、つまりブロックなら
                return True
        return False

    '''
    ゲームオーバー判定（もし最後のテトリミノの上が空いていなければ）
    とりあえず残りが2行になったらゲームーオーバー
    '''
    def __is_gameover(self):
        counter = 0
        for i in range(1, WIDTH+1):
            if self.screen[0][i] in [1,2]:
                counter = counter + 1
                if counter >= 4:
                    return True
        return False


    '''
    ランダムな回転と種類のテトリミノを作成する
    '''
    def __create_next_tetrimino(self):
        rotation = np.random.randint(MAX_TETRIMINO_SIZE)
        kind = np.random.randint(7)
        return Tetrimino(rotation, kind)
    
    '''
    メインからループの中で呼ばれるゲームの処理
    テトリミノを下に動かす、テトリミノを固定する、新しいテトリミノを生成する
    '''
    def do_game_loop(self):
        if self.__is_gameover():
            return False
        if self.__is_collided():#ぶつかっていたら新しいテトリミノを作る
            self.tetriminos.append(self.__create_next_tetrimino())
            self.__reflect_tetrimino_to_screen()
        else:#ぶつかっていなければ1つ下げる
            self.tetriminos[-1].y = self.tetriminos[-1].y+1
        self.draw()
        return True
        

    '''
    数値をそれっぽく描画する
    '''
    def draw(self):
        # screen = self.screen.copy()
        # screen = np.where(screen == 0, "□", screen)#何もない
        # screen = np.where(screen == 1, "◼", screen)#テトリミノ
        # screen = np.where(screen == '2', "＃", screen)#壁
        print(self.screen)
    
    '''
    self.tetriminosの最後の要素をself.screenに反映する
    '''
    def __reflect_tetrimino_to_screen(self):
        #for tetrimino in self.tetriminos:
        tetrimino = self.tetriminos[-1]
        print("a")
        print(tetrimino)
        print(self.tetriminos)
        #1行ずつself.screenをテトリミノで置き換え
        for i in range(MAX_TETRIMINO_SIZE):#y
            for j in range(MAX_TETRIMINO_SIZE):#x
                self.screen[tetrimino.y+i][int(tetrimino.x)+MAX_TETRIMINO_SIZE] = tetrimino.tetorimino[i][j]

    '''
    テトリミノ操作
    '''
    def move_left(self):
        if not __can_move("left"):
            self.tetriminos[-1].move_left()
    
    def move_right(self):
        if not __can_move("right"):
            self.tetriminos[-1].move_right()
    
    def move_down(self):
        if not __can_move("down"):
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
        if kb == "BB":#下
            game.move_down()
        elif kb == "CC":#右
            game.move_right()
        elif kb == "DD":#左
            game.move_left()
        elif kb == "q":#for debug
            break
        
        #テトリミノを落とす・新しいテトリミノを作る
        is_gamecontinue = game.do_game_loop()

        if not is_gamecontinue:
            break

        time.sleep(0.5)
    
    print("Game Over!")