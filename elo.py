import tkinter as tk
import random

window = tk.Tk()
window.title("Rainword")
window.geometry("600x400")
window.resizable(False, False)

canvas = tk.Canvas(window, width=600, height=400, bg="white")
canvas.pack()

word_list = ["Test", "Python", "Code", "Challenge", "Typing", "Game", "Window", "Canvas", "Letter", "Speed"]
active_words = []
speed = 2
game_running = True
typed_buffer = ""

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
            letter = canvas.create_text(self.x + i * 20, self.y, text=char, font=("Arial", 20), fill="black")
            self.letters.append(letter)

    def move(self):
        self.y += speed
        for letter in self.letters:
            canvas.move(letter, 0, speed)

    def destroy(self):
        for letter in self.letters:
            canvas.delete(letter)

# Add new falling words at random positions
def spawn_word():
    x_pos = random.randint(50, 400)
    word = random.choice(word_list)
    active_words.append(FallingWord(word, x_pos, 20))
    if game_running and len(active_words) < 4:
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
    for word_obj in active_words:
        if word_obj.text == typed_buffer:
            word_obj.destroy()
            active_words.remove(word_obj)
            typed_buffer = ""
            break

# Move all words down
def fall():
    global game_running
    if not game_running:
        return

    for word_obj in active_words:
        word_obj.move()
        if word_obj.y >= 350:
            game_over()
            return

    window.after(50, fall)

def game_over():
    global game_running
    game_running = False
    canvas.delete("all")
    canvas.create_text(300, 200, text="Game Over!", font=("Arial", 32), fill="red")

# Start the game
spawn_word()
window.bind("<Key>", on_key_press)
fall()
window.mainloop()
