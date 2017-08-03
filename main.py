# Version: Feb 23th
#   Group 7: Dream Dog

#   Update: Sprinting implemented
#   - Minor level dfficulty increase: Dog doubles!
#   - Menu screen, story sequence, and win/lose screen
#   - Timer implemented with UI dog bone fill timer
#   - Puppy moves and causes accidents
#   - Player can pick up items to clean up accidents
#       - no more than 2 items held at a time
#       - Drawn in two different planes, menu and in game

#   Future Implementations:
#   - Ghost to follow player
#   - Player "cleanup" animation
#   - Full screen play
#   - Background music

#   Problems:
#   - Items need to unequip after single use, currently stays in menu
#   - Player could pick up any object in object class, meaning the trashcan is equippable
#   - Puppy animation is not working
#   - How to make the player rect box appear at the bottom of image rather than top?

#   Credits:
#   - Menu screen design by nebelhom
# https://nebelprog.wordpress.com/2013/08/14/create-a-simple-game-menu-with-pygame-pt-1-writing-the-menu-options-to-the-screen/
#
#

import pygame
import random
import sys
from classes import Player, Puppy, Objects, Path, vector2

SCREEN_width = 1024
SCREEN_height = 768
object_color_warning = (255, 0, 0)  # RED
object_color_idle = (0, 137, 68)  # GREEN
object_color_active = (0, 0, 255)  # BLUE
last_rand = random.randint(0, 5)


#   GAME METHODS    ##############################
def intro():
    # Mouse mover works but only lights up whole menu rather than 1 portion
    # For now, press enter to continue to game. Later a mouse click will work

    intro_screen = pygame.image.load("Intro_ScreenLogo.png").convert()
    intro_menu = pygame.image.load("Intro_ScreenMenuIdle.png").convert()

    menu_size = [int(x * 1) for x in intro_menu.get_size()]  # x * [size rescaling]
    menu_rect = pygame.Rect(0, 572, menu_size[0], menu_size[1])

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

        if menu_rect.collidepoint(pygame.mouse.get_pos()):
            intro_menu = pygame.image.load("Intro_MenuHoverClick.png").convert()
            if evt.type == pygame.MOUSEBUTTONDOWN:
                running = False
        else:
            intro_menu = pygame.image.load("Intro_ScreenMenuIdle.png").convert()

        screen.blit(intro_screen, (0, 0))
        screen.blit(intro_menu, (0, 572))
        pygame.display.flip()
    return
# End of Intro Screen ---------------------------------------


def story():
    first = pygame.image.load("Story1.png").convert()
    second = pygame.image.load("Story2.png").convert()
    third = pygame.image.load("Story3.png").convert()
    fourth = pygame.image.load("Story4.png").convert()
    fifth = pygame.image.load("Story5.png").convert()

    screen_counter = 1

    story_running = True
    while story_running:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    screen_counter += 1

        if screen_counter == 1:
            screen.blit(first, (0, 0))
        elif screen_counter == 2:
            screen.blit(second, (0, 0))
        elif screen_counter == 3:
            screen.blit(third, (0, 0))
        elif screen_counter == 4:
            screen.blit(fourth, (0, 0))
        elif screen_counter == 5:
            screen.blit(fifth, (0, 0))

        if screen_counter >= 6:
            story_running = False

        pygame.display.flip()

    return
# End of Story Sequence -------------------------------------


def game_over(path_list):
    result = False
    for path in path_list:
        if path.status == 'warning':
            result = True

    if result:
        end_screen = pygame.image.load("GameOverScreen.png").convert()
    else:
        end_screen = pygame.image.load("GameOverScreen_Win.png").convert()

    running = True
    while running:
        # get user events
        pygame.event.pump()
        for event in pygame.event.get():
            # print(evt) #   Prints all key and mouse events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True

        screen.blit(end_screen, (0, 0))
        pygame.display.flip()


#  Game Loop main intro ##################
def game_loop(game_level):

    room = pygame.image.load("Living RoomWithStuff.png").convert()  # Living Room.jpg")
    menu = pygame.image.load("BoxWithElements.png").convert_alpha()
    # Menu is 1025 x 196
    timer_offset = 0
    menu_timer_fill = pygame.image.load("Timer.png").convert()
    menu_timer_background = pygame.image.load("WhiteBox.png").convert()
    menu_objective = pygame.image.load("Controls.png").convert()

    start_time = pygame.time.get_ticks()  # Time from the beginning of execution
    cycle_time = pygame.time.get_ticks()  # Time of each cycle or loop iteration
    time_counter = 0

    #ghost_guy = ghost("boo.png")
    # Player Sprite declaration ##############
    player_position = vector2(352, 114)
    player_sprite = Player("WalkingSheet.png", player_position)

    #   Object declaration, spray ID = 01, tape ID = 02, dog_toy ID = 03
    spray = Objects("SprayDarkLine.png", vector2(820, 444), 01)
    tape = Objects("Object_Tape.png", vector2(630, 280), 02)
    dog_toy = Objects("Object_DogToy.png", vector2(400, 530), 03)
    dog_bags = Objects("Object_DogBag.png", vector2(160, 308), 04)
    trash_can = Objects("Object_TrashCan.png", vector2(0, 450), 05)

    # Stores all objects into object_list
    #object_list = [spray, tape, dog_toy, dog_bags, trash_can]
    object_list = [spray, dog_bags]

    # Path declaration, 6 points for dog to travel too
    path_list = [Path(vector2(750, 510), vector2(60, 40)),
                 Path(vector2(160, 528), vector2(60, 40)),
                 Path(vector2(350, 400), vector2(60, 40)),
                 Path(vector2(550, 340), vector2(60, 40)),
                 Path(vector2(620, 500), vector2(60, 40)),
                 Path(vector2(250, 340), vector2(60, 40))]

    #   Puppy declaration and setup
    puppy_position = path_list[0].pos
    puppy_speed = vector2(0, 0)
    puppy_sprite = Puppy("dogresized.png", puppy_position, puppy_speed)

    # Pup clone: Better to start together or sep?
    puppy_position2 = path_list[2].pos
    puppy_speed2 = vector2(0, 0)
    puppy_sprite2 = Puppy("dogresized.png", puppy_position, puppy_speed2)

    pup_list = [puppy_sprite]

    if game_level >= 2:
        pup_list.append(puppy_sprite2)

    # Sets object status as active for first puppy path
    for pup in pup_list:
        pup.change_path(path_list)

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

            sprinting = False
            # Not sure if this is correct   ########
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    pygame.quit
                    sys.exit()
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
                # Equip items tree
                if evt.key == pygame.K_j:
                    player_sprite.looking_for_item = True
                else:
                    player_sprite.looking_for_item = False
            else:
                player_sprite.moving = False
        # Pressed keys are assigned an action
        keys_pressed = pygame.key.get_pressed()
        #   Movement speed increase with 'sprint'
        if keys_pressed[pygame.K_w]:
            player_sprite.moving = True
            player_sprite.timer = 0
            player_sprite.side = 3
            player_sprite.move(0, -4, sprinting)
        if keys_pressed[pygame.K_s]:
            player_sprite.moving = True
            player_sprite.timer = 0
            player_sprite.side = 0
            player_sprite.move(0, 4, sprinting)
        if keys_pressed[pygame.K_a]:
            player_sprite.moving = True
            player_sprite.timer = 0
            player_sprite.side = 2
            player_sprite.move(-4, 0, sprinting)
        if keys_pressed[pygame.K_d]:
            player_sprite.moving = True
            player_sprite.timer = 0
            player_sprite.side = 1
            player_sprite.move(4, 0, sprinting)
        if keys_pressed[pygame.K_k]:
            player_sprite.cleanup = True
        else:
            player_sprite.cleanup = False

# SIMULATION  ---------------------------
# UPDATE
        end = pygame.time.get_ticks()
        delta_time = end - cycle_time
        cycle_time = end

        # Game Timer functions
        counting_time = pygame.time.get_ticks() - start_time
        counting_seconds = int(counting_time % 60000 / 1000)
        # print(counting_seconds)

        # Using get_ticks, counting seconds currently times game
        if counting_seconds != time_counter:
            time_counter += 1
            timer_offset += 5
            # If the timer has exceeded 59 seconds, game over screen
            if counting_seconds == 59:
                game_running = False
                return path_list

        # Checks if player is touching any objects, works
        for obj in object_list:
            player_sprite.update(obj, delta_time)

        for pup in pup_list:
            # Moves towards active target, returns True if reached
            if pup.move(delta_time):
                # Set new active area when destination reached
                print("Reached point, in Main loop")
                for path in path_list:
                    path.update(pup)
                pup.change_path(path_list)

        # Is the player in the path area for cleanup
        for path in path_list:
            if path.status == 'warning':
                path.update(player_sprite)



# DRAW SECTION (from back to front) Room, paths, player, Pup, menu, objects##################
        screen.blit(room, (0, 0))

        # Draws each object to room
        for path in path_list:
            path.draw(screen)

        # draws the unequipped items
        for obj in object_list:
            if not obj.item_held:
                obj.draw(screen)

        player_sprite.draw(screen)
        for pup in pup_list:
            pup.draw(screen)

        screen.blit(menu_timer_background, (5, 584))
        screen.blit(menu_timer_fill, (5 - timer_offset, 594))
        # 305 x 146
        # 1 sec 5 pixel
        screen.blit(menu, (0, 572))
        screen.blit(menu_objective, (782, 628))

        #draws equipped items
        for obj in object_list:
            if obj.item_held:
                obj.draw(screen)

        pygame.display.flip()


#   Main game code ####################################
pygame.init()

# 1024 x 768
level = 1
screen = pygame.display.set_mode((1024, 768))  # pygame.FULLSCREEN
pygame.display.set_caption("Doggie Doodies")
screen.fill((255, 255, 0))

#Game Intro Screen
intro()

#ds Game Story
story()

try_again = True
while try_again:
    # Main Game
    game_results = game_loop(level)
    try_again = game_over(game_results)
    level += 1
