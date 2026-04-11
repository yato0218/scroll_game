import pyxel
import math
import random

screen_width = 400
screen_height = 300

SCENE_TITLE = 0
SCENE_CONTROLS = 1
SCENE_PLAY = 2
SCENE_GAME_OVER = 3
SCENE_CLEAR = 4
 

bullets = []
BULLET_SIZE_X = 8
BULLET_SIZE_Y = 8
BULLET_SPEED_X = 10

boss = []
boss_MAX_NUM = 1
BOSS_SIZE_X = 64
BOSS_SIZE_Y = 60

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
            

def entities_check_collisions(entities_1, entities_2, hit_switch_1, hit_switch_2):
        for entity_1 in entities_1:
            for entity_2 in entities_2:
                if not entity_1.is_alive or not entity_2.is_alive:
                    continue
                if (entity_1.x <= entity_2.x + entity_2.w and
                    entity_2.x <= entity_1.x + entity_1.w and
                    entity_1.y <= entity_2.y + entity_2.h and
                    entity_2.y <= entity_1.y + entity_1.h):
                    if hit_switch_1 == True:
                        entity_1.is_collision = True
                    if hit_switch_2 == True:
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
        self.vx = 0
        self.vy = 0
        self.w = BOSS_SIZE_X
        self.h = BOSS_SIZE_Y
        self.is_collision = False
        self.is_alive = True
        self.hit_point = 15
        boss.append(self)
        self.frame_interval = 6
        self.current_frame = 0
        self.frame_num = 4
        self.current_state = 0
        self.neutral = 0
        self.attack1 = 1
        self.attack2 = 2
        self.guard = 3
        self.state_timer = 0
        self.damage_timer = 0

        self.gurad_distance = 100

        self.intro_timer = 90 # 1.5秒間動かない
        self.display_hp = 0   # ゲージを0からギュイーンと増やす用


    def update(self):

        if self.intro_timer > 0:
            self.intro_timer -= 1
            # HPゲージを徐々に増やす
            if self.display_hp < self.hit_point:
                self.display_hp += self.hit_point / 90
            # 待機モーションだけは再生しておく
            self.current_frame = (pyxel.frame_count // self.frame_interval) % self.frame_num
            return



        #-----------------大まかなモーションを書く
        if self.current_state == self.neutral:
            self.neutral_update()
        elif self.current_state == self.attack1:
            self.attack1_update()
        elif self.current_state == self.attack2:
            self.attack2_update()
        elif self.current_state == self.guard:
            self.guard_update()


        

        if self.is_collision:
            if self.current_state != self.guard:
                self.hit_point -= 1
                self.is_collision = False
                self.damage_timer = 15 #15フレーム点滅させる
                if self.hit_point > 0:
                    pyxel.play(2, 1)   #ダメージ音
            else:
                self.is_collision = False 
                pyxel.play(2, 4)          # ガード音

        if self.hit_point <= 0:
            self.is_alive = False
            
        # 点滅タイマーを減らす
        if self.damage_timer > 0:
            self.damage_timer -= 1

        tile_x = (self.x + self.w // 2) // 8
        tile_y = (self.y + self.h // 2) // 8

        tile_info = pyxel.tilemaps[0].pget(tile_x, tile_y)
        if tile_info == (0, 2) or tile_info == (0,3):
            self.y = tile_y * 8 - self.h
            self.vy = 0

        if len(players) > 0:
            distance_x = abs(players[0].x - self.x)
        if distance_x > self.gurad_distance:
            self.current_state = self.guard
        elif self.current_state == self.guard:
                self.current_state = self.neutral
                self.state_timer = 0


        self.vy += GRAVITY * dt
        self.y += self.vy

        tile_x = (self.x + self.w // 2) // 8
        tile_y = (self.y + self.h) // 8 # ※Bossの高さに合わせて調整

        tile_info = pyxel.tilemaps[0].pget(tile_x, tile_y)
        if tile_info == (0, 2)or tile_info == (0,3):
            self.y = tile_y * 8 - self.h
            self.vy = 0
        
        
        #-----------------

    def neutral_update(self):
        self.current_frame = (self.state_timer // self.frame_interval) % self.frame_num
        self.state_timer += 1
        if len(players) > 0:
            if players[0].x > self.x:
                self.vx = 1   # 右へ
            else:
                self.vx = -1  # 左へ
        self.x += self.vx

        #ランダムでジャンプ（1%の確率でピョンと跳ぶ）
        # ※ self.vy == 0 は地面にいるときの簡易判定
        if self.vy == 0 and random.randint(1, 10) == 1:
            self.vy = -8
        if self.state_timer >= 40:
            self.current_state = self.attack1
            self.state_timer = 0
            self.current_frame = 0
            
        
    
    def attack1_update(self):
        #frame_intervalフレームに1回,フレームが進む. つまりframe_intervalが10なら10フレームで1枚分,キャラの絵が変わる.
        #一連の動きのフレーム数が4なら,合計で40フレームないと一連の動きが描画しきれない
        self.current_frame = (self.state_timer // self.frame_interval) % self.frame_num 
        self.state_timer += 1
        if self.state_timer == 20:
            pyxel.play(3, 3)
            for i in range(15):
                Mud(random.randint(self.x + self.w // 2 - 50, self.x + self.w // 2 + 50), self.y)
        if self.state_timer >= 23:
            self.current_state = self.neutral
            self.state_timer = 0


    def attack2_update(self):
        #frame_intervalフレームに1回,フレームが進む. つまりframe_intervalが10なら10フレームで1枚分,キャラの絵が変わる.
        #一連の動きのフレーム数が4なら,合計で40フレームないと一連の動きが描画しきれない
        self.current_frame = (self.state_timer // self.frame_interval) % self.frame_num 
        self.state_timer += 1
        if self.state_timer == 20:
            for i in range(40):
                Mud(random.randint(self.x + self.w // 2 - 50, self.x + self.w // 2 + 50), self.y)
        if self.state_timer >= 23:
            self.current_state = self.neutral
            self.state_timer = 0

    def guard_update(self):
        self.current_frame = (self.state_timer // self.frame_interval) % self.frame_num
        self.state_timer += 1
            




           
    def draw(self):
            v = self.current_state * 64
            # もしガード状態なら
            if self.current_state == self.guard:
                v = 128
            if getattr(self, 'damage_timer', 0) > 0 and pyxel.frame_count % 4 < 2:
                pass # 点滅中はボスの姿を描かない！
            else:
                if players[0].x > self.x:
                    pyxel.blt(self.x, self.y + 8, 2, self.current_frame * BOSS_SIZE_X, v, + self.w, self.h, pyxel.COLOR_BLACK)   # 右へ
                else:
                    pyxel.blt(self.x, self.y +8, 2, self.current_frame * BOSS_SIZE_X, v, - self.w, self.h, pyxel.COLOR_BLACK)  # 左へ
                
            pyxel.text(screen_width // 10 * 6, 10, f"BOSS", pyxel.COLOR_PINK)
            pyxel.rect(screen_width // 10 * 6, 20, self.display_hp * 10, 10, pyxel.COLOR_PINK)
            # pyxel.text(10,90, f"player invincible_count : {self.invincible_count}", pyxel.COLOR_LIME)
            # pyxel.text(screen_width // 10 * 6, 10, f"BOSS", pyxel.COLOR_PINK)
            # # ★ hit_point ではなく display_hp を使って四角を描く！
            # pyxel.rect(screen_width // 10 * 6, 20, self.display_hp * 10, 10, pyxel.COLOR_PINK)
        

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
                pyxel.play(1, 1) # ダメージ音
                self.is_invincible = True
                self.invincible_count = 0
                
        else:
            self.invincible_count += 1
            self.is_collision = False
            
            
        if self.invincible_count >= self.invincible_time:
            self.is_invincible = False
            

        if self.hit_point <= 0:
            self.is_alive = False
            pyxel.play(1, 2) # やられた音

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
        if self.vy > 7:
            self.vy = 7
        self.y += self.vy
        # プレイヤーの足元の中央座標が、タイルマップの何マス目かを計算（8ピクセルで1マス）
        tile_x = (self.x + self.w // 2) // 8
        tile_y = (self.y + self.h) // 8

        # tilemaps[0] のそのマスに、Imageバンクのどのタイルが置かれているかを取得
        tile_info = pyxel.tilemaps[0].pget(tile_x, tile_y)

        if tile_info == (0, 2):
            self.y = tile_y * 8 - self.h
            self.vy = 0
        
            self.jump_count = 0
        

        lengh = math.sqrt(math.pow(direction_x,2) + math.pow(direction_y,2))

        if direction_x != 0:   #これは毎ループdirection_x,yが0になってるから0で割らないようにする工夫
            self.pre_vx = self.vx
            self.vx = (direction_x  / lengh) * PLAYER_SPEED #(direction_x  / lengh)はcosθ
            self.x += self.vx

        if  self.x + self.w >= screen_width:
            self.x = screen_width - self.w
        elif self.x < 0:
            self.x = 0

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):#ボタンYと書いてあるが、今のコントローラだとXボタンに当たる
            if self.is_right:
                pyxel.play(3, 10)
                Bullet(self.x + self.w, self.y + self.h // 4, self.is_right)
            else:
                pyxel.play(3, 10)
                Bullet(self.x - self.w // 2, self.y + self.h // 4, self.is_right)

        
        
                 

        
        


    def draw(self):
        pyxel.text(10,10, f"PLAYER HP : {self.hit_point}", pyxel.COLOR_LIME)
        for i in range(self.hit_point):
            pyxel.rect(15 * i + 20, 20, 10, 10, pyxel.COLOR_GREEN)
        
        if self.is_invincible and pyxel.frame_count % 4 < 2:
            pass # 何も描かない！
        else:
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
        self.mouse_x = 0
        self.mouse_y = 0
        pyxel.load("my_resource.pyxres")
        # self.player = Player(screen_width // 3, screen_height // 5 * 2)
        self.background = Background()


        self.stick_cooldown = 0
        self.scene = SCENE_TITLE
        self.menu_selection = SCENE_TITLE

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_RIGHTSTICK):
            pyxel.stop() # BGMや効果音を一旦リセット
            self.scene = SCENE_TITLE

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_CONTROLS:
            self.update_controls_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAME_OVER:
            self.update_game_over_scene()
        elif self.scene == SCENE_CLEAR:
            self.update_clear_scene()
        
        
        
        
        

    def update_title_scene(self):
        self.axis_y = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)
        self.start_color = pyxel.COLOR_NAVY
        self.controls_color = pyxel.COLOR_NAVY
        if self.menu_selection == SCENE_TITLE:
            self.start_color = pyxel.COLOR_YELLOW
        elif self.menu_selection == SCENE_CONTROLS:
            self.controls_color = pyxel.COLOR_YELLOW
        
        # スティックのクールダウンを減らす
        if self.stick_cooldown > 0:
            self.stick_cooldown -= 1
            # スティックを中央に戻したら、すぐに次動かせるようにする
            if abs(self.axis_y) < 5000:
                self.stick_cooldown = 0

        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or 10000 <= self.axis_y and self.stick_cooldown == 0:
            self.menu_selection -= 1
            pyxel.play(0, 0) # ★カーソル移動音
            if self.menu_selection < 0:
                self.menu_selection = 1
            self.stick_cooldown = 15
                
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or self.axis_y <= -10000 and self.stick_cooldown == 0:
            self.menu_selection += 1
            pyxel.play(0, 0) # ★カーソル移動音
            if self.menu_selection > 1:
                self.menu_selection = 0
            self.stick_cooldown = 15

        
        
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            pyxel.play(0, 0) # ★カーソル移動音
            if self.menu_selection == 0:
                self.reset_game()
                self.scene = SCENE_PLAY
            elif self.menu_selection == 1:
                self.scene = SCENE_CONTROLS

        
        
        

    def update_play_scene(self):
        # if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        #     self.scene = SCENE_GAME_OVER
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y

        if pyxel.frame_count % 60 == 0 and not hasattr(self, 'boss_spawned'):
            pass # 1回目の60フレーム目まで待つための工夫
        
        if len(boss) < boss_MAX_NUM and getattr(self, 'boss_spawned', False) == False:
            Boss(random.randint(screen_width // 10 * 4, screen_width // 10 * 5),
                 random.randint(screen_height // 10 * 7, screen_height // 10 * 8))
            self.boss_spawned = True
                
        self.background.update()

        
        

        

        #一応これは残しておく.Bulletクラスのオブジェクトたちは生成されたときにbullets.appendでbulletsリストへ入っている。
        # このリストはBulletクラスのオブジェクトが入っているため、forでbulletという変数の箱にbulletsのリストを1つずつ入れ
        #.update()とするとBulletクラスのupdate()が呼び出される.
        # for bullet in bullets:
        #     bullet.update()
        
        
        #上記のbulletクラスのupdate()の使い方を踏まえて,関数をつくる.
        #今後もBulletクラスのようなリストで管理しないといけないようなたくさんのオブジェクト生成が予想される場合,クラスごとに上記のfor文を
        #書かずに済むようにする.Enemyクラスなどを作るかもしれないしな
        entities_check_collisions(bullets, boss, hit_switch_1 = True, hit_switch_2 = True)
        entities_check_collisions(players, boss, hit_switch_1 = True, hit_switch_2 = False)#ここは[self.player]とするとplayerというオブジェクトをリストとして扱うことができる
        entities_check_collisions(boss_attacks, players, hit_switch_1 = True, hit_switch_2 = True)
        
        entities_update(bullets)
        entities_update(boss)
        entities_update(boss_attacks)
        #ボスが存在していて、かつイントロ中ならプレイヤーのupdateを呼ばない
        if len(boss) > 0 and boss[0].intro_timer > 0:
            pass # イントロ中はプレイヤーは動けない
        else:
            self.player.update() # 通常時は動ける

        if not self.player.is_alive:
            if self.scene != SCENE_GAME_OVER: # 1回だけ実行する工夫
                pyxel.stop()     # BGMを止める
                pyxel.play(0, 8) # ゲームオーバー音
            self.scene = SCENE_GAME_OVER

        # ボスを倒した時
        if getattr(self, 'boss_spawned', False) == True and len(boss) == 0:
            if self.scene != SCENE_CLEAR: # 1回だけ実行する工夫
                pyxel.stop()     # BGMを止める
                pyxel.play(0, 9) # クリア音
            self.scene = SCENE_CLEAR
        
        entities_cleanup(bullets)
        entities_cleanup(boss)
        entities_cleanup(boss_attacks)
        # entities_cleanup(players)
        
        

        
        
        

        

    def update_game_over_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            
            self.scene = SCENE_TITLE
    
    def update_clear_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.scene = SCENE_TITLE
    
    def update_controls_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.scene = SCENE_TITLE

    def reset_game(self):
        bullets.clear()
        boss.clear()
        boss_attacks.clear()
        players.clear()

        self.player = Player(screen_width // 3, 7* screen_height // 10)

        self.boss_spawned = False # ボス復活フラグ
        pyxel.playm(0, loop=True) # バトルBGMループ再生


        


    





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
        elif self.scene == SCENE_CLEAR: 
            self.draw_clear_scene()

    def draw_title_scene(self):
        pyxel.text(10,10, f"self.scene : {self.scene}", pyxel.COLOR_LIME)
        pyxel.text(10,20, f"self.menu_selection : {self.menu_selection}", pyxel.COLOR_RED)

        pyxel.rect(screen_width // 10 * 4, screen_height // 10 * 3, screen_width // 10 * 2, 20, self.start_color)
        pyxel.text(screen_width // 10 * 4 + 30, screen_height // 10 * 3 + 7, f"Start", pyxel.COLOR_RED)

        pyxel.rect(screen_width // 10 * 4, screen_height // 10 * 5, screen_width // 10 * 2, 20, self.controls_color)
        pyxel.text(screen_width // 10 * 4 + 30, screen_height // 10 * 5 + 7, f"Controls", pyxel.COLOR_RED)

    def draw_play_scene(self):
        pyxel.text(screen_width // 7 * 3 , screen_height // 6 * 3, f"mouse_x: {self.mouse_x}", pyxel.COLOR_LIME)
        pyxel.text(screen_width // 7 * 3 , screen_height // 6 * 2, f"mouse_y: {self.mouse_y}", pyxel.COLOR_LIME)
        

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

    def draw_clear_scene(self):
        pyxel.text(screen_width // 10 * 4, screen_height // 10 * 5, f"GAME CLEAR!!", pyxel.COLOR_YELLOW)
        pyxel.text(screen_width // 10 * 4, screen_height // 10 * 7, f"Press A or B to continue", pyxel.COLOR_LIME)

    def draw_controls_scene(self):
        pyxel.text(50, 50, "--- HOW TO PLAY ---", pyxel.COLOR_YELLOW)
        pyxel.text(50, 80, "Move  : D-PAD / Stick", pyxel.COLOR_WHITE)
        pyxel.text(50, 100, "Jump  : A Button", pyxel.COLOR_WHITE)
        pyxel.text(50, 120, "Shoot : X Button", pyxel.COLOR_WHITE)
        
        pyxel.text(50, 200, "Press Action Button to Return", pyxel.COLOR_GRAY)

    
                






        

App()