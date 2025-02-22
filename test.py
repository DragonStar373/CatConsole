import sys
import time


def clear_to_start(text):
    lines = text.split('\n') # separate lines
    lines = lines[::-1] # reverse list
    nlines = len(lines) # number of lines

    for i, line in enumerate(lines): # iterate through lines from last to first
        sys.stdout.write('\r') # move to beginning of line
        sys.stdout.write(' ' * len(line)) # replace text with spaces (thus overwriting it)

        if i < nlines - 1: # not first line of text
            sys.stdout.write('\x1b[1A') # move up one line

    sys.stdout.write('\r') # move to beginning of line again


text = '''
this is my
multiline text
'''

text2 = '''
this is
multiline
'''

sys.stdout.write(text) # print text
sys.stdout.flush()
time.sleep(3) # sleep 3 seconds
clear_to_start(text) # clear lines and ascend to top
sys.stdout.write(text2) # overwrite text
