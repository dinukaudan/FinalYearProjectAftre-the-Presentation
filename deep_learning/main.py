from tkinter import *
from tkinter import messagebox

from deep_learning.core import get_prediction_for_user_id
from deep_learning.core import train_model
from deep_learning.extract_features import extract_features


def run_learning_application():
    def train():
        train_model()

    def extract():
        extract_features()

    def predict():
        user_id = username_entry.get()
        answer = get_prediction_for_user_id(user_id)
        messagebox.showinfo('Predicted Answer', answer)

    window = Tk()
    window.configure(bg="white")
    window.title("GitHub User Expertise Predictor")
    title_label = Label(window, text="GitHub User Expertise Predictor", wraplength=300, bg="#2c2c54", fg='white',
                        font=('Arial', 15))
    title_label.pack(fill=X)
    learn_frame = Frame(window, bg='white')
    extract_button = Button(learn_frame, text="Extract User Features", command=extract, bg="#2c4c74", fg='white')
    extract_button.pack(fill=BOTH, padx=40, pady=7)
    train_button = Button(learn_frame,
                          text="Train", command=train, bg="#2c4c74", fg='white')
    train_button.pack(fill=BOTH, padx=40, pady=7)
    learn_frame.pack(fill=BOTH, pady=20)
    # -----------------
    predict_frame = Frame(window, bg='white')
    input_frame = Frame(predict_frame, pady=10, bg='white')
    username_label = Label(input_frame, text="Enter username to predict expertise", wraplength=300, bg="white")
    username_label.grid(column=0, row=0)
    username_entry = Entry(input_frame, bg='white')
    username_entry.grid(column=1, row=0)
    input_frame.grid_columnconfigure(0, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)
    input_frame.pack(fill=BOTH, padx=30)
    predict_button = Button(predict_frame, text="Predict", command=predict, bg="#d35400", fg='white')
    predict_button.pack(fill=BOTH, padx=40, pady=20)
    predict_frame.pack(fill=BOTH)
    window.mainloop()
