# -*- coding: utf-8 -*-
#@author: Timothy Fleck

import random
from collections import Counter
#These are lists of English words, each with a newline character appended to the end.
#all_English_words is a larger dictionary than many_English_words.
all_English_words = open('WordsEn.txt')
many_English_words = open('popular 5-letter words.csv')
#These dictionaries pare down the lists to five-letter words with 5 unique letters.
#The newline character at the end of each word accounts for len=6 instead of 5
all_dictionary=[a[:5] for a in all_English_words if len(a)==6 and len(set(a))==6]
common_dictionary = [a[:5] for a in many_English_words if len(set(a))==6]


#The computer will guess a word. The human player will come up with a word
#and respond with how many letters that target word has in common with each
#computer guess.
def guess_word(strategy,all_playable):
    #all_playable is all words that can be guessed.
    #whittled_list is all words that can possibly be the correct guess, given
    #the information from previous guesses. Before the first guess, the lists
    #are the same.
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
            revealed_word = str(input('You stumped me! What was your word?\n')).lower()
            lrw=len(revealed_word)
            if lrw!=5:
                print('Error: ' + revealed_word + ' has ' + str(lrw) + ' letters.' + 
                      '\nOnly 5 letter words are allowed.')
            elif len(set(revealed_word))<5:
                print('Error: that word does not have 5 unique letters.')  
            elif revealed_word not in all_playable:
                print('That word is not in my dictionary. I should learn more words!')
            else:
                print("Maybe I'm not very good at this game, or maybe " +
                      "one of your responses was inaccurate?")
            return ()
    print('Found in ' + str(k) + ' guesses')
    return(k,guess)

if __name__ == "__main__":
    print('Pick a 5-letter word with all unique letters')
    game=guess_word('random',common_dictionary)
    print(game)
