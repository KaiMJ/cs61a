"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> choose(ps, s, 0)
    'hi'
    >>> choose(ps, s, 1)
    'fine'
    >>> choose(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    selected = list(filter(select, paragraphs))
    if len(selected) <= k:
        return ''
    return selected[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def contains(words):
        for word in split(words):
            if lower(remove_punctuation(word)) in topic:
                return True
        return False

    return contains

    return contains
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    Arguments:
        typed: a string that may contain typos
        reference: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    typed_length = len(typed_words)
    reference_words = split(reference)
    reference_length = len(reference_words)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"

    if len(reference_words) == 0:
        if len(typed_words) == 0:
            return 100.0
        else:
            return 0.0
    else:
        if len(typed_words) == 0:
            return 0.0

    correct = 0 # / typed_length
    for i in range(min(typed_length, reference_length)):
        if reference_words[i] == typed_words[i]:
            correct += 1
    return correct / (typed_length) * 100.0

    
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return len(typed)/5.0 * (60/elapsed)
    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        valid_words: a list of strings representing valid words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if typed_word in valid_words:
        return typed_word

    scores = [ diff_function(typed_word, word, limit) for word in valid_words]
    if min(scores) > limit:
        return typed_word
    else:
        index = scores.index(min(scores))
        return valid_words[index]

    # END PROBLEM 5


def feline_flips(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths and returns the result.

    Arguments:
        start: a starting word
        goal: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_flips("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_flips("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_flips("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_flips("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_flips("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    def helper(start_, goal_, count):
        if len(start_) == 0:
            return len(goal_)
        if len(goal_) == 0:
            return len(start_)
        if count > limit:
            return count + 1

        if start_[0] == goal_[0]:
            return helper(start_[1:], goal_[1:], count)
        else:
            return 1 + helper(start_[1:], goal_[1:], count+1)

    return helper(start, goal, 0)


    # END PROBLEM 6


def minimum_mewtations(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.

    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """

    if limit == 0:  # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        return max(len(goal), len(start))
        # END

    elif start == goal:  # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 0
        # END

    else:
        index = None
        total = max(len(start), len(goal))

        for i in range(min(len(start), len(goal))):
            if start[i] != goal[i]:
                index = i
                break
        diff = len(goal) - len(start)

        add = total
        remove = total
        substitute = total

        if index != None:
            add = 1 + minimum_mewtations(start[:index] + goal[index] + start[index:], goal, limit-1)
            remove = 1 + minimum_mewtations(start[:index] + start[index+1:], goal, limit-1)
            substitute = 1 + minimum_mewtations(start[:index] + goal[index] + start[index+1:], goal, limit-1)
        else:
            if diff > 0:
                add = diff
            if diff < 0:
                remove = abs(diff)

        # BEGIN
        "*** YOUR CODE HERE ***"
        return min(add, remove, substitute)
        # END

minimum_mewtations("wird", "bird", 10)
def final_diff(start, goal, limit):
    """A diff function that takes in a string START, a string GOAL, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(sofar, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        sofar: a list of the words input so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        send: a function used to send progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> sofar = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(sofar, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    count = 0
    for i in range(len(sofar)):
        if sofar[i] == prompt[i]:
            count = i+1
        else:
            break
    
    progress = count / len(prompt)
    
    send({"id" : user_id, "progress" : progress})
    return progress

    
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> game = time_per_word(p, ['collar', 'plush', 'blush', 'repute'])
    >>> get_words(game)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_times(game)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    result = []
    for t in range(len(times_per_player)):
        temp = []
        for i in range(len(times_per_player[t])-1):
            temp.append(times_per_player[t][i+1] - times_per_player[t][i])
        result.append(temp)
    return game(words, result)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(game(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    """
    player_indices = range(len(get_times(game)))  # contains an *index* for each player
    word_indices = range(len(get_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    
    # for each words,
    # get corresponding player times
    # get the word and put it in player's result []

    result = [ [] for p in player_indices]
    for w in word_indices:
        shortest = max([t for p in get_times(game) for t in p])
        word = word_at(game, w)
        pIdx = 0
        for p in player_indices:
            t = get_times(game)[p][w]
            if t < shortest:
                shortest = t
                pIdx = p
        result[pIdx].append(word)
    return result
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def get_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def get_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
