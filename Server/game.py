from json import load
from random import randint, choice

class Game:
    def __init__(self, username):
        self.words = self.init_words()

        self.level = "1"

        self.word_lenght = 0  # redifined in get_random_word
        self.progress = ""  # redifined in get_random_word
        # = list(random_word) to help with checking progress at self.event()
        self.random_word_list = []
        self.count = 0  # count to death gets redifined in get_random_word
        self.used_letters = []  # a list of used letters
        self.random_word = self.get_random_word()
        self.dead = False
        self.score = 0

    def shit_to_json(self):
        # no need to run this really unless the level needs to be raised
        with open("words.txt", 'r') as f:
            # open and read file content to a var
            file_content = f.read()

        word_list = [] 
        word = ""

        for letter in file_content:
            # change the long string into a list of words
            if letter == ',' or letter == ' ' or letter == '\n':
                word_list.append(word)
                word = ""
            else:
                word += letter

        words = {} # the dict to hold the words

        for word in word_list:
            lenght = len(word)  # get lenght of word
            level = lenght - 4  # get its level with

            # 1-4 = level 1
            # above 11 = level 11
            if level < 1:
                level = 1
            if level > 10:
                level = 11

            try:
                # a subset in this case the level as index and their words
                # example level 5 words is a subset of all the words in game
                subset = words[level]
            except KeyError as e:
                subset = {0: word}  # here the first subsets are created
                words.update({level: subset})
                continue  # because if not the first entry will be made twice

            last_key = sorted(subset.keys())[-1]  # get the last key
            new_key = last_key + 1  # append to it for next key
            subset.update({new_key: word})
            words.update({level: subset})

        with open("words.json", 'w') as f:
            json.dump(words, f)# no more need to run this really

    def init_words(self):
        """
        i have learnt hash tables as the most effiecient data structures in
        our field. Since i dont want my single core server trouble itselfwith
        10 stacks totalling to 97000 nodes i decided to work with a hash table 
        here. below is an example of the hash table to the best of my ability
                {
            level of words: {index of word: word}
        }

        so to get random word = 
            level of words = words[level]
                random word = level_of_words[random_num]
        """

        with open("words.json", 'r') as f:
            words = load(f)

        return words

    def update_dict(self, index):
        """remove the word in index of the current level"""
        words_in_level = self.words[self.level]  # get the subset of words
        del words_in_level[index]  # the index is actually an rng
        self.words.update({self.level: words_in_level}) # update superset

    def get_random_word(self):
        """get a random word with rng"""
        words_in_level = self.words[self.level]  # get the subset of words
        keys = sorted(words_in_level.keys())  # get all key into a list

        random_key = choice(keys)  # get a random key
        random_word = words_in_level[random_key]

        self.word_lenght = len(random_word)  # set the word lenght
        self.progress = "-" * self.word_lenght  # set the word progress to 0
        self.count = 0  # count to death gets redifined in get_random_word
        self.used_letters = []  # a list of used letters
        self.update_dict(random_key)  # remove current word for dict
        self.hints(random_word)
        self.random_word_list = list(random_word)

        return random_word

    def event(self, text):
        """fucntion to check if the letters inputted are contained in 
        random word. the letters are checked and counted individually"""
        # print("Text entered: " + text)  # debug

        text = list(text)  # turn it into a list
        indexes_chars = {}  # format: {index: char}

        for letter in text:
            self.used_letters.append(letter)

        for index, char in enumerate(text):
            # there are two loops here, one smaller and a bigger one inside it
            # the smaller one checks if the letter is in the bigger loop to 
            # avoid unnnecessary compute and if letter is in the bigger loop
            # all the indexes of where the letter is in bigger loop is updated 
            # to a dicitonary
            if char not in self.random_word_list:
                # increase count if a char is not in text
                self.count += 1
                if self.count == 7:
                    # end game condition here
                    self.dead = True
                    break  # break if so to end game.., rest depends on server

                continue

            for index2, char2 in enumerate(self.random_word_list):
                if char == char2:
                    # if char2 in text the index and char is added to a dict
                    # the index from self.random_word_list must be added
                    indexes_chars.update({index2: char})

        # print(indexes_chars)  # debug

        for k, v in indexes_chars.items():
            # update progression
            self.progress = f"{self.progress[:k]}{v}{self.progress[k+1:]}"

        check = self._check()
        
        return check

    def hints(self, random_word):
        """set some hints for the cry babies on the progression string"""
        level = int(self.level)
        if level < 4:
            # decision tree for the number of hints
            hint = 1
        elif level < 8:
            hint = 2
        else:
            hint = 3

        for h in range(hint):
            # apply hints
            random_num = randint(0, len(random_word)-1)
            random_char = random_word[random_num]

            self.progress = f"{self.progress[:random_num]}{random_char}{self.progress[random_num+1:]}"

    def _check(self):
        # check if current progression is enough for next word
        progress = list(self.progress)
        if "-" not in progress:
            # next word contidition
            # set score before statement to avoid sending unupdated score to
            # user and set self.random_word last to avoud sending the current
            # word to the user 
            self.score += (self.word_lenght ** 2) + (self.word_lenght * 2)
            statement = f"nextword {self.random_word} {self.score}"
            self.random_word = self.get_random_word()

            return statement

    def update_level(self, inp):
        """update and adjust the level"""
        # turn it into int to adjust
        try:
            level = int(inp)
        except Exception as e:
            print(e)

        if level > 11:
            # also turn it back into a str here
            level = "11"
        elif level < 1:
            level = "1"
        else:
            level = str(level)

        self.level = level  # update class attribute

        return "levelled " + level