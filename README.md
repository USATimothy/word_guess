# word_guess
Games for guessing a word based on number of common letters with guessed words.

In these games, one player (the chooser) thinks of a 5-letter word. The other player(s), the guesser(s), will attempt to guess the word. The chooser responds with how many letters the guessed word and the target word have in common. The process repeats until the correct word is guessed. Any valid word is allowed, regardless of whether it has been ruled about by information from previous guesses.

In the first, original variation, called fiveletterwords, only words with 5 unique letters are allowed. The chooser only tells the guesser how many letters are correct (i.e. shared between the guessed word and target word), and gives no information about which letters are correct or whether any are in the correct place. A skilled guesser (like the computer) can generally guess the 5 letters within 8 guesses; it may take more guesses to narrow down which of several anagrams (e.g. spear, spare, reaps, pears) is the target.

The more recent variation, called wordle, allows all 5-letter words, regardless of repeating letters. The chooser tells the guesser(s) whether each letter is in the correct place, in the wrong place, or not in the word at all. Since more information is given for each guess, a skilled player can generally guess the word within 4 guesses.

The code incorporates several strategies for finding the target in the fewest guesses.
