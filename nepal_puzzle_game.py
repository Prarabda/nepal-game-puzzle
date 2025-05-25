import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nepal Places Puzzle Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font_large = pygame.font.SysFont('Arial', 40)
font_medium = pygame.font.SysFont('Arial', 30)
font_small = pygame.font.SysFont('Arial', 20)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font_medium.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class PuzzleGame:
    def __init__(self):
        self.places = [
            {
                "name": "Pashupatinath Temple",
                "image": "pashupatinath.jpg",
                "facts": [
                    "Pashupatinath is one of the most sacred Hindu temples dedicated to Lord Shiva.",
                    "It is located on the banks of the Bagmati River in Kathmandu.",
                    "The temple is a UNESCO World Heritage Site.",
                    "The main pagoda-style temple has a gilded roof and four silver-plated doors."
                ],
                "quiz": [
                    {
                        "question": "On which river's bank is Pashupatinath Temple located?",
                        "options": ["Bagmati", "Koshi", "Gandaki", "Karnali"],
                        "answer": 0
                    },
                    {
                        "question": "To which deity is Pashupatinath Temple dedicated?",
                        "options": ["Vishnu", "Brahma", "Shiva", "Ganesh"],
                        "answer": 2
                    }
                ]
            },
            {
                "name": "Mount Everest",
                "image": "everest.jpg",
                "facts": [
                    "Mount Everest is Earth's highest mountain above sea level at 8,848.86 meters.",
                    "It is located in the Mahalangur Himal sub-range of the Himalayas.",
                    "In Nepali, Everest is known as Sagarmatha, meaning 'Goddess of the Sky'.",
                    "The first confirmed successful ascent was by Edmund Hillary and Tenzing Norgay in 1953."
                ],
                "quiz": [
                    {
                        "question": "What is the height of Mount Everest?",
                        "options": ["7,848.86 meters", "8,848.86 meters", "9,848.86 meters", "10,848.86 meters"],
                        "answer": 1
                    },
                    {
                        "question": "What is Mount Everest called in Nepali?",
                        "options": ["Annapurna", "Kanchenjunga", "Sagarmatha", "Dhaulagiri"],
                        "answer": 2
                    }
                ]
            },
            {
                "name": "Lumbini",
                "image": "lumbini.jpg",
                "facts": [
                    "Lumbini is the birthplace of Siddhartha Gautama, who later became Buddha.",
                    "It is a UNESCO World Heritage Site located in the Rupandehi District.",
                    "The sacred garden contains the Maya Devi Temple, marking the exact birth spot.",
                    "The Ashoka Pillar, erected by Emperor Ashoka in 249 BCE, confirms the birthplace of Buddha."
                ],
                "quiz": [
                    {
                        "question": "Who was born in Lumbini?",
                        "options": ["Lord Shiva", "Gautama Buddha", "Lord Vishnu", "Guru Nanak"],
                        "answer": 1
                    },
                    {
                        "question": "Which emperor erected a pillar in Lumbini to mark Buddha's birthplace?",
                        "options": ["Chandragupta", "Ashoka", "Akbar", "Kanishka"],
                        "answer": 1
                    }
                ]
            }
        ]
        
        self.current_place_index = 0
        self.current_place = self.places[self.current_place_index]
        self.state = "menu"  # menu, puzzle, congrats, facts, quiz
        self.puzzle_pieces = []
        self.selected_piece = None
        self.completed_puzzles = []
        self.current_quiz_question = 0
        self.score = 0
        self.total_questions = sum(len(place["quiz"]) for place in self.places)
        self.congrats_timer = 0
        
        # Create placeholder images for now
        self.create_placeholder_images()
        
    def create_placeholder_images(self):
        # Create directory for images if it doesn't exist
        if not os.path.exists("images"):
            os.makedirs("images")
            
        # Create placeholder images for the places
        for place in self.places:
            image_path = os.path.join("images", place["image"])
            if not os.path.exists(image_path):
                # Create a simple colored rectangle as placeholder
                img_surface = pygame.Surface((300, 200))
                img_surface.fill((random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
                
                # Add text to the image
                text = font_medium.render(place["name"], True, BLACK)
                text_rect = text.get_rect(center=(150, 100))
                img_surface.blit(text, text_rect)
                
                # Save the image
                pygame.image.save(img_surface, image_path)
    
    def load_puzzle(self):
        self.current_place = self.places[self.current_place_index]
        image_path = os.path.join("images", self.current_place["image"])
        
        try:
            original_image = pygame.image.load(image_path)
            self.original_image = pygame.transform.scale(original_image, (400, 300))
        except pygame.error:
            # If image loading fails, create a colored rectangle
            self.original_image = pygame.Surface((400, 300))
            self.original_image.fill((random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
            text = font_medium.render(self.current_place["name"], True, BLACK)
            text_rect = text.get_rect(center=(200, 150))
            self.original_image.blit(text, text_rect)
        
        # Create puzzle pieces (3x3 grid)
        self.puzzle_pieces = []
        piece_width = self.original_image.get_width() // 3
        piece_height = self.original_image.get_height() // 3
        
        positions = []
        for i in range(3):
            for j in range(3):
                positions.append((200 + j * piece_width, 150 + i * piece_height))
        
        # Shuffle positions
        random.shuffle(positions)
        
        for i in range(3):
            for j in range(3):
                piece_surface = pygame.Surface((piece_width, piece_height))
                piece_surface.blit(self.original_image, (0, 0), 
                                  (j * piece_width, i * piece_height, piece_width, piece_height))
                
                pos_index = i * 3 + j
                piece = {
                    "surface": piece_surface,
                    "current_pos": positions[pos_index],
                    "correct_pos": (200 + j * piece_width, 150 + i * piece_height),
                    "rect": pygame.Rect(positions[pos_index], (piece_width, piece_height))
                }
                self.puzzle_pieces.append(piece)
    
    def check_puzzle_complete(self):
        for piece in self.puzzle_pieces:
            if piece["current_pos"] != piece["correct_pos"]:
                return False
        return True
        
    def calculate_puzzle_progress(self):
        correct_pieces = 0
        for piece in self.puzzle_pieces:
            if piece["current_pos"] == piece["correct_pos"]:
                correct_pieces += 1
        return (correct_pieces / len(self.puzzle_pieces)) * 100
    
    def draw_menu(self):
        screen.fill(WHITE)
        
        # Title
        title = font_large.render("Nepal Places Puzzle Game", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Start button
        start_button = Button(SCREEN_WIDTH // 2 - 100, 200, 200, 50, "Start Game", GRAY, BLUE)
        start_button.draw(screen)
        
        # Exit button
        exit_button = Button(SCREEN_WIDTH // 2 - 100, 300, 200, 50, "Exit", GRAY, RED)
        exit_button.draw(screen)
        
        # Check button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        start_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)
        
        if start_button.is_clicked(mouse_pos, mouse_click):
            self.state = "puzzle"
            self.load_puzzle()
        
        if exit_button.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()
    
    def draw_puzzle(self):
        screen.fill(WHITE)
        
        # Draw place name
        name_text = font_medium.render(f"Puzzle: {self.current_place['name']}", True, BLACK)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 20))
        
        # Draw puzzle pieces
        for piece in self.puzzle_pieces:
            screen.blit(piece["surface"], piece["current_pos"])
            pygame.draw.rect(screen, BLACK, pygame.Rect(piece["current_pos"], piece["surface"].get_size()), 1)
        
        # Draw selected piece with highlight
        if self.selected_piece is not None:
            pygame.draw.rect(screen, BLUE, 
                            pygame.Rect(self.puzzle_pieces[self.selected_piece]["current_pos"], 
                                      self.puzzle_pieces[self.selected_piece]["surface"].get_size()), 3)
        
        # Draw progress bar
        progress = self.calculate_puzzle_progress()
        progress_text = font_small.render(f"Progress: {progress:.1f}%", True, BLACK)
        screen.blit(progress_text, (SCREEN_WIDTH - 150, 20))
        
        # Draw progress bar
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH - 150, 50, 100, 20))
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - 150, 50, int(progress), 20))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 150, 50, 100, 20), 1)
        
        # Draw back button
        back_button = Button(20, 20, 100, 40, "Back", GRAY, RED)
        back_button.draw(screen)
        
        # Check button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        back_button.check_hover(mouse_pos)
        
        if back_button.is_clicked(mouse_pos, mouse_click):
            self.state = "menu"
            self.selected_piece = None
            
    def draw_congrats(self):
        screen.fill(WHITE)
        
        # Draw congratulations message
        congrats_text = font_large.render("Congratulations!", True, GREEN)
        screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, 100))
        
        complete_text = font_medium.render(f"You completed the {self.current_place['name']} puzzle!", True, BLACK)
        screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, 180))
        
        # Draw the completed image
        image_rect = self.original_image.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(self.original_image, image_rect)
        
        # Draw continue button
        continue_button = Button(SCREEN_WIDTH // 2 - 100, 500, 200, 50, "Continue to Facts", GRAY, BLUE)
        continue_button.draw(screen)
        
        # Check button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        continue_button.check_hover(mouse_pos)
        
        if continue_button.is_clicked(mouse_pos, mouse_click):
            self.state = "facts"
            
        # Auto-continue after 3 seconds
        self.congrats_timer += 1
        if self.congrats_timer > 180:  # 3 seconds at 60 FPS
            self.state = "facts"
            self.congrats_timer = 0
    
    def draw_facts(self):
        screen.fill(WHITE)
        
        # Draw place name
        name_text = font_large.render(self.current_place["name"], True, BLACK)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 20))
        
        # Draw image
        image_rect = self.original_image.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(self.original_image, image_rect)
        
        # Draw facts
        y_offset = 250
        for fact in self.current_place["facts"]:
            # Wrap text to fit screen width
            words = fact.split()
            lines = []
            line = ""
            for word in words:
                test_line = line + word + " "
                if font_small.size(test_line)[0] < SCREEN_WIDTH - 40:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + " "
            lines.append(line)
            
            for line in lines:
                fact_text = font_small.render(line, True, BLACK)
                screen.blit(fact_text, (20, y_offset))
                y_offset += 25
            
            y_offset += 5  # Space between facts
        
        # Draw continue button
        continue_button = Button(SCREEN_WIDTH // 2 - 100, 500, 200, 50, "Continue to Quiz", GRAY, GREEN)
        continue_button.draw(screen)
        
        # Check button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        continue_button.check_hover(mouse_pos)
        
        if continue_button.is_clicked(mouse_pos, mouse_click):
            self.state = "quiz"
            self.current_quiz_question = 0
    
    def draw_quiz(self):
        screen.fill(WHITE)
        
        # Draw place name
        name_text = font_medium.render(f"Quiz: {self.current_place['name']}", True, BLACK)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 20))
        
        # Get current question
        question_data = self.current_place["quiz"][self.current_quiz_question]
        
        # Draw question
        question_text = font_medium.render(question_data["question"], True, BLACK)
        screen.blit(question_text, (SCREEN_WIDTH // 2 - question_text.get_width() // 2, 80))
        
        # Draw options as buttons
        option_buttons = []
        for i, option in enumerate(question_data["options"]):
            button = Button(SCREEN_WIDTH // 2 - 150, 150 + i * 70, 300, 50, option, GRAY, BLUE)
            button.draw(screen)
            option_buttons.append(button)
        
        # Check button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        for i, button in enumerate(option_buttons):
            button.check_hover(mouse_pos)
            
            if button.is_clicked(mouse_pos, mouse_click):
                # Check if answer is correct
                if i == question_data["answer"]:
                    self.score += 1
                
                # Move to next question or next place
                self.current_quiz_question += 1
                if self.current_quiz_question >= len(self.current_place["quiz"]):
                    self.completed_puzzles.append(self.current_place_index)
                    self.current_place_index += 1
                    
                    if self.current_place_index >= len(self.places):
                        self.state = "results"
                    else:
                        self.state = "puzzle"
                        self.load_puzzle()
    
    def draw_results(self):
        screen.fill(WHITE)
        
        # Draw title
        title = font_large.render("Game Complete!", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Draw score
        score_text = font_medium.render(f"Your Score: {self.score}/{self.total_questions}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))
        
        # Draw message based on score
        percentage = (self.score / self.total_questions) * 100
        if percentage >= 80:
            message = "Excellent! You're a Nepal expert!"
        elif percentage >= 60:
            message = "Good job! You know a lot about Nepal!"
        else:
            message = "Keep learning about the beautiful places of Nepal!"
        
        message_text = font_medium.render(message, True, BLACK)
        screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, 200))
        
        # Draw play again button
        play_again_button = Button(SCREEN_WIDTH // 2 - 100, 300, 200, 50, "Play Again", GRAY, GREEN)
        play_again_button.draw(screen)
        
        # Draw exit button
        exit_button = Button(SCREEN_WIDTH // 2 - 100, 400, 200, 50, "Exit", GRAY, RED)
        exit_button.draw(screen)
        
        # Check button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        play_again_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)
        
        if play_again_button.is_clicked(mouse_pos, mouse_click):
            self.__init__()  # Reset the game
            self.state = "menu"
        
        if exit_button.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.state == "puzzle":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a puzzle piece was clicked
                    for i, piece in enumerate(self.puzzle_pieces):
                        if pygame.Rect(piece["current_pos"], piece["surface"].get_size()).collidepoint(event.pos):
                            self.selected_piece = i
                            break
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.selected_piece is not None:
                        # Check if the piece was dropped on another piece
                        for i, piece in enumerate(self.puzzle_pieces):
                            if i != self.selected_piece and pygame.Rect(piece["current_pos"], piece["surface"].get_size()).collidepoint(event.pos):
                                # Swap pieces
                                self.puzzle_pieces[self.selected_piece]["current_pos"], piece["current_pos"] = \
                                    piece["current_pos"], self.puzzle_pieces[self.selected_piece]["current_pos"]
                                
                                # Update rects
                                self.puzzle_pieces[self.selected_piece]["rect"].topleft = self.puzzle_pieces[self.selected_piece]["current_pos"]
                                piece["rect"].topleft = piece["current_pos"]
                                
                                # Check if puzzle is complete
                                if self.check_puzzle_complete():
                                    self.state = "congrats"
                                    self.congrats_timer = 0
                                
                                break
                        
                        self.selected_piece = None
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            self.handle_events()
            
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "puzzle":
                self.draw_puzzle()
            elif self.state == "congrats":
                self.draw_congrats()
            elif self.state == "facts":
                self.draw_facts()
            elif self.state == "quiz":
                self.draw_quiz()
            elif self.state == "results":
                self.draw_results()
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = PuzzleGame()
    game.run()
