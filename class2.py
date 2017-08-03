#   Player: Attributes
#       - Size(x,y), my_image, pos(x,y), rect
#   Puppy:
#   Objects:
#   Path:
#   Vector2: Operator overload for negating
#
import math
import pygame
import random

SCREEN_width = 1024
SCREEN_height = 768
object_color_warning = (255, 0, 0)  # RED
object_color_idle = (0, 137, 68)  # GREEN
object_color_active = (0, 0, 255)  # BLUE


# Contains: Image, position, velocity, and radius
class Player:
    def __init__(self, image_file, pos):
        pic = pygame.image.load(image_file).convert_alpha()
        self.MARGIN = 1  # how far away each action is left to right, ex width margin width
        self.IMG_W = 88  # size of action left to right
        self.size = [int(x * 1) for x in pic.get_size()]  # x * [size rescaling]
        self.my_image = pygame.transform.scale(pic, self.size)
        self.pos = pos
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.IMG_W, self.size[1] / 4)
        # Animation resources
        self.moving = False
        self.timer = 0
        self.frame = 0
        self.TIME = 60
        self.CT = 6  # Images per strip (row)
        self.side = 0  # Col on sprite sheet
        # Size of individual avatar action, margin =
        self.clip = pygame.Rect(self.MARGIN + self.IMG_W * self.frame, self.side * 230, self.IMG_W, 225)
        # Used for player equipped items
        self.item1 = 00
        self.item2 = 00
        self.looking_for_item = False
        self.item_count = 0

    def update(self, other_rect, delta):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.IMG_W, self.size[1] / 4)
        self.clip = pygame.Rect(self.MARGIN + self.IMG_W * self.frame, self.side * 230, self.IMG_W, 225)

        if self.moving:
            if self.timer > self.TIME:
                self.timer -= self.TIME
                self.frame = (self.frame + 1) % self.CT
            self.timer += 1
        else:
            self.frame = 0
            self.timer = 0

        # This decides whether a object is active = player on obj
        # or idle = player not on object
        if self.rect.colliderect(other_rect):
            # Player on space
            other_rect.color = object_color_active
            other_rect.status = 'active'

            if self.looking_for_item and self.item_count < 3:
                if self.item_count == 0:
                    # Store item_Id, set held to true, and up item counter
                    self.item1 = other_rect.item_id
                    other_rect.item_held = True
                    other_rect.menu_pos = 1
                    self.item_count += 1
                elif self.item_count == 1:
                    # Store item_Id, set held to true, and up item counter
                    self.item2 = other_rect.item_id
                    other_rect.item_held = True
                    other_rect.menu_pos = 2
                    self.item_count += 1
        else:
            # Player is not touching object
            other_rect.color = object_color_idle
            other_rect.status = 'idle'
        return

    # Movement and barrier detection
    def move(self, dx, dy, run):
        run_mod = 1.0
        if run:
            run_mod = 2.025

        Lside = self.pos.x + self.pos.y
        Rside = self.pos.x - self.pos.y
        if Lside >= 306 and Rside <= 655:
            self.pos.x += dx * run_mod
        if Lside <= 306:
            self.pos.x = (Lside - self.pos.y) + 4
        if Rside >= 655:
            self.pos.x = (Rside + self.pos.y) - 4

        if self.pos.y > 70 and self.pos.y < 430:
            self.pos.y += dy * run_mod
        if self.pos.y <= 70:
            self.pos.y = 70.1
        if self.pos.y >= 430:
            self.pos.y = 429.9
        clip = pygame.Rect(self.MARGIN + self.IMG_W * self.frame, self.side * 230, self.IMG_W, 225)
        return

    def draw(self, scr):
        #   Draws rect same size as image, exclude to stop drawing to screen
        pygame.draw.rect(scr, object_color_idle, (int(self.pos.x), int(self.pos.y), self.IMG_W, self.size[1] / 4))
        # Blit the image surface to screen surface
        scr.blit(self.my_image, (self.pos.x, self.pos.y), area=self.clip)
        return


# End of Player class ----------------------------------------------------------------------


class Puppy:
    def __init__(self, image_file, pos, vel):
        pic = pygame.image.load(image_file).convert_alpha()
        self.pos = pos
        self.vel = vel
        self.size = [int(x * 1) for x in pic.get_size()]  # x * [size rescaling]
        self.IMG_W = 125  # size of action left to right
        self.IMG_H = 138
        self.my_image = pygame.transform.scale(pic, self.size)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.IMG_W, self.IMG_H)
        # Animation operations
        self.MARGIN = 5  # how far away each action is left to right, ex width margin width
        self.offset_x = 30
        self.moving = True
        self.timer = 0
        self.frame = 0
        self.TIME = 10
        self.CT = 4  # Images per strip (row)
        self.side = 0  # Col on sprite sheet
        # Size of individual avatar action, margin
        self.clip = pygame.Rect(self.MARGIN + self.IMG_W * self.frame, self.MARGIN + self.side * self.IMG_H,
                                self.IMG_W, self.IMG_H)

        # Path operations
        self.target = None
        self.reached_destination = False
        self.pup_wait = 200
        self.ran_num = 0

    def update(self, delta_t):
        # updates puppy speed and position
        self.pos = self.pos.add(self.vel.scale(delta_t))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.IMG_H)
        self.clip = pygame.Rect(self.MARGIN + self.IMG_W * self.frame, self.side * self.IMG_H, self.IMG_W, self.IMG_H)

    def change_path(self, point_list):
        new_ran = random.randint(0, 5)

        while new_ran == self.ran_num:
            new_ran = random.randint(0, 5)

        self.ran_num = new_ran
        #  print(self.ran_num)
        point_list[self.ran_num].color = object_color_active
        point_list[self.ran_num].status = 'active'
        self.target = vector2(point_list[self.ran_num].pos.x - self.offset_x,
                              point_list[self.ran_num].pos.y - self.IMG_W)
        return

    def draw(self, scr):
        # pygame.draw.rect(scr, object_color_idle, (int(self.pos.x), int(self.pos.y), self.IMG_W, self.IMG_H))
        # self.rect = pygame.Rect(int(self.pos.x), int(self.pos.y), self.IMG_W, self.IMG_H)
        self.clip = pygame.Rect(self.MARGIN + self.IMG_W * self.frame, self.side * self.IMG_H, self.IMG_W, self.IMG_H)
        scr.blit(self.my_image, (self.pos.x, self.pos.y), area=self.clip)
        return

    def move(self, delta):
        if not self.reached_destination:
            if self.target is not None:
                self.moving = True
                # get the full displacement to target
                displacement = self.target.sub(self.pos)
                # normalize it to get direction
                direction = displacement.normalize()
                if self.frame < self.CT - 1:
                    self.frame += 1
                else:
                    self.frame = 0
                print(self.frame)
                # and multiply by speed to get velocity (pixels/ms)
                self.vel = direction.scale(0.25)
                # to get the actual step for this frame, multiply
                #  velocity by time (numerical integration)
                step = self.vel.scale(delta)

                # prevent overshooting (causes jitter back and forth)
                if step.magn() > displacement.magn():
                    # print("Pup is in move, and reached destination")
                    self.pos = self.target
                    self.target = None
                    self.reached_destination = True
                    return True
                else:
                    # otherwise update position by adding step
                    self.pos = self.pos.add(step)
        # elif self.reached_destination:
        else:
            self.mvoing = False
            # Simulates a wait time for the pup
            if self.pup_wait <= 0:
                self.reached_destination = False
                self.pup_wait = 200
            else:
                # print(self.pup_wait)
                self.pup_wait -= 1
        return False


class Objects:
    def __init__(self, image_file, pos, id):
        pic = pygame.image.load(image_file).convert_alpha()
        self.size = [int(x * 1) for x in pic.get_size()]  # x * [size rescaling]
        self.my_image = pygame.transform.scale(pic, self.size)
        self.pos = pos
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
        self.color = object_color_idle
        self.status = "idle"
        self.item_id = id
        self.item_held = False
        self.menu_pos = 0

    def draw(self, scr):
        # Draw objects to game
        # draw to menu when player is holding it
        if self.item_held:
            menu_offset = 0
            if self.menu_pos == 2:
                menu_offset = 150

                # Scales image to fix in item box, except poop bag since to big
            if self.item_id == 04:  # Doggie Bag
                self.rect = pygame.Rect(390 + menu_offset, 650, self.size[0], self.size[1])
                scr.blit(self.my_image, (390 + menu_offset, 650))

            elif self.item_id == 03:  # Toy Bone
                self.rect = pygame.Rect(370 + menu_offset, 650, self.size[0], self.size[1])
                temp_img = pygame.transform.scale(self.my_image, (self.size[0] * 2, self.size[1] * 2))
                scr.blit(temp_img, (370 + menu_offset, 650))
            else:
                # self.rect = pygame.draw.rect(scr, self.color, (390 + menu_offset, 650, self.size[0], self.size[1]))
                self.rect = pygame.Rect(390 + menu_offset, 650, self.size[0], self.size[1])
                temp_img = pygame.transform.scale(self.my_image, (self.size[0] * 2, self.size[1] * 2))
                scr.blit(temp_img, (390 + menu_offset, 650))
        # Draw in normal position
        else:
            #   Draws rect same size as image, exclude to stop drawing to screen
            # self.rect = pygame.draw.rect(scr, self.color, (int(self.pos.x), int(self.pos.y), self.size[0], self.size[1]))
            self.rect = pygame.Rect(int(self.pos.x), int(self.pos.y), self.size[0], self.size[1])
            # Blit the image surface to screen surface
            scr.blit(self.my_image, (self.pos.x, self.pos.y))

        return


# End of Objects class -------------------------------------------------


class Path:
    def __init__(self, pos, size):
        self.size = size
        self.pos = pos
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.color = object_color_idle
        self.status = "idle"
        self.pup_intersect = False
        self.accident_id = 0

    # Changes object attribute if puppy is within space
    def update(self, other_rect):
        if self.rect.colliderect(other_rect):
            self.color = object_color_warning
            self.status = 'warning'
            # Pup is here
            self.accident_id = random.randint(0, 1)
            self.pup_intersect = True
            return True
        else:
            return False
            # self.color = object_color_idle

    def draw(self, scr):
        #   Draws rect same size as image, exclude to stop drawing to screen
        pygame.draw.rect(scr, self.color, (int(self.pos.x), int(self.pos.y), self.size.x, self.size.y))
        if self.pup_intersect == True:
            # print("The Pup is here!")
            if self.accident_id == 0:
                scr.blit(pygame.image.load("Accident_Pee.png").convert_alpha(), (self.pos.x, self.pos.y))
            else:
                scr.blit(pygame.image.load("Accident_Poop.png").convert_alpha(), (self.pos.x, self.pos.y))
        return


# End of Path class -----------------------------------------------------------------------------------


class vector2:
    #   Param constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):  # Negates a vector
        v = vector2(-self.x, -self.y)
        return v

    # method definitions
    def add(self, other):
        v = vector2(self.x + other.x, self.y + other.y)
        return v

    def sub(self, other):
        v = vector2(self.x - other.x, self.y - other.y)
        return v

    def scale(self, s):
        ans = vector2(self.x, self.y)
        ans.x *= s
        ans.y *= s
        return ans

    def magn(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        result = vector2(0, 0)
        m = self.magn()
        if m == 0:
            return vector2(0, 0)
        result.x = self.x / m
        result.y = self.y / m
        return result

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # overload return-this-as-string for printing
    def __str__(self):
        # format allows you to replace "{}" with variable values
        return "({}, {})".format(self.x, self.y)
