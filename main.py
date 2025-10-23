import random
import tkinter as tk
from tkinter import messagebox

# Game constants
MAX_TURNS = 6
WORD_LENGTH = 5

# Color constants
CORRECT_COLOR = "#6aaa64"    # Green for correct letter in correct spot
PRESENT_COLOR = "#c9b458"    # Yellow for correct letter in wrong spot
ABSENT_COLOR = "#787c7e"     # Gray for incorrect letter
DEFAULT_KEY_COLOR = "#d3d6da" # Default keyboard button color
DEFAULT_CELL_COLOR_1 = "#8494a0"  # Background color of a cell
DEFAULT_CELL_COLOR_2 = "#3e4d51" # foreground color of the text

def load_words(file):   
    words = set()
    # Load dictionary words
    try:
        with open(file, 'r') as f:
            for line in f:
                word = line.strip().upper()
                if len(word) == WORD_LENGTH:
                    words.add(word)
    except FileNotFoundError:
        print("Warning: file not found")
    
    return words    

# MAKE A GUESSING WORDS AND A DICTIONARY 
WORDS = load_words('assets/dictionary.txt')
GUESSSES = load_words('assets/guesses.txt')

# Ensure guesses are in words list
WORDS |= GUESSSES

# Converting to list
final_list = list(WORDS)
guess_list = list(GUESSSES)

def get_secret_word(Dict): 
    return random.choice(Dict)

# Create keyboard button
class KeyboardButton(tk.Button):
    def __init__(self, master, text, command, width=4):
        super().__init__(
            master,
            text=text,
            command=command,
            width=width,
            height=2,
            font=("Helvetica Neue", 12, "bold"),
            bg="#d3d6da",
            fg="#1a1a1b",
            relief="flat",
            borderwidth=0
        )
        
class WordleGUI: 
    def __init__(self, master):
        # initialize
        self.master = master
        self.current_turn = 0
        self.secret_word = get_secret_word(guess_list)
        self.round = 1
        # Configure the main window
        master.title("Python Wordle game")
        master.configure(bg="#045269")  
        master.resizable(False, False)        

        # Create main container
        self.main_container = tk.Frame(master, bg="#172829", padx=20, pady=20)
        self.main_container.pack(expand=True, fill="both")
        
        # Create game frame
        self.game_frame = tk.Frame(self.main_container, bg="#172829")
        self.game_frame.pack(expand=True, pady=20)
        
        # Create grid frame 
        self.grid_frame = tk.Frame(self.game_frame, bg="#373e3b", padx=10, pady=10)
        self.grid_frame.pack(pady = 20, padx = 10)

        # set grid label empty
        self.grid_labels = []
        for row in range(MAX_TURNS): 
            row_label = []
            for col in range(WORD_LENGTH): 
                label = tk.Label(
                self.grid_frame,
                text="",
                width=4,
                height=2,
                font=("Helvetica Neue", 24, "bold"),
                bg= DEFAULT_CELL_COLOR_1, 
                fg= DEFAULT_CELL_COLOR_2,
                borderwidth=2,
                relief="solid"
                )
                # .grid() place it in parent grid
                label.grid(row = row, column = col, padx = 5, pady = 5)
                row_label.append(label)
            self.grid_labels.append(row_label)

        # Initialize game state variables
        self.current_input = ""
        self.current_col = 0
        
        # Create keyboard frame
        self.keyboard_frame = tk.Frame(self.game_frame, bg="#172829")
        self.keyboard_frame.pack(pady=20)
        
        # Dictionary to store keyboard buttons
        self.keyboard_buttons = {}
        
        # First row of keyboard (Q to P)
        first_row = tk.Frame(self.keyboard_frame, bg="#172829")
        first_row.pack(pady=2)
        for letter in "QWERTYUIOP":
            btn = KeyboardButton(
                first_row,
                letter,
                lambda l=letter: self.handle_keyboard_click(l)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.keyboard_buttons[letter] = btn
            
        # Second row of keyboard (A to L)
        second_row = tk.Frame(self.keyboard_frame, bg="#172829")
        second_row.pack(pady=2)
        for letter in "ASDFGHJKL":
            btn = KeyboardButton(
                second_row,
                letter,
                lambda l=letter: self.handle_keyboard_click(l)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.keyboard_buttons[letter] = btn
            
        # Third row of keyboard (ENTER, Z to M, BACK)
        third_row = tk.Frame(self.keyboard_frame, bg="#172829")
        third_row.pack(pady=2)
        
        # Enter button
        self.enter_button = KeyboardButton(
            third_row,
            "ENTER",
            self.submit_guess,
            width=6
        )
        self.enter_button.pack(side=tk.LEFT, padx=2)
        
        # Letters Z to M
        for letter in "ZXCVBNM":
            self.keyboard_buttons[letter] = KeyboardButton(
                third_row,
                letter,
                lambda l=letter: self.handle_keyboard_click(l)
            )
            self.keyboard_buttons[letter].pack(side=tk.LEFT, padx=2)
            
        # Backspace button
        self.backspace_button = KeyboardButton(
            third_row,
            "⌫",
            self.handle_backspace,
            width=6
        )
        self.backspace_button.pack(side=tk.LEFT, padx=2)
        
        # Bind physical keyboard events to both master and grid_frame
        for widget in (self.master, self.grid_frame):
            widget.bind('<Key>', self.handle_keypress)
            widget.bind('<Return>', self.submit_guess)
            widget.bind('<BackSpace>', self.handle_backspace)
        
        # Set initial focus and make grid_frame focusable
        self.grid_frame.configure(takefocus=1)
        self.grid_frame.focus_set()
        
        # Maintain focus when clicking anywhere in the window
        self.master.bind('<Button-1>', lambda e: self.grid_frame.focus_set())
        
    def handle_keyboard_click(self, letter):
        # Handle virtual keyboard button clicks
        if self.current_turn >= MAX_TURNS or self.current_col >= WORD_LENGTH:
            return
            
        # Update the current cell with new letter
        self.grid_labels[self.current_turn][self.current_col].config(
            text=letter,
            fg = "#1a1a1b",
            bg = DEFAULT_CELL_COLOR_1
        )
        
        # Update tracking variables
        self.current_input += letter
        self.current_col += 1
        
        # Force update display
        self.grid_frame.update()
        
    def handle_keypress(self, event):
        # Handle physical keyboard press
        if self.current_turn >= MAX_TURNS:
            return "break"
            
        # Get the actual character input
        char = event.char
        
        # Handle Vietnamese characters and normal alphabet
        if char and len(char) == 1 and char.isalpha() and self.current_col < WORD_LENGTH:
            letter = char.upper()
            self.handle_keyboard_click(letter)  
            self.grid_frame.focus_set()  # Keep focus on grid
            
        return "break"

    def handle_backspace(self, event = None):
        if self.current_col > 0: 
            self.current_col -= 1
            self.current_input = self.current_input[:-1]
            self.grid_labels[self.current_turn][self.current_col].config(text="")
        return "break"  # Prevent the defau lt behavior
    
    def submit_guess(self, event = None):
        guess = self.current_input
        # validation
        if len(guess) != WORD_LENGTH:
            messagebox.showwarning("Invalid Guess", f"Please enter a {WORD_LENGTH}-letter word.")
            return "break" 

        if guess not in final_list: 
            messagebox.showwarning("Invalid Guess", f"Please enter a correct word!")          
            return "break" 

        # submit the answer
        feedback = self.provide_feedback(guess, self.secret_word)

        # Update the grid with the guess and feedback colors
        all_green = True 
        for i in range(WORD_LENGTH):
            # Get the label for the current row and column
            label = self.grid_labels[self.current_turn][i]
            letter = guess[i]
            label.config(text=letter) 
            
            # Change the background color based on feedback
            if feedback[i] == "GREEN":
                label.config(bg=CORRECT_COLOR, fg="white")
                # Update keyboard button to green
                if letter in self.keyboard_buttons:
                    self.keyboard_buttons[letter].configure(bg=CORRECT_COLOR, fg="white")
            elif feedback[i] == "YELLOW":
                label.config(bg=PRESENT_COLOR, fg="white")
                all_green = False
                # Update keyboard button to yellow if not already green
                if letter in self.keyboard_buttons:
                    if self.keyboard_buttons[letter].cget("bg") != CORRECT_COLOR:
                        self.keyboard_buttons[letter].configure(bg=PRESENT_COLOR, fg="white")
            else:  # GRAY
                label.config(bg=ABSENT_COLOR, fg="white")
                all_green = False
                if letter in self.keyboard_buttons:
                    if self.keyboard_buttons[letter].cget("bg") not in [CORRECT_COLOR, PRESENT_COLOR]:
                        self.keyboard_buttons[letter].configure(bg=ABSENT_COLOR, fg="white")

        #Check player win or not
        if all_green:
            self.round+=1
            result = messagebox.askyesno("Congratulations!", 
                f"You won! The word was {self.secret_word}\nWould you like to play round {self.round}?")
            if result:
                self.reset_game()
            else:
                self.master.quit()
            return "break" 

        # Move to the next turn
        self.current_turn += 1
        self.current_input = ""
        self.current_col = 0

        # Check if the player has run out of turns
        if self.current_turn >= MAX_TURNS:
            result = messagebox.askyesno("Game Over", 
                f"You've run out of turns! The word was {self.secret_word}\nWould you like to play again?")
            if result:
                self.round = 1
                self.reset_game()
                return "break"
            else:
                self.master.quit()
                return "break" 
        return "break"

    def reset_game(self):
        # Reset game state
        self.current_turn = 0
        self.current_input = ""
        self.current_col = 0
        # pick a new secret word
        self.secret_word = get_secret_word(guess_list)

        # Clear all grid labels (text and background)
        for row in range(MAX_TURNS):
            for col in range(WORD_LENGTH):
                self.grid_labels[row][col].config(
                    text="",
                    bg = DEFAULT_CELL_COLOR_1,
                    fg = DEFAULT_CELL_COLOR_2
                )

        # Reset on-screen keyboard buttons to default colors
        try:
            for key, btn in self.keyboard_buttons.items():
                btn.configure(bg=DEFAULT_KEY_COLOR, fg="#1a1a1b")
        except Exception:
            # If keyboard_buttons isn't available for some reason, skip
            pass

        # Reset Enter and Backspace button styles (if present)
        try:
            if hasattr(self, 'enter_button') and self.enter_button:
                self.enter_button.configure(bg=DEFAULT_KEY_COLOR, fg="#1a1a1b")
            if hasattr(self, 'backspace_button') and self.backspace_button:
                self.backspace_button.configure(bg=DEFAULT_KEY_COLOR, fg="#1a1a1b")
        except Exception:
            pass

        # Ensure focus is back 
        try:
            self.grid_frame.focus_set()
        except Exception:
            pass
        
    def provide_feedback(self, guess, secret): 
        feedback = [""] * WORD_LENGTH
        cnt_secret_letter = {}

        for letter in secret:
            cnt_secret_letter[letter] = cnt_secret_letter.get(letter,0) + 1

        for i in range(WORD_LENGTH):
            if (guess[i] == secret[i]): 
                feedback[i] = 'GREEN'
                cnt_secret_letter[guess[i]]-=1

        for i in range(WORD_LENGTH):
            letter = guess[i]
            if feedback[i] == 'GREEN':
                continue
            if (letter in cnt_secret_letter and cnt_secret_letter[letter] > 0): 
                feedback[i] = 'YELLOW'
                cnt_secret_letter[letter] -= 1
            else: 
                feedback[i] = 'GRAY'
        return feedback

if __name__ == "__main__":
    root = tk.Tk()
    game_GUI = WordleGUI(root)
    root.mainloop()