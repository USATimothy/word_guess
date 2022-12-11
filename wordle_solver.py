#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Wordle solver
#Programmed by Tim Fleck
#Started May 5th, 2022

from collections import Counter
import random
import re
#Import the dictionary
all_English_words = open('wordsEn.txt')
words5=[a[:5] for a in all_English_words if len(a)==6]
popular_English_words=open('popular 5-letter words.csv')
popwords5=[word[:5] for word in popular_English_words]

def process_guess(guessword,targetword):
    guess=[c for c in guessword]
    target=[c for c in targetword]
    response = [0,0,0,0,0]
    for i in range(5):
        if guess[i]==target[i]:
            response[i]=2
            guess[i]='*'
            target[i]='^'
    for i in range(5):
        for j in range(5):
            if guess[i]==target[j]:
                response[i]=1
                target[j]='@'
                break
    return tuple(response)

def evaluate_guess(guessword,targetlist):
    responses=[]
    for targetword in targetlist:
        responses.append(process_guess(guessword,targetword))
    response_split=Counter(responses)
    return response_split

def find_best_guess(guesslist,targetlist):
    bestbin=len(targetlist)+1
    bestguess='apple'
    for guessword in guesslist:
        splits=evaluate_guess(guessword,targetlist)
        maxbin=splits.most_common()[0][1]
        if maxbin<bestbin:
            bestguess=guessword
            bestbin=maxbin
        elif maxbin==bestbin:
            if guessword in targetlist:
                bestguess=guessword
    return bestguess

def whittle_list(guess,response,targetlist):
    return [word for word in targetlist if process_guess(guess,word)==response]

def play_wordle(wordlist,target_word=""):
    if not target_word:
        target_word=random.choice(wordlist)
    possible_words=wordlist
    response=(0,0,0,0,0)
    while sum(response)<10:
        if len(possible_words)==1:
            possible_word_s = ' possible word'
        else:
            possible_word_s = ' possible words'
        print(str(len(possible_words)) + possible_word_s)
        if len(possible_words)>6000:
            guess_word='aloes'
        elif len(possible_words)==3088:
            guess_word='arose'
        else:
            guess_word=find_best_guess(wordlist,possible_words)
        response=process_guess(guess_word,target_word)
        print(guess_word,response)
        possible_words=whittle_list(guess_word,response,possible_words)
    return

def get_response(ask_string):
    while True:
        response=input(ask_string)
        list_response=re.findall("\d",response)
        math_response=tuple([int(e) for e in list_response])
        if len(math_response)==5:
            for i in range(5):
                if math_response[i] not in [0,1,2]:
                    print('Enter a 0, 1, or 2 for each letter in the word')
                    break
            else:
                break
        else:
            print('Response must be 5 numbers separated by commas')
    return math_response
    
def solve_wordle(word_list):
    message = ("When entering responses, type 2 for correct letter and place; " + 
    "type 1 for correct letter and wrong place; type 0 for wrong letters. " +
    "Separate letters with commas.  For example, if the guess is SPORT " +
    "and the answer is BROWN, type 0,0,2,1,0\n")
    print(message)
    print('Guess "aloes"')
    response=get_response('What is the response for the guess "aloes"?\n')
    possible_words=whittle_list("aloes",response,word_list)
    while sum(response)<10:
        guess_word=find_best_guess(word_list,possible_words)
        print('Guess "' + guess_word)
        response=get_response('What is the response for your guess?\n')
        possible_words=whittle_list(guess_word,response,possible_words)
    
    
                   