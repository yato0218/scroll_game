import pyxel
import math
import random

screen_width = 400
screen_height = 300

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAME_OVER = 2

bullets = []
BULLET_SIZE_X = 8
BULLET_SIZE_Y = 8
BULLET_SPEED_X = 10

enemies = []
ENEMIES_MAX_NUM = 4
ENEMY_SIZE_X = 20
ENEMY_SIZE_Y = 20

PLAYER_SIZE_X = 16
PLAYER_SIZE_Y = 16
PLAYER_SPEED = 5
PLAYER_JUMP = 12
GRAVITY = 9.8
dt = 0.1

#今後もBulletクラスのようなリストで管理しないといけないようなたくさんのオブジェクト生成が予想される場合,クラスごとに上記のfor文を
#書かずに済むようにする.Enemyクラスなどを作るかもしれないしな
def entities_update(entities):
        for entity in entities:
            entity.update()

def entities_draw(entities):
        for entity in entities:
            entity.draw()
            pyxel.text(10, 40, f"bullets: {len(bullets)}", pyxel.COLOR_GREEN)

def entities_is_crash(entities_1, entities_2):
        for entity_1 in entities_1:
            for entity_2 in entities_2:
                if not entity_1.is_alive or not entity_2.is_alive:
                    continue
                if (entity_1.x <= entity_2.x + entity_2.w and
                    entity_2.x <= entity_1.x + entity_1.w and
                    entity_1.y <= entity_2.y + entity_2.h and
                    entity_2.y <= entity_1.y + entity_1.h):
                    entity_1.is_alive = False
                    entity_2.is_alive = False

def entities_cleanup(entities):
    # entities[:]は引数entitiesのリストの中身を全部出して,右側の値([]の中身)をentitiesのリストに入れなおすというものである
    # = [a for b in c if xxx] について. これは cというリストから1つ取り出し,bと名付ける. その後,xxxの条件に当てはまるものをaに変換してに入れる
    # そして,右辺を丸ごと囲む[]はリスト.そして[]にaを入れる.
    # aはbと同じものを入れるとentitiesから取り出したentityのなかで条件式を満たすentityがそのまま右辺の[]に入る.
    # a.xとしたり,a.x * 2などとするとentityが持っているxというインスタンス変数を右辺の[]に入れたり,その2倍の値を入れることができる
    entities[:] = [entity for entity in entities if entity.is_alive]
    # entities[:] = [entity.x for entity in entities if entity.is_alive]



class Bullet:
    def __init__(self, x, y, right):
        self.x = x
        self.y = y
        self.w = BULLET_SIZE_X
        self.h = BULLET_SIZE_Y
        self.is_right = right
        self.is_alive = True
        if self.is_right:
            self.direction_x = 1
        else:
            self.direction_x = -1
        
        bullets.append(self)

    def update(self):
        if self.is_alive:
            self.x += BULLET_SPEED_X * self.direction_x

        if not 0 < self.x < screen_width:
            self.is_alive = False
        if not 0 < self.y < screen_height:
            self.is_alive = False
        


    def draw(self):
        if self.is_alive:
            if self.is_right:
                pyxel.blt(self.x, self.y, 1, 0, 0, self.w, self.h, pyxel.COLOR_BLACK)
            else:
                pyxel.blt(self.x, self.y, 1, 0, 0, -self.w, self.h, pyxel.COLOR_BLACK)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_SIZE_X
        self.h = ENEMY_SIZE_Y
        self.is_alive = True
        enemies.append(self)
    def update(self):
        pass
           
    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, pyxel.COLOR_LIGHT_BLUE)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_SIZE_X
        self.h = PLAYER_SIZE_Y
        self.player_frame_num = 4
        self.frame_interval = 8
        self.vy = 0
        self.pre_vx = 0
        self.vx = 0

        self.is_right = True

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
            self.is_right = True
        if pyxel.btn(pyxel.KEY_LEFT):
            direction_x += -1
            self.is_right = False
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
            if self.is_right:
                Bullet(self.x + self.w, self.y + self.h // 4, self.is_right)
            else:
                Bullet(self.x - self.w // 2, self.y + self.h // 4, self.is_right)

        if pyxel.frame_count % 60 == 0:
            if len(enemies) <= ENEMIES_MAX_NUM:
                Enemy(random.randint(screen_width // 10 * 7, screen_width // 10 * 9),
                      random.randint(screen_height // 10 * 5, screen_height // 10 * 7))
                 

        
        


    def draw(self):
        if self.vx == 0 and self.is_right and self.vy == 0:
            self.player_current_frame = (pyxel.frame_count // self.frame_interval) % self.player_frame_num
            u = self.player_current_frame * 16
            pyxel.blt(self.x, self.y, 0, u, 0, self.w, self.h, pyxel.COLOR_BLACK)
        elif self.vx == 0 and not self.is_right and self.vy == 0:
            self.player_current_frame = (pyxel.frame_count // self.frame_interval) % self.player_frame_num
            u = self.player_current_frame * 16
            pyxel.blt(self.x, self.y, 0, u, 0, - self.w, self.h, pyxel.COLOR_BLACK)
        elif self.vx >= 0 and self.is_right:
            pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, pyxel.COLOR_BLACK)
        elif self.vx <= 0 and not self.is_right:
            pyxel.blt(self.x, self.y, 0, 0, 0, - self.w, self.h, pyxel.COLOR_BLACK)#キャラの向きを左右反転させるため-self.w
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

        
        self.background.update()
        self.player.update()

        

        #一応これは残しておく.Bulletクラスのオブジェクトたちは生成されたときにbullets.appendでbulletsリストへ入っている。
        # このリストはBulletクラスのオブジェクトが入っているため、forでbulletという変数の箱にbulletsのリストを1つずつ入れ
        #.update()とするとBulletクラスのupdate()が呼び出される.
        # for bullet in bullets:
        #     bullet.update()
        
        
        #上記のbulletクラスのupdate()の使い方を踏まえて,関数をつくる.
        #今後もBulletクラスのようなリストで管理しないといけないようなたくさんのオブジェクト生成が予想される場合,クラスごとに上記のfor文を
        #書かずに済むようにする.Enemyクラスなどを作るかもしれないしな
        entities_is_crash(bullets, enemies)
        entities_update(bullets)
        entities_update(enemies)
        
        
        entities_cleanup(enemies)
        entities_cleanup(bullets)
        

        
        
        

        

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

        

        entities_draw(bullets)
        # for bullet in bullets:
        #     bullet.draw()
        entities_draw(enemies)

    def draw_game_over_scene(self):
        pyxel.text(screen_width // 7 * 3, screen_height // 2, f"Game Over", pyxel.COLOR_LIME)
        






        

App()