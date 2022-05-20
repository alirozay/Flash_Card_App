from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
    if len(data) == 0:
        data = pandas.read_csv("data/french_words.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
french_data = data["French"].tolist()
english_data = data["English"].tolist()
data_dict = {french_data[i]: english_data[i] for i in range(len(french_data))}
random.shuffle(french_data)
words_to_learn = {"French": [],
                  "English": []
                  }
key = 0


def exit_window() -> bool:
    return key == len(french_data) - 1


def flip_card() -> None:
    canvas.itemconfig(canvas_img, image=back_image)
    canvas.itemconfig(lang_text_canvas, text="English",
                      font=('Arial', 40, 'italic'))
    canvas.itemconfig(word_text_canvas, text=f"{data_dict[french_data[key]]}",
                      font=('Arial', 60, 'bold'))


def canvas_writer() -> None:
    canvas.itemconfig(canvas_img, image=front_image)
    canvas.itemconfig(lang_text_canvas, text="French",
                      font=('Arial', 40, 'italic'))
    canvas.itemconfig(word_text_canvas, text=f"{french_data[key]}",
                      font=('Arial', 60, 'bold'))
    window.after(3000, func=flip_card)


def right_button() -> None:
    global key
    if exit_window():
        window.destroy()
    else:
        key += 1
        canvas_writer()


def wrong_button() -> None:
    global key
    words_to_learn["French"].append(french_data[key])
    words_to_learn["English"].append(data_dict[french_data[key]])
    if exit_window():
        window.destroy()
    else:
        key += 1
        canvas_writer()


window = Tk()
window.title("French to English Flash Card App")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

canvas = Canvas()
canvas.config(width=800, height=526, background=BACKGROUND_COLOR,
              highlightthickness=0)

front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 526 / 2, image=front_image)
lang_text_canvas = canvas.create_text(400, 150, text="French",
                                      font=('Arial', 40, 'italic'))
word_text_canvas = canvas.create_text(400, 263, text=f"{french_data[key]}",
                                      font=('Arial', 60, 'bold'))
window.after(3000, func=flip_card)
canvas.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")
right_button = Button(image=right_image, highlightthickness=0,
                      command=right_button, background=BACKGROUND_COLOR)
wrong_button = Button(image=wrong_image, highlightthickness=0,
                      command=wrong_button, background=BACKGROUND_COLOR)
right_button.grid(row=1, column=1)
wrong_button.grid(row=1, column=0)
window.mainloop()

data_words_to_learn = pandas.DataFrame(words_to_learn)
data_words_to_learn.to_csv("data/words_to_learn.csv", index=False)
