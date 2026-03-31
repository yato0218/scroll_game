import pyxel
import math

screen_width = 400
screen_height = 300

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAME_OVER = 2

bullets = []
BULLET_SIZE_X = 8
BULLET_SIZE_Y = 8

PLAYER_SIZE_X = 16
PLAYER_SIZE_Y = 16
PLAYER_SPEED = 5
PLAYER_JUMP = 12
GRAVITY = 9.8
dt = 0.1

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        bullets.append(self)

    def update(self):
        self.x += 10
    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, 0, BULLET_SIZE_X, BULLET_SIZE_Y, pyxel.COLOR_BLACK)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_frame_num = 4
        self.frame_interval = 8
        self.vy = 0
        self.pre_vx = 0
        self.vx = 0

        self.right = True

        #init以外の関数で使う場合、selfを入れること
        self.jump_count = 0
        self.jump_max = 2
        
        
        
    def update(self):
        #sin cos でルート2走法を禁止できるんじゃね？ sin^2+cos^2 = 1とか？
        direction_x = 0
        direction_y = 0
        self.pre_vx = self.vx
        self.vx = 0
        

        if pyxel.btn(pyxel.KEY_RIGHT):
            direction_x += 1
            self.right = True
        if pyxel.btn(pyxel.KEY_LEFT):
            direction_x += -1
            self.right = False
        if self.jump_count < self.jump_max:
            if pyxel.btnp(pyxel.KEY_UP):
                #最初は self.vy -= PLAYER_JUMP としていたが、これでは2回目のジャンプ時にプレイヤーが上昇中か下降中かでself.vyの状態が違うため2回目のジャンプの度合いが一定ではなくなる
                self.vy = - PLAYER_JUMP
                self.jump_count += 1


        self.vy += GRAVITY * dt
        self.y += self.vy
        
        if self.y >= screen_height // 6 * 5:
            self.y = screen_height // 6 * 5
            self.vy = 0
        
            self.jump_count = 0
        

        lengh = math.sqrt(math.pow(direction_x,2) + math.pow(direction_y,2))

        if direction_x != 0:   #これは毎ループdirection_x,yが0になってるから0で割らないようにする工夫
            self.pre_vx = self.vx
            self.vx = (direction_x  / lengh) * PLAYER_SPEED #(direction_x  / lengh)はcosθ
            self.x += self.vx

        if pyxel.btn(pyxel.KEY_SPACE):
            Bullet(self.x + PLAYER_SIZE_X, self.y + PLAYER_SIZE_Y // 4)


        
        


    def draw(self):
        if self.vx == 0 and self.right and self.vy == 0:
            self.player_current_frame = (pyxel.frame_count // self.frame_interval) % self.player_frame_num
            u = self.player_current_frame * 16
            pyxel.blt(self.x, self.y, 0, u, 0, PLAYER_SIZE_X, PLAYER_SIZE_Y, pyxel.COLOR_BLACK)
        elif self.vx == 0 and not self.right and self.vy == 0:
            self.player_current_frame = (pyxel.frame_count // self.frame_interval) % self.player_frame_num
            u = self.player_current_frame * 16
            pyxel.blt(self.x, self.y, 0, u, 0, - PLAYER_SIZE_X, PLAYER_SIZE_Y, pyxel.COLOR_BLACK)
        elif self.vx >= 0 and self.right:
            pyxel.blt(self.x, self.y, 0, 0, 0, PLAYER_SIZE_X, PLAYER_SIZE_Y, pyxel.COLOR_BLACK)
        elif self.vx <= 0 and not self.right:
            pyxel.blt(self.x, self.y, 0, 0, 0, -PLAYER_SIZE_X, PLAYER_SIZE_Y, pyxel.COLOR_BLACK)#キャラの向きを左右反転させるため-PLAYER_SIZE_X
        # pyxel.blt(x, y, img, u, v, w, h, colkey=None, rotate=0, scale=1)
        #text(x, y, s, col, font=None)
        pyxel.text(10,10, f"self.x : {self.x}", pyxel.COLOR_LIME)
        pyxel.text(10,20, f"self.vx : {self.vx}", pyxel.COLOR_LIME)
        pyxel.text(10,30, f"self.y : {self.y}", pyxel.COLOR_LIME)

class Background:
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass



class App:
    def __init__(self):
        pyxel.init(screen_width, screen_height, title = "scroll_game")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        self.player = Player(screen_width // 3, screen_height // 5 * 2)
        self.background = Background()


        self.scene = SCENE_TITLE

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAME_OVER:
            self.update_game_over_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.scene = SCENE_PLAY
    def update_play_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.scene = SCENE_GAME_OVER

        for bullet in bullets:
            bullet.update()
        
        self.background.update()
        self.player.update()

        

    def update_game_over_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.scene = SCENE_TITLE
        


    





    def draw(self):
        pyxel.cls(0)

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAME_OVER:
            self.draw_game_over_scene()

    def draw_title_scene(self):
        pyxel.text(screen_width // 7 * 3, screen_height // 2, f"Click To Start", pyxel.COLOR_LIME)

    def draw_play_scene(self):
        pyxel.text(screen_width // 7 * 3, screen_height // 2, f"Play", pyxel.COLOR_LIME)

        self.background.draw()
        self.player.draw()
        
        for bullet in bullets:
            bullet.draw()

    def draw_game_over_scene(self):
        pyxel.text(screen_width // 7 * 3, screen_height // 2, f"Game Over", pyxel.COLOR_LIME)
        






        

App()