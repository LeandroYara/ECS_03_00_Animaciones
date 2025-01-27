import copy
import random
import pygame
import esper
from src.ecs.components.c_animation import CAnimation

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity

def create_sprite(world: esper.World, pos:pygame.Vector2, vel: pygame.Vector2,
                  surface:pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, 
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = pygame.image.load(enemy_info["image"]).convert_alpha()
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy())
    

def create_enemy_hunter(world: esper.World, pos: pygame.Vector2, enemy_info: dict) -> int:
    hunter_sprite = pygame.image.load(enemy_info["image"]).convert_alpha()
    size = hunter_sprite.get_size()
    size = (size[0] / enemy_info["animations"]["number_frames"], size[1])
    c_pos = pygame.Vector2(pos.x - (size[0] / 2),
                        pos.y - (size[1] / 2))
    vel = pygame.Vector2(0, 0)
    dis_chase = enemy_info["distance_start_chase"]
    dis_return = enemy_info["distance_start_return"]
    vel_chase = enemy_info["velocity_chase"]
    vel_return = enemy_info["velocity_return"]
    hunter_entity = create_sprite(world, c_pos, vel, hunter_sprite)
    nc_pos = copy.deepcopy(c_pos)
    world.add_component(hunter_entity, CTagHunter(dis_chase, dis_return, vel_chase, vel_return, nc_pos))
    world.add_component(hunter_entity, CAnimation(enemy_info["animations"]))
    world.add_component(hunter_entity, CHunterState())
    return hunter_entity


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    player_sprite = pygame.image.load(player_info["image"]).convert_alpha()
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size[0] / 2),
                         player_lvl_info["position"]["y"] - (size[1] / 2))
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_explosion(world:esper.World, entity_pos:pygame.Vector2, entity_size:pygame.Vector2, explosion_info:dict):
    explosion_sprite = pygame.image.load(explosion_info["image"])
    explosion_size = explosion_sprite.get_rect().size
    explosion_size = (explosion_size[0] / explosion_info["animations"]["number_frames"], explosion_size[1])
    pos = pygame.Vector2(entity_pos.x + (entity_size[0] / 2) - (explosion_size[0] / 2),
                         entity_pos.y + (entity_size[1] / 2) - (explosion_size[1] / 2))
    vel = pygame.Vector2(0, 0)
    explosion_entity = create_sprite(world, pos, vel, explosion_sprite)
    world.add_component(explosion_entity, CTagExplosion(0))
    world.add_component(explosion_entity, CAnimation(explosion_info["animations"]))
    return explosion_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()

    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up,
                        CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down,
                        CInputCommand("PLAYER_DOWN", pygame.K_DOWN))

    input_fire = world.create_entity()
    world.add_component(input_fire,
                        CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))


def create_bullet(world: esper.World,
                  mouse_pos: pygame.Vector2,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):
    bullet_surface = pygame.image.load(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
                         player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_info["velocity"]

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
