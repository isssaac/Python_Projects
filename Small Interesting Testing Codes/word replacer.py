def word_swapper(sentence, word):
    a = 'ABC'
    return a.join(sentence.split(word))

print(word_swapper('This is a sentence.', 'is'))
## will return 'ThABC ABC a sentence.'