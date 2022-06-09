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

        # IF THE FIRST SESSION, LOAD DATA
        if session['loaded'] == 0:

            session['loaded'] = 1

            if request.method == 'POST':

                guess = request.form["guessedWord"]
                wrong_letters = request.form["wrongLetters"]
                right_spots = request.form["right_spots"]

                session['guessedWordsList'].append(guess)

                session['wordsLeft'] = reload_available_words(session['guessedWordsList'], wrong_letters, right_spots, words_list)

                return render_template("index.html", result=session['wordsLeft'], random_phrase=random_phrase, guess=session['guessedWordsList'])
            
            else:

                return render_template("index.html", result='', random_phrase=random_phrase, guess='')

        else:

            if request.method == 'POST':

                guess = request.form["guessedWord"]
                wrong_letters = request.form["wrongLetters"]
                right_spots = request.form["right_spots"]

                session['guessedWordsList'].append(guess)

                available_word_list = words_list
                session['Words'] = reload_available_words(guess, wrong_letters, right_spots, available_word_list)

                return render_template("index.html", result=session['Words'], random_phrase=random_phrase, guess=session['guessedWordsList'])

            else:

                return render_template("index.html", result=session['Words'], random_phrase=random_phrase, guess=session['guessedWordsList'])           
    else:
        session['loaded'] = 0
        session['guessedWordsList'] = []
        return redirect("/")

@app.route("/reset")
def reset():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    session.init_app(app)
    app.run()
