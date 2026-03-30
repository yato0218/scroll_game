import pyxel
import math

screen_width = 400
screen_height = 300

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAME_OVER = 2

PLAYER_SIZE_X = 8
PLAYER_SIZE_Y = 8
PLAYER_SPEED = 5

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_frame_num = 4
        self.frame_interval = 30
        
        
    def update(self):
        #sin cos でルート2走法を禁止できるんじゃね？ sin^2+cos^2 = 1とか？
        direction_x = 0
        direction_y = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            direction_x += 1
        if pyxel.btn(pyxel.KEY_LEFT):
            direction_x += -1
        if pyxel.btn(pyxel.KEY_UP):
            direction_y += -1
        if pyxel.btn(pyxel.KEY_DOWN):
            direction_y += 1

        lengh = math.sqrt(math.pow(direction_x,2) + math.pow(direction_y,2))

        if direction_x != 0:
            self.x += (direction_x  / lengh) * PLAYER_SPEED
        if direction_y != 0:
            self.y += (direction_y  / lengh) * PLAYER_SPEED


    def draw(self):

        self.player_current_frame = (pyxel.frame_count // self.frame_interval) % self.player_frame_num
        u = self.player_current_frame * 8
        pyxel.blt(self.x, self.y, 0, u, 0, PLAYER_SIZE_X, PLAYER_SIZE_Y, pyxel.COLOR_BLACK)
        # pyxel.blt(x, y, img, u, v, w, h, colkey=None, rotate=0, scale=1)
        #text(x, y, s, col, font=None)
        pyxel.text(10,10, f"self.x : {self.x}", pyxel.COLOR_LIME)
        if pyxel.btn(pyxel.KEY_RIGHT):
            pyxel.text(10,10, f"R", pyxel.COLOR_LIME)
        if pyxel.btn(pyxel.KEY_LEFT):
            pyxel.text(20,10, f"L", pyxel.COLOR_LIME)

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