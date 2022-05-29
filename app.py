from flask import Flask, redirect, url_for, request, render_template, session
from helper import reload_available_words
# from config import secret_key
import pandas as pd 
import random

app = Flask(__name__)
# app.secret_key = secret_key


random_phrase = random.choice(['From Wordle Dud to Wordle Stud', 'From Wordle Zero to Wordle Hero', 
'From Wordle Chump to Wordle Champ', 'From Wordle Whiner to Wordle Winner', 
'From Wordle Flop to Wordle Top', 'From Wordle “Oh Crap!” to Wordle “Oh Snap!”'])

## HOME PAGE
@app.route("/", methods=["GET", "POST"])
def home():

    # IF THE SESSION IS SET, WE USE THE SESSION DATA
    if 'loaded' in session:

        if request.method == 'POST':

            guess = request.form["guessedWord"]
            wrong_letters = request.form["wrongLetters"]
            right_spots = request.form["right_spots"]

            if session['loaded'] == 0:
                new_list_df = pd.read_csv("data\words.csv", sep=" ", header=None)
                new_list_df.rename(columns={0: 'W'}, inplace=True)

                available_word_list = []

                for i, r in new_list_df[new_list_df['W'].str.len() == 5].iterrows():

                    word = r['W']

                    available_word_list.append(word)

                session['loaded'] = 1

                session['Words'] = reload_available_words(guess, wrong_letters, right_spots, available_word_list)

            else:
                session['Words'] = reload_available_words(guess, wrong_letters, right_spots, session['Words'])

            
            return render_template("index.html", result=session['Words'], random_phrase=random_phrase)

    else:
        return redirect("/load")

@app.route("/load", methods=["GET"])
def firstload():

    session['guess_counter'] = 0
    session['loaded'] = 0

    return redirect("/")


if __name__ == "__main__":
    session.init_app(app)
    app.run()
