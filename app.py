from flask import Flask, redirect, url_for, request, render_template, session
import pandas as pd 
import random

app = Flask(__name__)

random_phrase = random.choice(['From Wordle Dud to Wordle Stud', 'From Wordle Zero to Wordle Hero', 
'From Wordle Chump to Wordle Champ', 'From Wordle Whiner to Wordle Winner', 
'From Wordle Flop to Wordle Top', 'From Wordle “Oh Crap!” to Wordle “Oh Snap!”'])

@app.route("/", methods=["GET", "POST"])
def home():

    new_list_df = pd.read_csv("data\english3.csv", sep=" ", header=None)
    new_list_df.rename(columns={0: 'W'}, inplace=True)

    available_word_list = []

    for i, r in new_list_df[new_list_df['W'].str.len() == 5].iterrows():
    
        word = r['W']
        word_letters = list(r['W'])
        
        available_word_list.append({'Word': word, 'Letters': word_letters})

    guess_counter = 0

    if request.method == "POST":
    
        guess = request.form["guessedWord"]
        wrong_letters = request.form["wrongLetters"]
        right_spots = request.form["right_spots"]

        right_letters = [x for x in guess if x not in wrong_letters]

        check_letters = [x for x in right_letters if x not in right_spots]

        exclude_list = []

        # Exclude all words where the letter is correct but the index of the letter is not
        for x in check_letters:

            for w in available_word_list:

                try:
                    if x not in w['Letters']:
                        exclude_list.append(w)
                    else:
                        next
                except:
                    next

                try:
                    if guess.index(x) == w['Letters'].index(x):
                        exclude_list.append(w)
                    else:
                        next
                except:
                    next

        # Exclude all words containing the wrong letters
        for x in wrong_letters:
            for w in available_word_list:
                if x in w['Letters']:
                    exclude_list.append(w)
                else:
                    next

        # Exclude all words where letter is not in the right index

        for x in right_spots:
            for w in available_word_list:
                try:
                    if guess.index(x) != w['Letters'].index(x):
                        exclude_list.append(w)
                    else:
                        next
                except:
                    exclude_list.append(w)

        # Reset available words list

        available_word_list = [x for x in available_word_list if x not in exclude_list]

        # Get each letter's weight/value

        letter_count_dictionary = {}
        for x in available_word_list:
            for l in x['Letters']:
                if l not in letter_count_dictionary:
                    letter_count_dictionary[f'{l}'] = 0
                    for a in available_word_list:
                        if l in a['Letters']:
                            letter_count_dictionary[f'{l}'] +=1
                else:
                    next

        top_words = {}

        for w in available_word_list:
            word_weight = 0

            for l in w['Word']:

                word_weight += letter_count_dictionary[l]

            if w['Word'] not in top_words:
                word = w['Word']
                top_words[word] = word_weight
            else:
                next

        # {k: v for k, v in sorted(top_words.items(), key=lambda item: item[1], reverse=True)}
        top_list_exlude = {}
        for x in top_words:
            word_sum = 0
            for l in x:
                word_sum += x.count(l)
            if word_sum > 5:
                top_list_exlude[f'{x}'] = top_words[x]

        # Reset top words list based on no repeats and order by their expected information value
        suggested_words = [{x: top_words[x] for x in top_words if x not in top_list_exlude}]
        top_words = {k: v for k, v in sorted(suggested_words[0].items(), key=lambda item: item[1], reverse=True)} 
        for x in top_words:
            print(f'Word: {x}, Information Value: {round(top_words[x] / len(top_words), 2)}')

        guess_counter += 1
        
        if guess_counter == 6 and len(right_spots) !=5:
            game_over = 'Sorry, it looks like you were not able to guess the word.'
        elif (len(right_spots) == 5) and (guess == right_spots):
            correct_word = word_check(guess)
            game_over = f'Congrats! The word is {correct_word}.'
        else:
            next

        return render_template("index.html", code=302, result=top_words)

    return render_template("index.html", random_phrase=random_phrase, result='')


if __name__ == "__main__":
    app.run(debug=True)
