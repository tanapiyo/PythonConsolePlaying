import numpy as np
from enum import Enum
import sys
import time
import copy


WIDTH = 6
# HEIGHT = 20
HEIGHT = 10
MAX_TETRIMINO_SIZE = 4

class Game():
    def __init__(self):
        #スクリーンの初期化
        #self.screen_size = [WIDTH+2, HEIGHT+2]#枠があるので2ずつ追加
        self.screen_size = [HEIGHT, WIDTH]
        self.screen = self.init_board()

        #テトリミノの初期化
        self.tetrimino = self.__create_next_tetrimino()
        self.draw()

    '''
    スクリーンの作成と壁の作成
    '''
    def init_board(self):
        screen = np.zeros(self.screen_size, dtype=np.int)
        # #枠は2で埋める
        # #screen[0] = 2
        # screen[-1] = 2 
        # screen[:,0] = 2 #列の指定 
        # screen[:,-1] = 2
        return screen

    '''
    テトリミノを固定するかの判定
    '''
    def __is_collided(self):
        #テトリミノの下が壁もしくはテトリミノかどうかの判定
        for i in range(MAX_TETRIMINO_SIZE):#y
            for j in range(MAX_TETRIMINO_SIZE):#x
                if self.tetrimino.tetorimino[i][j] == 1 and (self.tetrimino.y+i>=HEIGHT-1 or self.screen[self.tetrimino.y+i+1][self.tetrimino.x+j] == 1):
                    print("collide")
                    return True
        return False

    '''
    テトリミノを動かすことができるかの判定
    '''
    def __can_move(self, direction):
        if direction == "left":
            left_outline = []#高さごとの一番左のindex
            #テトリミノの外枠の左があいているか
            #列ごとに一番左の1の一を探す
            for line in self.tetrimino.tetorimino:
                result = np.where(line==1)
                if len(result[0])>0:
                    left_outline.append(result[0][0])
                else:
                    left_outline.append(-1)
            for i, outline in enumerate(left_outline):
                if outline == -1:
                    continue
                if outline+self.tetrimino.x<=0 or self.screen[self.tetrimino.y+i][self.tetrimino.x+outline-1] == 1:
                    return False
            return True

            
        elif direction == "right":
            right_outline = []
            #テトリミノの外枠の右があいているか
            #列ごとに一番左の1の一を探す
            for line in self.tetrimino.tetorimino:
                result = np.where(line==1)
                if len(result[0])>0:
                    left_outline.append(result[0][-1])
                else:
                    left_outline.append(-1)
            for i, outline in enumerate(left_outline):
                if outline == -1:
                    continue
                if outline+self.tetrimino.x>=WIDTH-1 or self.screen[self.tetrimino.y+i][self.tetrimino.x+outline+1] == 1:
                    return False
            return True

        elif direction == "down":
            down_outline = []
            result = np.any(self.tetrimino.tetorimino==1, axis=0)
            temp_transporsed_tetrimino = self.tetrimino.tetorimino.T
            for line in temp_transporsed_tetrimino:
                result = np.where(line==1)
                if len(result[0])>0:
                    down_outline.append(result[0][-1])#一番下が一番右にあたる（∵転置している）ので-1をとる
                else:
                    down_outline.append(-1)

            for i, outline in enumerate(down_outline):
                if outline == -1:
                    continue
                if outline+self.tetrimino.y>=HEIGHT-1 or self.screen[self.tetrimino.y+outline+1][self.tetrimino.x+i] == 1:
                    return False
            return True

    '''
    横一列揃っているかの判定
    '''
    def __is_aligned_and_delete(self):
        for i, line in enumerate(self.screen):
            if np.all(line):#壁を除く要素が全て1、つまりブロックなら
                np.delete(self.screen, i, 0)#一旦その行を消す
                np.append(np.zeros[WIDTH], self.screen)#先頭に0を追加

    '''
    ゲームオーバー判定
    今回は左上に必ずテトリミノをおくので、左上に隙間がなければゲームオーバー
    '''
    def __is_gameover(self):
        counter = 0
        blank = 0
        for i in range(WIDTH):
            if self.screen[0][i] == 1:
                counter = counter + 1
                if counter >= 4:
                    return True
            else:
                blank += 1
                if blank >= 4:
                    counter = 0
                    blank = 0
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
            self.__reflect_tetrimino_to_screen()
        else:#ぶつかっていなければ1つ下げる
            self.__down_tetrimino()
        #もし一列揃っていたら消す
        self.__is_aligned_and_delete()
        self.draw()
        return True
    

    '''
    テトリミノとスクリーンを描画する
    '''
    def draw(self):
        # screen = self.screen.copy()
        # screen = np.where(screen == 0, "□", screen)#何もない
        # screen = np.where(screen == 1, "◼", screen)#テトリミノ
        # screen = np.where(screen == '2', "＃", screen)#壁
        screen_buffer = copy.deepcopy(self.screen)
        for i in range(MAX_TETRIMINO_SIZE):#y
            for j in range(MAX_TETRIMINO_SIZE):#x
                if self.tetrimino.tetorimino[i][j] == 1:
                    screen_buffer[self.tetrimino.y+i][self.tetrimino.x+j] = self.tetrimino.tetorimino[i][j]
        print(screen_buffer)
        print("\n\n\n\n\n")
    
    '''
    self.tetriminoをスクリーンに反映して、新しいtetriminoをインスタンス変数に入れる
    （スクリーンに反映＝スクリーンに同化）
    '''
    def __reflect_tetrimino_to_screen(self):
        #1行ずつself.screenをテトリミノで置き換え
        for i in range(MAX_TETRIMINO_SIZE):#y
            for j in range(MAX_TETRIMINO_SIZE):#x
                if self.tetrimino.tetorimino[i][j] == 1:
                    self.screen[self.tetrimino.y+i][self.tetrimino.x+j] = self.tetrimino.tetorimino[i][j]
        self.tetrimino = self.__create_next_tetrimino()
    '''
    テトリミノを下げる
    '''
    def __down_tetrimino(self):
        if self.__can_move("down"):
            #一番上のテトリミノがいたところは0に戻す
            for x_index in range(MAX_TETRIMINO_SIZE):
                if(self.tetrimino.tetorimino[0][x_index] == 1):
                    self.screen[self.tetrimino.y][self.tetrimino.x+x_index] = 0
            #テトリミノ自体の位置を下げる
            self.tetrimino.y = self.tetrimino.y+1
            # #テトリミノを下げた座標でscreenを更新
            # for i in range(MAX_TETRIMINO_SIZE):#y
            #     for j in range(MAX_TETRIMINO_SIZE):#x
            #         if self.tetrimino.tetorimino[i][j] == 1:
            #             self.screen[self.tetrimino.y+i][self.tetrimino.x+j] = self.tetrimino.tetorimino[i][j]
                

    '''
    テトリミノ操作
    '''
    def move_left(self):
        if self.__can_move("left"):
            self.tetrimino.move_left()
            self.draw()
    
    def move_right(self):
        if self.__can_move("right"):
            self.tetrimino.move_right()
            self.draw()
    
    def move_down(self):
        if self.__can_move("down"):
            self.tetrimino.move_down()
            self.draw()

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
        self.x = 0
        self.y = 0
        self.tetorimino = tetrimino_kind.tetrimino_list[kind]
        self.rotate(rotation)#回転させる
        
    def rotate(self, rotation):#テトリミノ自体を回転して返す
        for i in range(rotation):
            self.tetorimino = np.rot90(self.tetorimino, -1)

    def move_left(self):
        self.x = self.x - 1

    def move_right(self):
        self.x = self.x + 1

    def move_down(self):
        self.y = self.y + 1

    

import fcntl
import termios
# import sys
import os

def getkey():
    fno = sys.stdin.fileno()

    #stdinの端末属性を取得
    attr_old = termios.tcgetattr(fno)

    # stdinのエコー無効、カノニカルモード無効
    attr = termios.tcgetattr(fno)
    attr[3] = attr[3] & ~termios.ECHO & ~termios.ICANON # & ~termios.ISIG
    termios.tcsetattr(fno, termios.TCSADRAIN, attr)

    # stdinをNONBLOCKに設定
    fcntl_old = fcntl.fcntl(fno, fcntl.F_GETFL)
    fcntl.fcntl(fno, fcntl.F_SETFL, fcntl_old | os.O_NONBLOCK)

    chr = 0

    try:
        # キーを取得
        c = sys.stdin.read(1)
        if len(c):
            while len(c):
                chr = (chr << 8) + ord(c)
                c = sys.stdin.read(1)
    finally:
        # stdinを元に戻す
        fcntl.fcntl(fno, fcntl.F_SETFL, fcntl_old)
        termios.tcsetattr(fno, termios.TCSANOW, attr_old)

    return chr



if __name__ == "__main__":
    game = Game()#ゲームの初期化

    while True:#1秒ごとに描画
        kb = getkey()
     
        #キー入力があればテトリミノの操作処理
        # if kb == "122":#下,z
        #     print("down")
        #     game.move_down()
        # elif kb == "100":#右,d
        #     print("right")
        #     game.move_right()
        # elif kb == "97":#左,a
        #     print("left")
        #     game.move_left()
        # elif kb == "113":#for debug, q
        #     break

        a = input()
        if(a == "a"):
            print("左")
            game.move_left()
        elif a == "d":
            print("右")
            game.move_right()
        elif a == "z":
            print("した")
            game.move_down()


        #テトリミノを落とす・新しいテトリミノを作る
        is_gamecontinue = game.do_game_loop()

        if not is_gamecontinue:
            break

        #time.sleep(1)
    
    print("Game Over!")

