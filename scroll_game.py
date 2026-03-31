import pyxel
import math

screen_width = 400
screen_height = 300

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAME_OVER = 2

PLAYER_SIZE_X = 16
PLAYER_SIZE_Y = 16
PLAYER_SPEED = 5
PLAYER_JUMP = 12
GRAVITY = 9.8
dt = 0.1

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_frame_num = 4
        self.frame_interval = 30
        self.vy = 0
        #init以外の関数で使う場合、selfを入れること
        self.jump_count = 0
        self.jump_max = 2
        
        
        
    def update(self):
        #sin cos でルート2走法を禁止できるんじゃね？ sin^2+cos^2 = 1とか？
        direction_x = 0
        direction_y = 0

        if pyxel.btn(pyxel.KEY_RIGHT):
            direction_x += 1
        if pyxel.btn(pyxel.KEY_LEFT):
            direction_x += -1
        if self.jump_count < self.jump_max:
            if pyxel.btnp(pyxel.KEY_UP):
                self.vy -= PLAYER_JUMP
                self.jump_count += 1


        self.vy += GRAVITY * dt
        self.y += self.vy
        
        if self.y >= screen_height // 6 * 5:
            self.y = screen_height // 6 * 5
            self.vy = 0
            self.jump_count = 0
        

        lengh = math.sqrt(math.pow(direction_x,2) + math.pow(direction_y,2))

        if direction_x != 0:   #これは毎ループdirection_x,yが0になってるから0で割らないようにする工夫
            self.x += (direction_x  / lengh) * PLAYER_SPEED #(direction_x  / lengh)はcosθ

        
        


    def draw(self):

        self.player_current_frame = (pyxel.frame_count // self.frame_interval) % self.player_frame_num
        u = self.player_current_frame * 16
        pyxel.blt(self.x, self.y, 0, u, 0, PLAYER_SIZE_X, PLAYER_SIZE_Y, pyxel.COLOR_BLACK)
        # pyxel.blt(x, y, img, u, v, w, h, colkey=None, rotate=0, scale=1)
        #text(x, y, s, col, font=None)
        pyxel.text(10,10, f"self.x : {self.x}", pyxel.COLOR_LIME)
        pyxel.text(10,20, f"self.y : {self.y}", pyxel.COLOR_LIME)

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

    def draw_game_over_scene(self):
        pyxel.text(screen_width // 7 * 3, screen_height // 2, f"Game Over", pyxel.COLOR_LIME)
        






        

App()