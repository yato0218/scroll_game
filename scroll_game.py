import pyxel

screen_width = 400
screen_height = 300

class Background:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class Player:
    def __init__(self, x, y):
        self.x = x
        self.x_min = screen_width // 2 - 50
        self.x_max = screen_width // 2 + 50 -4
        
        self.y = y
        self.speed = 5
        self.right = 0
        self.left = 0

    def update(self):
        self.x = min(self.x, self.x_max)
        self.x = max(self.x_min, min(self.x, self.x_max))
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.right += 1

        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.left += 1

        # if screen_width // 2 - 50 > self.x:
        #     self.x = screen_width // 2 - 50

        # if self.x > screen_width // 2 + 50:
        #     self.x = screen_width // 2 + 50



    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, pyxel.COLOR_BLACK)
        #pyxel.rect(screen_width // 2, screen_height // 2, 40, 40, pyxel.COLOR_PINK)

        pyxel.text(15, 15, f"right{self.right}", pyxel.COLOR_GREEN)
        pyxel.text(15, 25, f"right{self.left}", pyxel.COLOR_GREEN)

class Bullet:
    pass


class App:
    def __init__(self):
        pyxel.init(screen_width, screen_height, title = "scroll_game")
        pyxel.load("my_resource.pyxres")
        self.player = Player(screen_width // 2, screen_height // 2)
        pyxel.mouse = True

        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        self.player.update()


    def draw(self):
        pyxel.cls(0)
        self.player.draw()



App()