# Python Wordle Game

A classic word-guessing game built with Python and the Tkinter GUI library.

*(Suggestion: Add a screenshot or GIF of your game here!)*

## 📖 About The Game

This project is a desktop implementation of the Wordle game. Players have six attempts to guess a secret five-letter word. After each guess, the game provides color-coded feedback:

* **🟩 Green:** The letter is in the word and in the correct position.
* **🟨 Yellow:** The letter is in the word but in the wrong position.
* **⬜ Gray:** The letter is not in the word.

The game includes an on-screen keyboard that also updates with these colors, helping you track used and correctly-placed letters.

## ✨ Features

* Classic 5-letter, 6-turn Wordle gameplay.
* Simple graphical user interface (GUI) built with Tkinter.
* Handles both mouse clicks on virtual keyboard and physical keyboard inputs.
* Validates guesses against a built-in dictionary to ensure only valid words are entered.
* "Play Again" option after winning or losing a round.
* Players could play multiple round in the game. 

## ⚙️ Requirements

* [Python >= 3.x](https://www.python.org/downloads/)
* Tkinter (This library is already included by default with most Python 3 installations.)

## 🚀 How to Set Up and Play

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
    cd YourRepoName
    ```
2.  **Run the game:**
    Once the `assets` folder and word lists are in place, you can run the game from your terminal:
    ```bash
    python main.py
    ```
    *(Note: On some systems, you may need to use `python3` instead of `python`.)*

## 📁 Project Structure
Wordle_Python/
│
├── assets/
│   ├── dictionary.txt  
│   └── guesses.txt     
│
├── main.py           
│
└── README.md           