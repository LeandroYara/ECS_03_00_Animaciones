

import math
import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_hunter_chase(world:esper.World, player_pos:pygame.Vector2, player_size:pygame.Vector2):
    HComponents = world.get_components(CTransform, CSurface, CVelocity, CTagHunter)
    
    player_center = pygame.Vector2(player_pos.x + (player_size[0] / 2),
                        player_pos.y + (player_size[1] / 2))
    for _, (ch_t, ch_s, ch_v, ch_tag) in HComponents:
        hunter_center = pygame.Vector2(ch_t.pos.x + (ch_s.area.width / 2),
                        ch_t.pos.y + (ch_s.area.height / 2))
        origin_center = pygame.Vector2(ch_tag.initial_pos.x + (ch_s.area.width / 2),
                        ch_tag.initial_pos.y + (ch_s.area.height / 2))
        dist_from_origin = math.sqrt((origin_center.x - hunter_center.x)**2 + (origin_center.y-hunter_center.y)**2)
        relative_area = CSurface.get_area_relative(ch_s.area, ch_t.pos)
        if ch_tag.active == False and relative_area.collidepoint(origin_center.x, origin_center.y):
            ch_v.vel.x = 0
            ch_v.vel.y = 0
            dist_player = math.sqrt((hunter_center.x-player_center.x)**2 + (hunter_center.y-player_center.y)**2)
            if dist_player <= ch_tag.dis_chase:
                ch_tag.active = True
        elif ch_tag.active and dist_from_origin <= ch_tag.dis_return:
            vel = (player_center - hunter_center)
            ch_v.vel = vel.normalize() * ch_tag.vel_chase
        elif ch_tag.active and dist_from_origin > ch_tag.dis_return:
            vel = origin_center - hunter_center
            ch_v.vel = vel.normalize() * ch_tag.vel_return
            ch_tag.active = False