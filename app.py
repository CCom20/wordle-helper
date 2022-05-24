from flask import Flask, redirect, url_for, request, render_template, session
import pandas as pd 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        guess = request.form["guessField"]
        wrong_letters = request.form["wrongLettersField"]
        right_letters = request.form["rightLettersField"]
        return redirect("/", code=302)
        
    return render_template("index.html")

# def form():
#     if request.method == "POST":
#         guess = request.form["guessField"]
#         wrong_letters = request.form["wrongLettersField"]
#         right_letters = request.form["rightLettersField"]

#         pet = Pet(name=name, lat=lat, lon=lon)
#         db.session.add(pet)
#         db.session.commit()
#         return redirect("/", code=302)
#     return render_template("index.html")

while guess_counter < 7:
    
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
    
    if guess_counter == 7:
        break
    elif (len(right_spots) == 5) and (guess == right_spots):
        correct_word = word_check(guess)
        print(f'Congrats! The word is {correct_word}.')
        break
    else:
        next





if __name__ == "__main__":
    app.run()
