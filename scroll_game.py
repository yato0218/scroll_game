import pyxel
import math
import random

screen_width = 400
screen_height = 300

SCENE_TITLE = 0
SCENE_CONTROLS = 1
SCENE_PLAY = 2
SCENE_GAME_OVER = 3
 

bullets = []
BULLET_SIZE_X = 8
BULLET_SIZE_Y = 8
BULLET_SPEED_X = 10

boss = []
boss_MAX_NUM = 1
BOSS_SIZE_X = 64
BOSS_SIZE_Y = 64

boss_attacks = []

players = []
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
            

def entities_check_collisions(entities_1, entities_2):
        for entity_1 in entities_1:
            for entity_2 in entities_2:
                if not entity_1.is_alive or not entity_2.is_alive:
                    continue
                if (entity_1.x <= entity_2.x + entity_2.w and
                    entity_2.x <= entity_1.x + entity_1.w and
                    entity_1.y <= entity_2.y + entity_2.h and
                    entity_2.y <= entity_1.y + entity_1.h):
                    entity_1.is_collision = True
                    entity_2.is_collision = True
                
                    

                

def entities_cleanup(entities):
    # entities[:]は引数entitiesのリストの中身を全部出して,右側の値([]の中身)をentitiesのリストに入れなおすというものである
    # = [a for b in c if xxx] について. これは cというリストから1つ取り出し,bと名付ける. その後,xxxの条件に当てはまるものをaに変換してに入れる
    # そして,右辺を丸ごと囲む[]はリスト.そして[]にaを入れる.
    # aはbと同じものを入れるとentitiesから取り出したentityのなかで条件式を満たすentityがそのまま右辺の[]に入る.
    # a.xとしたり,a.x * 2などとするとentityが持っているxというインスタンス変数を右辺の[]に入れたり,その2倍の値を入れることができる
    entities[:] = [entity for entity in entities if entity.is_alive]
    # entities[:] = [entity.x for entity in entities if entity.is_alive]

class Mud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.randint(-10, 10)
        self.vy = -15
        self.w = 32
        self.h = 32
        self.is_collision = False
        self.is_alive = True
        boss_attacks.append(self)
        
    def update(self):
        self.vy += GRAVITY * dt
        self.y += self.vy
        self.x += self.vx
        if not 0 <= self.y <= screen_height:
            self.is_alive = False
        if not 0 <= self.x <= screen_width:
            self.is_alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, 16, self.w, self.h, pyxel.COLOR_BLACK)

class Bullet:
    def __init__(self, x, y, right):
        self.x = x
        self.y = y
        self.w = BULLET_SIZE_X
        self.h = BULLET_SIZE_Y
        self.is_right = right
        self.is_collision = False
        self.is_alive = True
        if self.is_right:
            self.direction_x = 1
        else:
            self.direction_x = -1
        
        bullets.append(self)

    def update(self):
        if self.is_collision:
            self.is_alive = False

        if self.is_alive:
            self.x += BULLET_SPEED_X * self.direction_x

        if not 0 < self.x < screen_width:
            self.is_alive = False
        if not 0 < self.y < screen_height:
            self.is_alive = False
        


    def draw(self):
        if self.is_right:
            pyxel.blt(self.x, self.y, 1, 0, 0, self.w, self.h, pyxel.COLOR_BLACK)
        else:
            pyxel.blt(self.x, self.y, 1, 0, 0, -self.w, self.h, pyxel.COLOR_BLACK)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self):
        pass
    def draw(self):
        pass

class Mob(Enemy):
    def __init(self, x, y):
        super().__init__(x, y)

    def update(self):
        pass
    def draw(self):
        pass

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.w = BOSS_SIZE_X
        self.h = BOSS_SIZE_Y
        self.is_collision = False
        self.is_alive = True
        self.hit_point = 10
        boss.append(self)
        self.frame_interval = 10
        self.current_frame = 0
        self.frame_num = 4
        self.current_state = 0
        self.neutral = 0
        self.attack1 = 1
        self.state_timer = 0
    def update(self):
        #-----------------大まかなモーションを書く
        if self.current_state == self.neutral:
            self.neutral_update()
        elif self.current_state == self.attack1:
            self.attack1_update()


        

        if self.is_collision:
            self.hit_point -= 1
            self.is_collision = False
        if self.hit_point <= 0:
            self.is_alive = False
        
        #-----------------

    def neutral_update(self):
        self.current_frame = (self.state_timer // self.frame_interval) % self.frame_num
        self.state_timer += 1
        if self.state_timer >= 40:
            self.current_state = self.attack1
            self.state_timer = 0
            self.current_frame = 0
            
        
    
    def attack1_update(self):
        self.current_frame = (self.state_timer // self.frame_interval) % self.frame_num
        self.state_timer += 1
        if self.state_timer == 30:
            for i in range(40):
                Mud(random.randint(self.x + self.w // 2 - 50, self.x + self.w // 2 + 50), self.y)
        if self.state_timer >= 40:
            self.current_state = self.neutral
            self.state_timer = 0
            




           
    def draw(self):
            pyxel.blt(self.x, self.y, 2, self.current_frame * BOSS_SIZE_X, self.current_state * 64, - self.w, self.h, pyxel.COLOR_BLACK)
            pyxel.text(screen_width // 10 * 6, 10, f"BOSS", pyxel.COLOR_PINK)
            pyxel.rect(screen_width // 10 * 6, 20, self.hit_point * 10, 10, pyxel.COLOR_PINK)
            # pyxel.text(10,90, f"player invincible_count : {self.invincible_count}", pyxel.COLOR_LIME)
        

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
        self.invincible_time = 70
        self.invincible_count = 0
        self.is_invincible = False

        self.is_right = True
        self.is_collision = False
        self.is_alive = True
        self.hit_point = 3

        players.append(self)

        #init以外の関数で使う場合、selfを入れること
        self.jump_count = 0
        self.jump_max = 2
        
        
        
    def update(self):

        if not self.is_invincible:
            if self.is_collision:
                self.hit_point -= 1
                self.is_invincible = True
                self.invincible_count = 0
                
        else:
            self.invincible_count += 1
            self.is_collision = False
            
            
        if self.invincible_count >= self.invincible_time:
            self.is_invincible = False
            

        if self.hit_point <= 0:
            self.is_alive = False

        # if not self.is_collision:
        #     self.is_collision = False
        #     self.is_alive = True
        

        #sin cos でルート2走法を禁止できるんじゃね？ sin^2+cos^2 = 1とか？
        direction_x = 0
        direction_y = 0
        self.pre_vx = self.vx
        self.vx = 0
        
        self.axis_x = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or self.axis_x > 10000:
            direction_x += 1
            self.is_right = True
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or self.axis_x < -10000:
            direction_x += -1
            self.is_right = False
        if self.jump_count < self.jump_max:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):#ボタンBと書いてあるが、今のコントローラだとAボタンに当たる
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

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):#ボタンYと書いてあるが、今のコントローラだとXボタンに当たる
            if self.is_right:
                Bullet(self.x + self.w, self.y + self.h // 4, self.is_right)
            else:
                Bullet(self.x - self.w // 2, self.y + self.h // 4, self.is_right)

        
        
                 

        
        


    def draw(self):
        pyxel.text(10,10, f"PLAYER HP : {self.hit_point}", pyxel.COLOR_LIME)
        for i in range(self.hit_point):
            pyxel.rect(15 * i, 20, 10, 10, pyxel.COLOR_GREEN)
        

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
        # pyxel.text(10,10, f"self.x : {self.x}", pyxel.COLOR_LIME)
        # pyxel.text(10,20, f"self.vx : {self.vx}", pyxel.COLOR_LIME)
        # pyxel.text(10,30, f"self.y : {self.y}", pyxel.COLOR_LIME)
        # pyxel.text(10, 40, f"bullets: {len(bullets)}", pyxel.COLOR_GREEN)
        # pyxel.text(10,50, f"player is_collision : {self.is_collision}", pyxel.COLOR_LIME)
        # pyxel.text(10,60, f"player is_alive : {self.is_alive}", pyxel.COLOR_LIME)
        # pyxel.text(10,70, f"player hit_point : {self.hit_point}", pyxel.COLOR_LIME)
        # pyxel.text(10,80, f"player is_invincible : {self.is_invincible}", pyxel.COLOR_LIME)
        # pyxel.text(10,90, f"player invincible_count : {self.invincible_count}", pyxel.COLOR_LIME)

class Background:
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, screen_width, screen_height, pyxel.COLOR_BLACK)



class App:
    def __init__(self):
        pyxel.init(screen_width, screen_height, title = "scroll_game")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        self.player = Player(screen_width // 3, screen_height // 5 * 2)
        self.background = Background()


        self.scene = SCENE_TITLE
        self.menu_selection = SCENE_TITLE

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_CONTROLS:
            self.update_controls_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAME_OVER:
            self.update_game_over_scene()
        
        
        
        
        

    def update_title_scene(self):
        self.axis_y = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)
        self.start_color = pyxel.COLOR_NAVY
        self.controls_color = pyxel.COLOR_NAVY
        if self.menu_selection == SCENE_TITLE:
            self.start_color = pyxel.COLOR_YELLOW
        elif self.menu_selection == SCENE_CONTROLS:
            self.controls_color = pyxel.COLOR_YELLOW


        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or 10000 <= self.axis_y:
            self.menu_selection -= 1
            if self.menu_selection < 0:
                self.menu_selection = 1
                
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or self.axis_y <= -10000:
            self.menu_selection += 1
            if self.menu_selection > 1:
                self.menu_selection = 0

        
        
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            if self.menu_selection == 0:
                self.scene = SCENE_PLAY
            elif self.menu_selection == 1:
                self.scene = SCENE_CONTROLS

        
        
        

    def update_play_scene(self):
        # if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        #     self.scene = SCENE_GAME_OVER
        
        if pyxel.frame_count % 60 == 0:
            if len(boss) < boss_MAX_NUM:
                Boss(random.randint(screen_width // 10 * 4, screen_width // 10 * 5),
                    random.randint(screen_height // 10 * 7, screen_height // 10 * 8))
                
        self.background.update()

        
        

        

        #一応これは残しておく.Bulletクラスのオブジェクトたちは生成されたときにbullets.appendでbulletsリストへ入っている。
        # このリストはBulletクラスのオブジェクトが入っているため、forでbulletという変数の箱にbulletsのリストを1つずつ入れ
        #.update()とするとBulletクラスのupdate()が呼び出される.
        # for bullet in bullets:
        #     bullet.update()
        
        
        #上記のbulletクラスのupdate()の使い方を踏まえて,関数をつくる.
        #今後もBulletクラスのようなリストで管理しないといけないようなたくさんのオブジェクト生成が予想される場合,クラスごとに上記のfor文を
        #書かずに済むようにする.Enemyクラスなどを作るかもしれないしな
        entities_check_collisions(bullets, boss)
        entities_check_collisions(players, boss)#ここは[self.player]とするとplayerというオブジェクトをリストとして扱うことができる
        entities_check_collisions(boss_attacks, players)
        
        entities_update(bullets)
        entities_update(boss)
        entities_update(boss_attacks)
        self.player.update()

        if not self.player.is_alive:
            self.scene = SCENE_GAME_OVER
        
        entities_cleanup(bullets)
        entities_cleanup(boss)
        entities_cleanup(boss_attacks)
        # entities_cleanup(players)
        
        

        
        
        

        

    def update_game_over_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.scene = SCENE_TITLE
    
    def update_controls_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.scene = SCENE_TITLE
        


    





    def draw(self):
        pyxel.cls(0)

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_CONTROLS:
            self.draw_controls_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAME_OVER:
            self.draw_game_over_scene()

    def draw_title_scene(self):
        pyxel.text(10,10, f"self.scene : {self.scene}", pyxel.COLOR_LIME)
        pyxel.text(10,20, f"self.menu_selection : {self.menu_selection}", pyxel.COLOR_RED)

        pyxel.rect(screen_width // 10 * 4, screen_height // 10 * 3, screen_width // 10 * 2, 20, self.start_color)
        pyxel.text(screen_width // 10 * 4 + 30, screen_height // 10 * 3 + 7, f"Start", pyxel.COLOR_RED)

        pyxel.rect(screen_width // 10 * 4, screen_height // 10 * 5, screen_width // 10 * 2, 20, self.controls_color)
        pyxel.text(screen_width // 10 * 4 + 30, screen_height // 10 * 5 + 7, f"Controls", pyxel.COLOR_RED)

    def draw_play_scene(self):
        pyxel.text(screen_width // 7 * 3 , screen_height // 2, f"Play", pyxel.COLOR_LIME)

        self.background.draw()
        self.player.draw()

        

        entities_draw(bullets)
        # for bullet in bullets:
        #     bullet.draw()
        entities_draw(boss)
        entities_draw(boss_attacks)

    def draw_game_over_scene(self):
        pyxel.text(screen_width // 10 * 4, screen_height // 10 * 5, f"Game Over", pyxel.COLOR_LIME)
        pyxel.text(screen_width // 10 * 4, screen_height // 10 * 7, f"Press A or B to continue", pyxel.COLOR_LIME)

    def draw_controls_scene(self):
        pyxel.text(50, 50, "--- HOW TO PLAY ---", pyxel.COLOR_YELLOW)
        pyxel.text(50, 80, "Move  : D-PAD / Stick", pyxel.COLOR_WHITE)
        pyxel.text(50, 100, "Jump  : A Button", pyxel.COLOR_WHITE)
        pyxel.text(50, 120, "Shoot : X Button", pyxel.COLOR_WHITE)
        
        pyxel.text(50, 200, "Press Action Button to Return", pyxel.COLOR_GRAY)
        






        

App()