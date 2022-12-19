from entity import Entity
from move import Move
from states import Stat
from utils import normalize, load_image
from sword import Sword
from gun import Gun


class Player(Entity):
    def __init__(self, pos, hitbox_size, image_list, speed, max_health=100, max_mana=100):
        super().__init__(pos, hitbox_size, image_list, speed, max_health, max_health)
        self.dash_cooldown = 40
        self.dash_current_cooldown = 0
        self.dash_speed = 3
        self.weapon = Sword([load_image('sword', 'sword.png', color_key='white')], self)
        self.abbility = Gun([load_image('sword', 'sword.png', color_key='white')], self)
        self.try_attack = False
        self.try_sec_attack = False
        self.stats[Stat.Mana] = max_mana
        self.stats[Stat.MaxMana] = max_mana
        self.looking_direction = (1, 1)

    def render(self, surf, camera_x, camera_y):
        self.weapon.render(surf, camera_x, camera_y)
        super().render(surf, camera_x, camera_y)

    def secondary_attack(self):
        self.try_sec_attack = True

    def attack(self):
        self.try_attack = True

    def calc_movement(self):
        dx = 0
        dy = 0
        for mov in self.move_q:
            if mov.own_speed:
                sx, sy = normalize(*mov.pos)
                dx += sx * self.stats[Stat.Speed] * (1 - self.dash_current_cooldown / self.dash_cooldown) ** 0.5
                dy += sy * self.stats[Stat.Speed] * (1 - self.dash_current_cooldown / self.dash_cooldown) ** 0.5
                continue
            dx += mov.dx
            dy += mov.dy
        for i in self.move_q:
            i.update()
        self.move_q = [i for i in self.move_q if i.duration > 0]
        return dx, dy

    def update(self, board):
        super().update(board)
        self.dash_current_cooldown = max(0, self.dash_current_cooldown - 1)
        self.weapon.update()
        self.abbility.update()
        if self.try_attack:
            self.weapon.attack(board)
            self.try_attack = False
        if self.try_sec_attack:
            self.abbility.attack(board)
            self.try_sec_attack = False

    def move_input(self, x, y):
        # self.looking_direction = (x, y)
        self.move_coords(x, y, own_speed=True)

    def dash(self, dx, dy):
        dx, dy = normalize(dx, dy)
        if self.dash_current_cooldown:
            return
        self.dash_current_cooldown = self.dash_cooldown
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 10))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 7))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 4))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 2))
