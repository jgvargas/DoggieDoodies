# Version: Feb 19th
#   Group 7: Dream Dog

#   Update: Sprinting implemented
#   - Menu screen
#   - Timer implemented w/out UI dog bone fill timer
#   - Puppy moves but doesnt have accidents

#   Future Implementations:
#   - Game replay-able
#   - Player cleanup interaction

#   Problems:
#   - Walking animation seems to be getting slower as more assets being used
#   - Puppy.move is working but when the same point is given move stops
#   - Puppy animation is not working
#   - How to make the player rect box appear at the bottom of image rather than top?

#   Credits:
#   - Menu screen design by nebelhom
# https://nebelprog.wordpress.com/2013/08/14/create-a-simple-game-menu-with-pygame-pt-1-writing-the-menu-options-to-the-screen/
#   - Health Bar by Emmett Tomai
#     @ http://faculty.utrgv.edu/emmett.tomai/courses/3370/mod1/refs/health/health.py.txt

import pygame
import random
import sys
from classes import Player, Puppy, Objects, Path, vector2

SCREEN_width = 1024
SCREEN_height = 768
object_color_warning = (255, 0, 0)  # RED
object_color_idle = (0, 137, 68)  # GREEN
object_color_active = (0, 0, 255)  # BLUE


#   GAME METHODS    ##############################
def change_point(point_list):
    ran_num = random.randint(0, 5)

    # If the point is already active, choose a different point
    if point_list[ran_num].status == 'active':
        ran_num = random.randint(0, 5)

    print(ran_num)
    point_list[ran_num].color = object_color_warning
    point_list[ran_num].status = 'active'
    return


def intro():
    intro_screen = pygame.image.load("Intro_ScreenLogo.png")
    intro_menu = pygame.image.load("Intro_ScreenMenuIdle.png")
    intro_menu_highlighted = pygame.image.load("Intro_MenuHoverClick.png")

    running = True
    while running:
        # get user events
        pygame.event.pump()
        for evt in pygame.event.get():
            # print(evt) #   Prints all key and mouse events
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                pygame.quit
                sys.exit()

        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_RETURN:
                running = False

        screen.blit(intro_screen, (0, 0))
        screen.blit(intro_menu, (0, 572))
        pygame.display.flip()


def game_over(path_list):
    result = False
    for path in path_list:
        if path.status == 'active':
            result = True

    if result:
        end_screen = pygame.image.load("GameOverScreen.png")
    else:
        end_screen = pygame.image.load("WinningScreen.png")

    screen.blit(end_screen, (0, 0))
    pygame.display.flip()

    pygame.time.wait(2000)


def game_loop():
    room = pygame.image.load("Living RoomWithStuff.png")  # Living Room.jpg")
    menu = pygame.image.load("BoxWithElements.png").convert_alpha()
    # Menu is 1025 x 196

    ###########################

    start_time = pygame.time.get_ticks()  # Time from the beginning of execution
    cycle_time = pygame.time.get_ticks()  # Time of each cycle or loop iteration
    time_counter = 0

    # Player Sprite declaration ##############
    player_position = vector2(352, 114)
    player_sprite = Player("WalkingSheet.png", player_position)

    #   Object declaration
    spray = Objects("Object_Spray.png", vector2(200, 430))
    tape = Objects("Object_Tape.png", vector2(300, 330))
    dog_toy = Objects("Object_DogToy.png", vector2(400, 530))

    # Stores all objects into object_list
    object_list = [spray, tape, dog_toy]

    # Path declaration, 6 points for dog to travel too
    path_list = [Path(vector2(750, 300), vector2(40, 40)),
                 Path(vector2(110, 370), vector2(40, 40)),
                 Path(vector2(304, 420), vector2(40, 40)),
                 Path(vector2(750, 300), vector2(40, 40)),
                 Path(vector2(620, 100), vector2(40, 40)),
                 Path(vector2(250, 250), vector2(40, 40))]

    # Sets object status as active for first puppy path
    change_point(path_list)

    #   Puppy declaration and setup
    puppy_position = path_list[0].pos
    puppy_speed = vector2(0, 0)
    puppy_sprite = Puppy("DogSpriteSpreadfinal.png", puppy_position, puppy_speed)

    # Game loop setup
    frame_clock = pygame.time.Clock()
    FPS = 60
    game_running = True

    while game_running:
        frame_clock.tick(FPS)
        # get user events
        pygame.event.pump()
        for evt in pygame.event.get():
            # print(evt) #   Prints all key and mouse events
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                pygame.quit
                sys.exit()

            sprinting = False
            player_sprite.moving = False
            # Not sure if this is correct   ########
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_w:  # Up
                    player_sprite.moving = True
                elif evt.key == pygame.K_s:
                    player_sprite.moving = True
                elif evt.key == pygame.K_a:
                    player_sprite.moving = True
                elif evt.key == pygame.K_d:
                    player_sprite.moving = True
                elif evt.key == pygame.K_SPACE:
                    sprinting = True

        # Pressed keys are assigned an action
        keys_pressed = pygame.key.get_pressed()
        #   Movement speed increase with 'sprint'

        if keys_pressed[pygame.K_w]:
            player_sprite.timer = 0
            player_sprite.side = 3
            player_sprite.move(0, -4, sprinting)
        if keys_pressed[pygame.K_s]:
            player_sprite.timer = 0
            player_sprite.side = 0
            player_sprite.move(0, 4, sprinting)
        if keys_pressed[pygame.K_a]:
            player_sprite.timer = 0
            player_sprite.side = 2
            player_sprite.move(-4, 0, sprinting)
        if keys_pressed[pygame.K_d]:
            player_sprite.timer = 0
            player_sprite.side = 1
            player_sprite.move(4, 0, sprinting)

# SIMULATION  ---------------------------
        # UPDATE simulation
        end = pygame.time.get_ticks()
        delta_time = end - cycle_time
        cycle_time = end

        # Checks if player is touching any objects
        for obj in object_list:
            player_sprite.update(obj, delta_time)

        # Finds active spot for puppy to travel too
        for path in path_list:
            if path.status == 'active':
                puppy_sprite.target = path.pos
                path.status = 'idle'
                path.color = object_color_idle
                break

        # Moves towards active target
        if puppy_sprite.move(delta_time):
            # Set new active area when destination reached
            print("Reached point")
            change_point(path_list)

        # Game Timer functions
        counting_time = pygame.time.get_ticks() - start_time
        counting_seconds = int(counting_time % 60000 / 1000)
        # print(counting_seconds)

        # Using get_ticks, counting seconds currently times game
        if counting_seconds != time_counter:
            time_counter += 1
            # If the timer has exceeded 59 seconds, game over screen
            if counting_seconds == 59:
                game_running = False
                game_over(path_list)

# DRAW SECTION (from back to front)##################
        screen.blit(room, (0, 0))

        # Draws each object to room
        for path in path_list:
            path.draw(screen)

        for obj in object_list:
            obj.draw(screen)

        # Puppy sprite is not allowing the room to be redrawn
        puppy_sprite.draw(screen)
        player_sprite.draw(screen)
        screen.blit(menu, (0, 572))
        pygame.display.flip()


#   Main game code #########################
pygame.init()

screen = pygame.display.set_mode((1024, 768))  # 1024 x 768
pygame.display.set_caption("Doggie Doodies")
screen.fill((255, 255, 0))

#Game Intro Screen
intro()

# Main Game
game_loop()
