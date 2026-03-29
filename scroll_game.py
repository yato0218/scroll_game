import pyxel

screen_width = 400
screen_height = 300

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAME_OVER = 2

PLAYER_SIZE_X = 8
PLAYER_SIZE_Y = 8

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self):
        pass
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, PLAYER_SIZE_X, PLAYER_SIZE_Y, pyxel.COLOR_BLACK)
        # pyxel.blt(x, y, img, u, v, w, h, colkey=None, rotate=0, scale=1)
        #text(x, y, s, col, font=None)
        pyxel.text(10,10, f"Game Start", pyxel.COLOR_LIME)

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