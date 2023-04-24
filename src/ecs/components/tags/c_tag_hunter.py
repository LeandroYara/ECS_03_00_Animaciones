import pygame


class CTagHunter:
    def __init__(self, dis_chase: int, dis_return: int, vel_chase: int, vel_return: int, initial_pos: pygame.Vector2) -> None:
        self.dis_chase = dis_chase
        self.dis_return = dis_return
        self.vel_chase = vel_chase
        self.vel_return = vel_return
        self.initial_pos = initial_pos
        self.active = False