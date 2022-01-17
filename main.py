from tkinter import *

from pandas import *
from random import *

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("words_to_learn.csv")
    data_dict = data.to_dict(orient="records")
    if len(data_dict) == 0:
        raise FileNotFoundError
except FileNotFoundError:
    data = pandas.read_csv("french_words.csv")
    data_dict = data.to_dict(orient="records")




word_set = {}
french = []
known_list = []


def french_word():
    # fr_word = word_set["French"]
    # en_word = word_set["English"]
    global word_set, FLIP, data
    window.after_cancel(FLIP)
    if len(data_dict) == 0:
        return
    word_set = choice(data_dict)
    canvas.itemconfigure(card, image=front)
    canvas.itemconfigure(card_title, text="French", fill="black")
    canvas.itemconfigure(card_word, text=word_set["French"], fill="black")
    FLIP = window.after(3000, english_word)


def english_word():
    global word_set
    canvas.itemconfigure(card, image=back)
    canvas.itemconfigure(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=word_set["English"], fill="white")


def known():
    global word_set
    if len(data_dict) == 0:
        canvas.itemconfigure(card_title, text="Mots terminé!!", fill="black")
        canvas.itemconfigure(card_word, text="Words completed!!", fill="black")
        return
    known_list.append(word_set)
    data_dict.remove(word_set)
    print(len(data_dict))
    french_word()


window = Tk()
window.config(bg=BACKGROUND_COLOR)
window.config(padx=5, pady=10)
FLIP = window.after(3000, english_word)

front = PhotoImage(file="card_front.png")
back = PhotoImage(file="card_back.png")

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(410, 263, image=front)

card_title = canvas.create_text(400, 150, text="", font=("Amithen", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Brannboll Smal", 50, "bold"))


canvas.grid(column=0, row=0, columnspan=2)


right = PhotoImage(file="right.png")
wrong = PhotoImage(file="wrong.png")

known_word = Button(image=right, bg=BACKGROUND_COLOR, highlightthickness=0, bd=0, command=known)
unknown_word = Button(image=wrong, bg=BACKGROUND_COLOR, highlightthickness=0, bd=0, command=french_word)

known_word.grid(column=0, row=1, padx=5, pady=5)
unknown_word.grid(column=1, row=1, padx=5, pady=5)

french_word()

window.mainloop()

words_to_learn = pandas.DataFrame(data_dict)
words_to_learn.to_csv("words_to_learn.csv")
