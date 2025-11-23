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
        self.size_x = 8
        self.size_y = 8
        #playerは中心座標で考えることとする
        self.x = x
        self.x_min = screen_width // 2 - 50
        self.x_max = screen_width // 2 + 50
        self.y = y
        self.speed = 5
        

    def update(self):
        
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed

        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed

        self.x = max(self.x_min + self.size_x // 2, min(self.x, self.x_max - self.size_x // 2))



    def draw(self):
        pyxel.blt(self.x - self.size_x // 2, self.y - self.size_y // 2, 0, 0, 0, self.size_x, self.size_y, pyxel.COLOR_BLACK)
        #pyxel.rect(screen_width // 2, screen_height // 2, 40, 40, pyxel.COLOR_PINK)

        pyxel.text(15, 15, f"player_x{self.x}", pyxel.COLOR_GREEN)
        pyxel.text(15, 25, f"player_y{self.y}", pyxel.COLOR_GREEN)

class Bullet:
    pass


class App:
    def __init__(self):
        pyxel.init(screen_width, screen_height, title = "scroll_game")
        pyxel.load("my_resource.pyxres")
        #Playerクラスでは引数にしたx,y座標がそのままplayerの中心座標となるように計算してくれるようにした。
        self.player = Player(screen_width // 2, screen_height // 2)
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        self.player.update()


    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 3, 10)
        pyxel.line(self.player.x_min, 0, self.player.x_min, screen_height, pyxel.COLOR_LIME)
        pyxel.line(self.player.x_max, 0, self.player.x_max, screen_height, pyxel.COLOR_LIME)



App()