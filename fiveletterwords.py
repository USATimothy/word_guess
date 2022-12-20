# -*- coding: utf-8 -*-
#@author: Timothy Fleck

import random
from collections import Counter
import re
#These are lists of English words, each with a newline character appended to the end.
#all_English_words is a larger dictionary than many_English_words.
all_English_words = open('WordsEn.txt')
many_English_words = open('popular 5-letter words.csv')
#These dictionaries pare down the lists to five-letter words with 5 unique letters.
#The newline character at the end of each word accounts for len=6 instead of 5
all_dictionary=[a[:5] for a in all_English_words if len(a)==6 and len(set(a))==6]
common_dictionary = [a[:5] for a in many_English_words if len(set(a))==6]


def best_guess(word_list,all_playable,strategy='no big bucket'):
    if strategy=='random':
        guess = random.choice(word_list)
    else:
        #The next two strategies look at which guess splits the possible words
        #into as many small buckets as possible, with a different bucket for
        #words that have 0,1,2,3,4, or 5 letters in common.
        q=len(word_list)/6
        S=[]
        if q<2:
            guesses=word_list
        else:
            guesses=all_playable
        for g in guesses:
            count0to5=Counter([len(set(g)&set(wl)) for wl in word_list])
            if strategy=='even_buckets':
                s=0
                for i in range(6):
                    s+=(count0to5[i]-q)**2
            else: #the default "no big bucket" strategy
                s=count0to5.most_common()[0][1]
            S.append(s)
        guess=guesses[S.index(min(S))]
    return guess

#The human player will come up with a target word, and the computer will try to
#guess it. The human player responds to each computer guess with 
#with how many letters the guess and the target have in common.
def guess_word(strategy,all_playable):
    #all_playable is all words that can be guessed.
    #whittled_list is all words that can possibly be the correct guess, given
    #the information from previous guesses. Before the first guess, the lists
    #are the same.
    whittled_list=all_playable
    guesses=[]
    responses=[]
    guess_number=0
    while guess_number<100:#If it takes more than 100 guesses, something wrong happened.
        guess=best_guess(whittled_list,all_playable,strategy)   
        guess_number+=1
        while True:
            try:
                response=int(input('How many letters does your word have in common with ' + guess + '?\n'))        
                if response in [0,1,2,3,4,5]:
                    break
                else:
                    print('The response must be an integer 0-5. Please try again')
            except:
                print('The response must be an integer 0-5. Please try again')
        guesses.append(guess)
        responses.append(response)
        if response==5:
            if input('Is it your word?\n')[0] in ['1','y','Y']:
                break
            else:
                whittled_list.remove(guess)
        whittled_list=[word for word in whittled_list if len(set(guess) & set(word))==response]
        if whittled_list==[]:
            revealed_word = str(input('You stumped me! What was your word?\n')).lower()
            error_message=check_answers(revealed_word,guesses,responses,all_playable)
            print('\n' + error_message)
            print('Please try again.')
            return ()
    print('Found in ' + str(guess_number) + ' guesses')
    return(guess_number,guess)

def check_answers(revealed_target,guessed_words,responses,all_playable):
    lrw = len(revealed_target)
    if revealed_target in guessed_words:
        error_message='Oops. I thought I had guessed that already.'
    elif lrw!=5:
        error_message=('Error: ' + revealed_target + ' has ' + str(lrw) + ' letters.' + 
              '\nOnly 5 letter words are allowed.')
    elif not re.search('[a-zA-Z]{5}',revealed_target):
        error_message='Error: word must contain only alphabetic characters a-z.'
    elif len(set(revealed_target))<5:
        error_message='Error: that word does not have 5 unique letters.'
    elif revealed_target not in all_playable:
        error_message='That word is not in my dictionary. I should learn more words!'
    else:
        for guess,response in zip(guessed_words,responses):
            correct_response = len(set(guess) & set(revealed_target))
            if response!=correct_response:
                error_message=(guess + ' and ' + revealed_target + ' have ' +
                               str(correct_response) + ' letters in common, not ' +
                               str(response) + '.')
                break
        else:
            error_message= 'Great game! I guess I need to practice some more.'

    return error_message

#Computer chooses a word. Human tries to guess it
def human_play(all_playable):
    target=random.choice(all_playable)
    guess_number=0
    guesses=[]
    responses=[]
    while guess_number<100:
        guess=str(input('What is your guess?\n')).lower()
        if guess == target:
            print('Congratulations! You got it!')
            return
        elif guess not in all_playable:
            print('Only common five-letter words with all unique letters are allowed.')
        else:
            response=len(set(guess) & set(target))
            guess_number+=1
            guesses.append(guess)
            responses.append(response)
            print('My word has ' + str(response) + ' letter(s) in common with ' + guess + '.')
            
        
if __name__ == "__main__":
    print('Pick a 5-letter word with all unique letters')
    game=guess_word('random',common_dictionary)
    print(game)
