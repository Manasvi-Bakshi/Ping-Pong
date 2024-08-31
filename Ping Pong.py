import pygame
import random

pygame.init()

# Base
Width, Height = 1000, 600
wn = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Ping Pong")
run = True
direction = [0, 1]
angle = [0, 1, 2]

# Graphics (Updated colors)
pong_color = (255, 105, 180)  # Hot pink
ping_color = (173, 216, 230)  # Light blue
BG_color = (255, 228, 181)    # Moccasin

# Ping-pong
radius = 15
pong_x, pong_y = Width / 2 - radius, Height / 2 - radius
ping_width, ping_height = 20, 120
left_ping_x, right_ping_x = 100 - ping_width / 2, Width - (100 - ping_width / 2)
left_ping_y = right_ping_y = Height / 2 - ping_height / 2
pong_vel_x, pong_vel_y = 0.7, 0.7
right_ping_vel = left_ping_vel = 0

# Score
left_score = 0
right_score = 0
font = pygame.font.SysFont("Comic Sans MS", 50)  # Updated font
initial_font = pygame.font.SysFont("Comic Sans MS", 40)  # Font for initial text

# Randomize initial direction
if random.choice([True, False]):
    pong_vel_x *= -1

# Player mode selection
one_player = False
mode_selected = False

# Main loop
while run:
    wn.fill(BG_color)
    
    if not mode_selected:
        # Mode selection screen with updated text
        select_text = initial_font.render("Please CHOOSE your game-mode", True, (0, 0, 0))
        select_text_1 = initial_font.render("press 1 for 1 PLAYER MODE", True, (0, 0, 0))
        select_text_2 = initial_font.render("2 for 2 PLAYER MODE", True, (0, 0, 0))
        wn.blit(select_text, (Width / 2 - select_text.get_width() / 2, Height / 2 - 100))
        wn.blit(select_text_1, (Width / 2 - select_text_1.get_width() / 2, Height / 2 - 50))
        wn.blit(select_text_2, (Width / 2 - select_text_2.get_width() / 2, Height / 2))
        pygame.display.update()
        
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_1:
                    one_player = True
                    mode_selected = True
                elif i.key == pygame.K_2:
                    one_player = False
                    mode_selected = True
    else:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    right_ping_vel = -0.9
                if i.key == pygame.K_DOWN:
                    right_ping_vel = 0.9
                if not one_player:
                    if i.key == pygame.K_w:
                        left_ping_vel = -0.9
                    if i.key == pygame.K_s:
                        left_ping_vel = 0.9
            if i.type == pygame.KEYUP:
                right_ping_vel = 0
                if not one_player:
                    left_ping_vel = 0

        # Collision with the left paddle
        if left_ping_x <= pong_x - radius <= left_ping_x + ping_width:
            if left_ping_y <= pong_y <= left_ping_y + ping_height:
                pong_vel_x *= -1

        # Collision with the right paddle
        if right_ping_x <= pong_x + radius <= right_ping_x + ping_width:
            if right_ping_y <= pong_y <= right_ping_y + ping_height:
                pong_vel_x *= -1

        # Boundaries
        if pong_y <= 0 + radius or pong_y >= Height - radius:
            pong_vel_y *= -1

        # If ball goes past the right paddle (left player scores)
        if pong_x >= Width - radius:
            left_score += 1
            pong_x, pong_y = Width / 2 - radius, Height / 2 - radius
            pong_vel_x *= random.choice([-1, 1])  # Randomize direction on reset

        # If ball goes past the left paddle (right player scores)
        if pong_x <= 0 + radius:
            right_score += 1
            pong_x, pong_y = Width / 2 - radius, Height / 2 - radius
            pong_vel_x *= random.choice([-1, 1])  # Randomize direction on reset

        # AI movement for left paddle
        if one_player:
            if pong_y < left_ping_y + ping_height / 2:
                if random.random() > 0.1:  # 10% chance AI will miss
                    left_ping_y -= 0.7
            if pong_y > left_ping_y + ping_height / 2:
                if random.random() > 0.1:  # 10% chance AI will miss
                    left_ping_y += 0.7

        # Limit paddles' movement
        if left_ping_y >= Height - ping_height:
            left_ping_y = Height - ping_height
        if left_ping_y <= 0:
            left_ping_y = 0
        if right_ping_y >= Height - ping_height:
            right_ping_y = Height - ping_height
        if right_ping_y <= 0:
            right_ping_y = 0

        # Movement
        pong_x += pong_vel_x
        pong_y += pong_vel_y
        right_ping_y += right_ping_vel
        if not one_player:
            left_ping_y += left_ping_vel

        # Draw objects
        pygame.draw.circle(wn, pong_color, (int(pong_x), int(pong_y)), radius)
        pygame.draw.rect(wn, ping_color, pygame.Rect(left_ping_x, left_ping_y, ping_width, ping_height))
        pygame.draw.rect(wn, ping_color, pygame.Rect(right_ping_x, right_ping_y, ping_width, ping_height))

        # Draw scores in the center
        score_text = font.render(f"{left_score}  -  {right_score}", True, (0, 0, 0))  # Black text
        wn.blit(score_text, (Width / 2 - score_text.get_width() / 2, 20))

        # Update display
        pygame.display.update()

pygame.quit()
