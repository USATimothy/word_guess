# word_guess
Game for guessing a word based on number of common letters with guessed words.

In this game, one player thinks of a 5-letter word with all unique letters (the target word). The other player(s), in this case the computer, will attempt to guess the word. The first player responds with how many letters the guessed word and the target word have in common. Position within the word is unimportant.

All guesses must fit the general criteria (5 unique letters); however, guesses that conflict with previous information are allowed. Otherwise the game would be very difficult for human players. The computer can generally guess the 5 letters within 8 guesses; it may take more guesses to narrow down which of several anagrams (e.g. spear, spare, reaps, pears) is the target.

The code incorporates several strategies for finding the target in the fewest guesses.
