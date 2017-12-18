# Donovan Schroeder

######################################################################
# returns content of file as a single string
# lines of all uppercase text are removed
# blank lines are also removed
def getBook(file):
    '''returns contents of file as string with empty and all uppercase lines excluded'''
    lineList = []
    try:
        fopen = open(file)
    except:
        print("File couldn't be opened: ", file)
        exit()
    for line in fopen:
        line = line.rstrip()
        if not line.isupper():
            lineList.append(line)
    fopen.close()
    return(' '.join(lineList)) #join with space so first and last words of sentences aren't joined

######################################################################
# returns file that's been retrieved by getBook
# with any punctuation other than . removed
# or replaced with .
def cleanup(text):
    '''returns string with all punctuation removed
except for periods, question marks, and exclamation marks
question and exclamation marks are replaced with periods'''
    badPunct = (('(',' '),(')',' '),(',',' '),("'s",''),(':',' '),(';',' '),('-',' '),('"',' '),("'",''),('_',' '),('*',' '),('!','.'),('?','.')) #can add additional replacements here in pair of (target element, replacement)
    for punctuation in badPunct:
        text = text.replace(punctuation[0], punctuation[1])
    return(' '.join(text.split())) #the split and join are to remove extra spaces created by turning hyphen into spaces

######################################################################
# returns a list of words in file from cleanup
# list has no punctuation and is lowercase
# currently is by default in the order the words appear in book
def extractWords(text):
    '''returns lowercase list of words in argument by replacing periods with spaces and splitting at space'''
    return(text.replace(".", " ").lower().split())

######################################################################
# returns list of strings
# the strings are sentences with no punctuation
def extractSentences(text):
    '''returns list of sentences by splitting string at periods'''
    sentList = []
    for sentence in text.split("."):
        sentence = sentence.strip() #removes extra spaces at start and end of line
        if len(sentence) != 0: #stops empty elements from being appended
            sentList.append(sentence)
    return(sentList)

######################################################################
# returns integer equal to number of vowels in word
# for this function, vowels are defined as aeiou
# syllables are vowels and y that follow non vowels or y
# value of atleast one
def countSyllables(word):
    '''returns an integer with value equal to number of vowels in argument
For this function vowels are defined as letters a, e, i, o, u, or y
That don't follow a, e, i, o, or u.'''
    sylCount = 0
    vowels = 'aeiou'
    i = 0
    vbool = False #initialize as False because first vowel is a syllable
    if word[-1] in 'es': #remove trailing e or s as per hw instructions
        word = word[:-1]
    while i < len(word):
        while word[i] in vowels:
            if vbool == False: #add a syllable when vowel following non vowel
                sylCount += 1
            vbool = True
            i += 1
            if i == len(word):
                return(sylCount) #return early no more characters in string
        while word[i] == 'y':
            if vbool == False and i != 0: #y following non vowel adds syllable, but first y such as in you doesn't
                sylCount += 1
            vbool = False #vowel following y will be counted as syllable
            i += 1
            if i == len(word):
                return(max(sylCount,1)) #must check max because a single y would have sylcount = 0
        while word[i] not in vowels and word[i] != 'y': #handles consonants by setting up next vowel or y to be a syllable
            vbool = False
            i += 1
            if i == len(word):
                break
    return(max(sylCount, 1))

######################################################################
# returns float equal to Automated Readability Score of text
# the score is an equation with variables cpw and wps
# cpw is avg characters per word / wps is avg words per sentences
def ars(text):
    '''returns a float equal to the Automated Readability Score of the text.
Input should be a string such as one received from cleanup and getBook'''
    wordList = extractWords(text)
    cpw = sum([len(word) for word in wordList])/len(wordList) #avg word length by total word length / amount of words
    wps = len(wordList) / len(extractSentences(text)) #wps = total words / total sentences
    return(4.71*cpw + 0.5*wps - 21.43)

######################################################################
# returns float equal to Flesch-Kincaid Index of text
# score is an equation with variables wps and spw
# wps is avg words per sentences / spw is avg syllables per word
def fki(text):
    '''returns a float equal to Flesch-Kincaid Index of the text.
Input should be a string such as one received from cleanup and getBook'''
    wordList = extractWords(text)
    wps = len(wordList) / len(extractSentences(text)) #same as wps in ars
    spw = sum([countSyllables(word) for word in wordList]) / len(wordList) #avg syllables per word by sum sylcount of all words / amount of words
    return(0.39*wps + 11.8*spw - 15.59)

######################################################################
# returns float equal to Coleman-Liau Index of text
# score is an equation with variables cphw and sphw
# cphw is avg characters per 100 words / sphw is avg characters per 100 words
def cli(text):
    '''returns a float  equal to the Coleman0Liau Index of the text.
Input should be a string such as one received from cleanup and getBook'''
    cphw = sum([len(word) for word in extractWords(text)])/(len(extractWords(text))/100) #avgs word length per 100 words by using earlier cpw and divide numerator by 100
    sphw = len(extractSentences(text))/(len(extractWords(text))/100) #avgs sentences per 100 words by ratio of sentences divided by words/100
    return(0.0588*cphw - 0.296*sphw - 15.8)

######################################################################
# Reads in a book from a file and evaluates its readability. Returns
# None.
def evalBook(file):
    text = cleanup(getBook(file))
    print("Evaluating {}:".format(file.upper()))
    print("  {:5.2f} Automated Readability Score".format(ars(text)))
    print("  {:5.2f} Flesch-Kincaid Index".format(fki(text)))
    print("  {:5.2f} Coleman-Liau Index".format(cli(text)))
