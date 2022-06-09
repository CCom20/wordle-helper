# wordle-helper
Wordle Helper (link: [wordle-guess-optimizer.herokuapp.com/](wordle-guess-optimizer.herokuapp.com/)) is a guess-optimizer for [Wordle](https://www.nytimes.com/games/wordle/index.html). While Wordle guesses max out at 6, Wordle Helper does not have a set max amount of guesses. Rather, Wordle Helper takes your guess and matches the correct and incorrect letters across a database of all possible words and returns a list of words with an "information value score". Based on this information, a list of words is curated and returned to the user with a score (as mentioned). The score changes based on the value of the word and the number of words left. So the information value is relative to the list of available words, not relative to the whole original list of words.
