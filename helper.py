import pandas as pd 
import csv

def reload_available_words(guess, wrong_letters, right_spots, available_word_list):
        
    available_word_list = available_word_list
    right_letters = [x for x in guess if x not in wrong_letters]
    check_letters = [x for x in right_letters if x not in right_spots]

    exclude_list =[]

    # If a right letter is not in a word, let's exclude that word
    for x in right_letters:
        for w in available_word_list:
            if x not in list(w):
                exclude_list.append(w)
            else:
                next


    # Exclude all words where the letter is correct but the index of the letter is not
    for x in check_letters:

        for w in available_word_list:

            try:
                if x not in list(w):
                    exclude_list.append(w)
                else:
                    next
            except:
                next

            try:
                if guess.index(x) == list(w).index(x):
                    exclude_list.append(w)
                else:
                    next
            except:
                next

    # Exclude all words containing the wrong letters
    for x in wrong_letters:
        for w in available_word_list:
            if x in list(w):
                exclude_list.append(w)
            else:
                next

    # Exclude all words where letter is not in the right index

    for x in right_spots:
        for w in available_word_list:
            try:
                if guess.index(x) != w.index(x):
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
        for l in list(x):
            if l not in letter_count_dictionary:
                letter_count_dictionary[f'{l}'] = 0
            else:
                letter_count_dictionary[f'{l}'] += 1

    top_words = {}

    for w in available_word_list:
        word_weight = 0

        for l in w:

            word_weight += letter_count_dictionary[l]

        if w not in top_words:
            word = w
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
    if len(suggested_words) < 15:
        top_words = {k: v for k, v in sorted(top_words.items(), key=lambda item: item[1], reverse=True)}
    else:
        top_words = {k: v for k, v in sorted(suggested_words[0].items(), key=lambda item: item[1], reverse=True)} 
        
    return top_words