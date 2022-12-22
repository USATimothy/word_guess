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

#Process guess compares a guess word to the target word and returns the result:
    # 2 for a correct letter in the correct place, 1 for a correct letter in another place.    
def process_guess(guessword,targetword):
    #Convert words from strings to lists
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

#evaluate_guess checks one guess word against a list of possible target words.
#It then counts the number of instances of each possible response.
def evaluate_guess(guessword,targetlist):
    responses=[]
    for targetword in targetlist:
        responses.append(process_guess(guessword,targetword))
    response_split=Counter(responses)
    return response_split

#find_best_guess calls evaluate_guess for every word in the guess list.
#It chooses the guess that trims the target list most effectively.
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

#whittle_list finds all the words in the target list that match the response
def whittle_list(guess,response,targetlist):
    return [word for word in targetlist if process_guess(guess,word)==response]

#this routine tests the solver by printing how drastically each successive
#guess reduces the number of possible words
def check_solver(wordlist,target_word=""):
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
    "For example, if the guess is SPORT and the answer is BROWN, type 00210\n" + 
    "Letters earlier in the word take priority -- if the guess is SPEED " +
    "and the answer is CHUTE, type 00100, not 00010.")
    print(message)
    possible_words=word_list
    guesses=['arose']
    responses=[]
    guess_word='arose' #saves computation time, since first guess is always the same
    response=get_response("What is the response for " + guess_word.upper() + "?\n")
    responses.append(response)
    possible_words=whittle_list(guess_word,response,possible_words)    
    while sum(response)<10:
        guess_word=find_best_guess(word_list,possible_words)
        response=get_response("What is the response for " + guess_word.upper() + "?\n")
        guesses.append(guess_word)
        responses.append(response)
        possible_words=whittle_list(guess_word,response,possible_words)
        if len(possible_words)<1:
            revealed_word = str(input('You stumped me! What was your word?\n')).lower()
            error_message=check_answers(revealed_word,guesses,responses,word_list)
            print('\n' + error_message)
            print('Please try again.')
            return

def check_answers(revealed_target,guessed_words,responses,all_playable):
    lrw = len(revealed_target)
    if revealed_target in guessed_words:
        error_message='Oops. I thought I had guessed that already.'
    elif lrw!=5:
        error_message=('Error: ' + revealed_target + ' has ' + str(lrw) + ' letters.' + 
              '\nOnly 5 letter words are allowed.')
    elif not re.search('[a-zA-Z]{5}',revealed_target):
        error_message='Error: word must contain only alphabetic characters a-z.'
    elif revealed_target not in all_playable:
        error_message='That word is not in my dictionary. I should learn more words!'
    else:
        for guess,response in zip(guessed_words,responses):
            correct_response = process_guess(guess,revealed_target)
            if response!=correct_response:
                error_message=(guess + ' and ' + revealed_target + ' sohould be' +
                               str(correct_response) + ' not ' +
                               str(response) + '.')
                break
        else:
            error_message= 'Great game! I guess I need to practice some more.'

    return error_message
    
                   