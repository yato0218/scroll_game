import pyxel

screen_width = 400
screen_height = 300

class Player:
    def __init__(self, x, y):
        self.size_x = 8
        self.size_y = 8
        self.x = x  # これはワールド全体の座標
        self.y = y
        self.speed = 5
        # 画面内の動ける範囲（この範囲を超えるとスクロール）
        self.margin_left = 100
        self.margin_right = 300

    def update(self, scroll_x):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            
        # 左端に行き過ぎないように制限
        self.x = max(self.x, self.size_x // 2)

        # プレイヤーの画面上での座標を計算して、スクロール量を決める
        self.display_x = self.x - scroll_x
        
        if self.display_x > self.margin_right:
            scroll_x = self.x - self.margin_right
        elif self.display_x < self.margin_left:
            scroll_x = max(0, self.x - self.margin_left)

        # プレイヤーの画面上での座標を計算して、スクロール量を決める
        self.display_x = self.x - scroll_x
            
        return scroll_x
    
        

    def draw(self, display_x):
        # 描画するときだけscroll_xを引く
        pyxel.blt(self.display_x - self.size_x // 2, self.y - self.size_y // 2, 0, 0, 0, self.size_x, self.size_y, pyxel.COLOR_BLACK)
        pyxel.line(100, 0, 100, screen_height, pyxel.COLOR_ORANGE)
        pyxel.line(300, 0, 300, screen_height, pyxel.COLOR_ORANGE)

class Background:
    def __init__(self, player):
        self.player = player

    def draw(self, scroll_x):
        pyxel.cls(0)
        # スクロールを確認するための目印（地面や柱など）
        # 40ピクセルごとに線を引く例
        for i in range(20):
            line_x = i * 100 - (scroll_x % 100) # ループ背景のテクニック
            pyxel.line(line_x, 0, line_x, screen_height, pyxel.COLOR_LIME)
        
        pyxel.text(15, 15, f"scroll_x: {scroll_x}", pyxel.COLOR_GREEN)
        pyxel.text(15, 25, f"display_x: {self.player.display_x}", pyxel.COLOR_GREEN)
        pyxel.text(15, 35, f"self.x   : {self.player.x}", pyxel.COLOR_GREEN)
class App:
    def __init__(self):
        pyxel.init(screen_width, screen_height, title="side_scroll_game")
        pyxel.load("my_resource.pyxres") # リソースがある場合は有効に
        self.player = Player(screen_width // 2, screen_height // 2)
        self.background = Background(self.player)
        self.scroll_x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        # updateから新しいscroll_xを受け取る
        self.scroll_x = self.player.update(self.scroll_x)

    def draw(self):
        self.background.draw(self.scroll_x)
        self.player.draw(self.scroll_x)

App()