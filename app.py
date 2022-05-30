from flask import Flask, redirect, request, render_template, session
from helper import reload_available_words, words_list
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(16)


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

                available_word_list = words_list

                session['loaded'] = 1

                session['Words'] = reload_available_words(guess, wrong_letters, right_spots, available_word_list)

            else:
                session['Words'] = reload_available_words(guess, wrong_letters, right_spots, session['Words'])

            
            return render_template("index.html", result=session['Words'], random_phrase=random_phrase)

    else:
        session['guess_counter'] = 0
        session['loaded'] = 0

        return redirect("/")

    return render_template("index.html", result='', random_phrase=random_phrase)

@app.route("/reset")
def reset():
    session.clear()
    session['guess_counter'] = 0
    session['loaded'] = 0
    redirect('/')


if __name__ == "__main__":
    session.init_app(app)
    app.run()
