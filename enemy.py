from math import dist

from entity import Entity
from states import Stat
from manaLoot import ManaLoot
from utils import vector_len


class Enemy(Entity):
    def __init__(self, pos, hitbox_size, image_list, speed=2, health=0, max_health=0, detect_range=200):
        super().__init__(pos, hitbox_size, image_list, speed, health, max_health)
        self.detect_range = detect_range
        self.player_pos = None
        self.dist = 30

    def update(self, board):
        super().update(board)
        if self.stats[Stat.Health] <= 0:
            board.add_projectile(ManaLoot(self.pos, 20))
            return
        vecx, vecy = board.player.x - self.x, board.player.y - self.y
        dist_to_player = vector_len((vecx, vecy))
        if self.player_pos and dist_to_player <= self.dist:
            return
        if board.has_clear_sight(self) and dist_to_player < self.detect_range:
            self.player_pos = board.player.pos
            if vecx > vecy:
                self.looking_direction = (1, 0)
            else:
                self.looking_direction = (0, 1)
        if self.player_pos:
            if dist(self.player_pos, self.pos) <= self.stats[Stat.Speed]:
                self.player_pos = None
            else:
                self.move_coords(self.player_pos[0] - self.x, self.player_pos[1] - self.y, own_speed=True)
