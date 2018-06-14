"""Generate Markov text from text files."""

from random import choice
import sys
import twitter
import os

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    text_string = open(file_path).read()

    return text_string


def make_chains(text_string, n_gram):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """
    words = text_string.split()
    

    chains = {}
    
    for i in range(len(words) - n_gram):
        
        words_key = tuple(words[i:n_gram + i])

        add_word = words[i + n_gram]

        if words_key in chains:
            chains[words_key].append(add_word)
        else:
            chains[words_key] = [add_word]

   
    
    return chains


def make_text(chains, n_gram):
    """Return text from chains."""

    words = []
    keys_lst = list(chains.keys())

    #start point
    link_tpl = choice(keys_lst)

    while not link_tpl[0][0].isupper():
        link_tpl = choice(keys_lst)

    words.extend(list(link_tpl))
    
    count_char = 0
    while link_tpl in chains and count_char < 281:
        
        link_word_str = choice(chains[link_tpl])
        words.append(link_word_str)
        count_char = len(' '.join(words))
        #if count_char > 279 and link_tpl[-1][-1] in ".!?":
         #   break
        #else:
        link_tpl = tuple(words[-n_gram:])


    return " ".join(words)


def make_tweet(random_text):

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    )

    status = api.PostUpdate(random_text)
    print(status.text)


input_path = sys.argv[1]
n_gram = int(sys.argv[2])

while True:
    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)

    # Get a Markov chain
    chains = make_chains(input_text, n_gram)

    # Produce random text
    random_text = make_text(chains, n_gram)
    print(random_text)
    print('\n')

    make_tweet(random_text)

    user_input = input("Enter to tweet again [q to quit] > ")
    if user_input.lower() == 'q' or user_input.lower() == 'quit':
        break