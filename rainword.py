## Imports
import tkinter as tk
import random

# Window set up
window = tk.Tk()
window.title("RainWord")
window.geometry("600x400")
window.resizable(False, False)

# Canvas set up
canvas = tk.Canvas(window, width=600, height=400, bg="black")
canvas.pack()

# Variables
word_list = ["Test", "Python", "Code", "Challenge", "Typing", "Game", "Window", "Canvas", "Letter", "Speed"]
active_words = []
speed = 1
game_running = False
typed_buffer = ""
score = 0

# Word object structure
class FallingWord:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.letters = []
        self.create_text()

    def create_text(self):
        self.letters.clear()
        for i, char in enumerate(self.text):
            if game_running:
                letter = canvas.create_text(self.x + i * 20, self.y, text=char, font=("Console", 20), fill="white")
                self.letters.append(letter)

    def move(self, speed):
        self.y += speed
        for letter in self.letters:
            canvas.move(letter, 0, speed)

    def destroy(self):
        for letter in self.letters:
            canvas.delete(letter)

    def highlight(self, typed):
        for i, letter in enumerate(self.letters):
            if i < len(typed) and self.text[i] == typed[i]:
                canvas.itemconfig(letter, fill="green")
            else:
                canvas.itemconfig(letter, fill="white")

# Add new falling words at random positions
def spawn_word():
    global game_running
    x_pos = random.randint(50, 400)
    word = random.choice(word_list)

    active_words.append(FallingWord(word, x_pos, 20))
    if game_running:
        window.after(2000, spawn_word)  # Spawn every 2 seconds

# Typing input
def on_key_press(event):
    global typed_buffer
    if not game_running:
        return

    if event.keysym == "BackSpace":
        typed_buffer = typed_buffer[:-1]
    elif event.keysym == "Return":
        typed_buffer = ""
    else:
        typed_buffer += event.char

    check_words()

def check_words():
    global typed_buffer
    global speed
    global score
    if not active_words:
        return
    
    # Targeting bottom word
    target_word = max(active_words, key=lambda w: w.y)

    # Highlighting each letter as its written
    target_word.highlight(typed_buffer)

    # Check if the user wrote the word correctly
    if target_word.text == typed_buffer:
        target_word.destroy()
        active_words.remove(target_word)
        typed_buffer = ""
        speed += .5
        score += 1

# Move all words down
def fall():
    global game_running
    if not game_running:
        return

    for word_obj in active_words:
        word_obj.move(speed)
        if word_obj.y >= 400:
            game_over()
            return

    window.after(50, fall)

def game_over():
    global game_running
    global score
    game_running = False
    canvas.delete("all")
    canvas.create_text(300, 150, text="Game Over!", font=("Console", 32), fill="white")
    canvas.create_text(300, 200, text="Score: " + str(score), font=("Console", 32), fill="white")

def start(event=None):
    global game_running
    if game_running:
        return
    # Start the game
    canvas.delete("all")
    game_running = True
    spawn_word()
    window.bind("<Key>", on_key_press)
    fall()

canvas.create_text(300, 150, text="RainWord", font=("Console", 32), fill="white")
canvas.create_text(300, 200, text="Press <ENTER> to continue...", font=("Console", 32), fill="white")
window.bind("<Return>", start)
window.mainloop()
