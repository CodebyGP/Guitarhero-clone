import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up display
WINDOW_SIZE = (800, 600)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Keyboard Hero")

# Load the background image
background = pygame.image.load('concert.png') 
background = pygame.transform.scale(background, WINDOW_SIZE)  # Resize the background to match the window size


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Define rectangles for keys
KEY_RECTS = [pygame.Rect(100, 500, 50, 50), pygame.Rect(200, 500, 50, 50),
             pygame.Rect(300, 500, 50, 50), pygame.Rect(400, 500, 50, 50),
             pygame.Rect(500, 500, 50, 50)]

# List of available keys for the game
AVAILABLE_KEYS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g]

# Define hit zones for each key
HIT_ZONES = [pygame.Rect(75, 475, 50, 50), pygame.Rect(175, 475, 50, 50),
             pygame.Rect(275, 475, 50, 50), pygame.Rect(375, 475, 50, 50),
             pygame.Rect(475, 475, 50, 50)]

# Define a class for the "notes"
class Note:
    def __init__(self, key):
        self.key = key
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.x = KEY_RECTS[AVAILABLE_KEYS.index(key)].x
        self.speed = 10
        self.hit = False

    def move(self):
        self.rect.y += self.speed

    def check_hit(self):
        if self.rect.y > HIT_ZONES[AVAILABLE_KEYS.index(self.key)].y:
            return False
        if not self.hit and self.rect.colliderect(HIT_ZONES[AVAILABLE_KEYS.index(self.key)]):
            self.hit = True
            return True
        return False

# List to store active notes
active_notes = []

# Function to display text on screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function for displaying the main menu
def main_menu():
    while True:
        window.fill(BLACK)
        draw_text('Keyboard Hero', font, WHITE, window, 300, 200)
        draw_text('Select a Song:', small_font, GRAY, window, 300, 300)
        draw_text('1. Twinkle Twinkle Little Star', small_font, GRAY, window, 300, 350)
        draw_text('2. Memories', small_font, GRAY, window, 300, 380)
        draw_text('3. Hit Me With Your Best Shot', small_font, GRAY, window, 300, 410)
        draw_text('4. Wonderwall', small_font, GRAY, window, 300, 440)
        draw_text('Press "Q" to quit', small_font, GRAY, window, 300, 470)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_1:
                    return 'ttls.mp3', 161
                elif event.key == pygame.K_2:
                    return 'memories.mp3', 91
                elif event.key == pygame.K_3:
                    return 'hitmewithbestshot.mp3', 127
                elif event.key == pygame.K_4:
                    return 'wonderwall.mp3', 174


# Show main menu
chosen_song, chosen_bpm = main_menu()

# Load the chosen music
pygame.mixer.music.load(chosen_song)
pygame.mixer.music.play()


# Main game loop
running = True
score = 0
streak = 0
multiplier = 1
multiplier_active = False
multiplier_fade = 255
NOTE_GENERATION_INTERVAL = int(60000 / chosen_bpm)  # Convert BPM to milliseconds
last_note_time = pygame.time.get_ticks()
music_playing = True

stop_time = pygame.time.get_ticks() + 145000  # 2 minutes and 28 seconds in milliseconds

def game_over(score):
    while True:
        window.fill(BLACK)
        draw_text('Game Over', font, WHITE, window, 300, 200)
        draw_text('Final Score: ' + str(score), small_font, WHITE, window, 300, 250)
        draw_text('1. Return to Main Menu', small_font, GRAY, window, 250, 300)
        draw_text('2. Quit Game', small_font, GRAY, window, 250, 330)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'main_menu'
                elif event.key == pygame.K_2:
                    pygame.quit()
                    quit()

while running:
    # Blit the background
    window.blit(background, (0, 0))

    hit_note = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate a random note based on BPM
    current_time = pygame.time.get_ticks()
    if music_playing and current_time <= stop_time:
        if current_time - last_note_time >= NOTE_GENERATION_INTERVAL:
            num_notes = random.randint(1,2) # Generate 1 or 2 notes
            for _ in range(num_notes):
                key = random.choice(AVAILABLE_KEYS)
                active_notes.append(Note(key))
            last_note_time = current_time
    else:
        music_playing = False

    # Handle user input and check for hits
    keys = pygame.key.get_pressed()
    for note in active_notes:
        if note.check_hit() and keys[note.key]:
            note.hit = True
            score += 10
            streak += 1
            if streak % 10 == 0:
                multiplier_active = True
                multiplier = 2
            hit_note = True
        
        if streak >=10:
            score *= 2
            streak = 0

        if multiplier_active and multiplier_fade > 0:
            multiplier_fade -= 5


    # Move and draw notes
    for note in active_notes:
        note.move()
        if not note.hit:  # Only draw if the note hasn't been hit
            pygame.draw.rect(window, COLORS[AVAILABLE_KEYS.index(note.key)], note.rect)

    # Draw the keys with animation
    for i, (key_rect, key) in enumerate(zip(KEY_RECTS, ['A', 'S', 'D', 'F', 'G'])):
        pygame.draw.rect(window, WHITE, key_rect)
        key_text = font.render(key, True, BLACK)
        window.blit(key_text, (key_rect.centerx - 10, key_rect.centery - 10))

        if keys[AVAILABLE_KEYS[i]]:
            pygame.draw.rect(window, (100, 100, 100), key_rect)  # Change color when pressed

    # Draw the score and streak
    score_text = font.render("Score: " + str(score), True, WHITE)
    streak_text = small_font.render("Streak: " + str(streak), True, WHITE)
    multiplier_text = small_font.render("Multiplier: x" + str(multiplier), True, (255, 255, 255, multiplier_fade))

    window.blit(score_text, (10, 10))
    window.blit(streak_text, (10, 50))
    window.blit(multiplier_text, (10, 90))

    # Check if the music has finished playing
    if not pygame.mixer.music.get_busy() and music_playing:
        music_playing = False

    # Display the game over screen
    if not music_playing:
        window.fill(BLACK)
        draw_text('Game Over', font, WHITE, window, 300, 200)
        draw_text('Final Score: ' + str(score), small_font, WHITE, window, 300, 250)
        draw_text('Press "Y" to play again, any other key to quit', small_font, GRAY, window, 200, 300)
        pygame.display.update()

        # Wait for user input
        replay = False
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                    replay = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        replay = True
                    waiting = False

        if not replay:
            running = False
            main_menu()

        # Reset game variables
        active_notes = []
        score = 0
        streak = 0
        last_note_time = pygame.time.get_ticks()
        stop_time = pygame.time.get_ticks() + 145000  # Reset stop time

    pygame.display.update()
    window.fill(BLACK)
    pygame.time.Clock().tick(59)

pygame.quit()
