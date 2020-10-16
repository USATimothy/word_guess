# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 11:08:01 2016

@author: odin
"""
import random
from collections import Counter
#This is all English words, each with a newline character appended to the end
all_English_words = open(r'/Users/odin/Downloads/wordsEn.txt')

#all_playable is all words with 5 total letters and 5 unique letters.
#Newline character at the end of each word accounts for len=6 instead of 5
all_playable=[a[:5] for a in all_English_words if len(a)==6 and len(set(a))==6]
#all_playable is all words that can be chosen as Player 1, or guessed by other players.
#whittled_list  is all words that are still possibilities, based on previous guesses.
#Initialize whittled_list to all_playable
whittled_list=all_playable


def guess_word(strategy,all_playable):
    whittled_list=all_playable
    k=0
    while k<100:#If k>100, something wrong happened.
        if strategy=='random':
            #This strategy picks a word at random from the whittled_list.
            guess=random.choice(whittled_list)
        if strategy=='even_buckets':
            #This strategy picks the word that has the most evenly sized buckets
            #for words that have 0 to 5 letters in common with the guess
            q=len(whittled_list)/6
            S=[]
            if q<2:
                guesses=whittled_list
            else:
                guesses=all_playable
            for g in guesses:
                count0to5=Counter([len(set(g)&set(wl)) for wl in whittled_list])
                s=0
                for i in range(6):
                    s+=(count0to5[i]-q)**2
                S.append(s)
            guess=guesses[S.index(min(S))]
        if strategy=='no_big_bucket':
            #This strategy looks at which guess has the fewest words that share
            #0,1,2,3,4, or 5 letters with it, whichever is most.
            q=len(whittled_list)/6
            S=[]
            if q<2:
                guesses=whittled_list
            else:
                guesses=all_playable
            for g in guesses:
                count0to5=Counter([len(set(g)&set(wl)) for wl in whittled_list])
                s=count0to5.most_common()[0][1]
                S.append(s)
            guess=guesses[S.index(min(S))]
        k+=1
        x=int(input('How many letters does your word have in common with ' + guess + '?\n'))        
        if x==5:
            if input('Is it your word?\n')[0] in ['1','y','Y']:
                break
            else:
                whittled_list.remove(guess)
        whittled_list=[word for word in whittled_list if len(set(guess) & set(word))==x]
        if whittled_list==[]:
            print('Error: possible mistake in counting common letters')
            return ()
    print('Found in ' + str(k) + ' guesses')
    return(k,guess)

if __name__ == "__main__":
    print('Pick a 5-letter word with all unique letters')
    game=guess_word('random',all_playable)
    print(game)