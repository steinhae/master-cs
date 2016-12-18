[Description]
For solving practical 1, I decided to use a BKTree and leveraging the A* serach.
It was quite time intesive to come up with that combination, before I tried several other things. 
If you only want to read about my final attempt go to [Third attempt]. 

[First attempt]
I tried to prone the search tree by calculating the difference between the start and endword i.e.: 
Start word:  lead
End word  :  gold
Letters and operations to transform startword into endword including operation --> {'a': '-', 'e': '-', 'g': '+', 'o': '+'}
Based on that I created a tree with permutations of each entry and did a BFS on it. 
To find all words in the wordlist which can be reached from a startword by adding or removing a letter I created a method 
"generateWordsAsTuple(start_word, operationLetter[letter], letter)". In this method I added or removed the letter from
the start_word, sorted the new word and compared it with a list of all sortedWords from the wordlist. If there was a match 
I looked up the word in the actual wordlist (which takes much more time).
The solution works (found solutions to all given test cases) and is really fast, 
but not complete in terms of it would not be able to find words if there is a detour
(in case you have to add a letter which is not in startword or endword and remove it later)

[Second attempt]
I used the same algorithm with the whole alphabet and both operations "+" and "-" for each letter.
The search space was way to big so the algorithm never terminated or took really long.

[Third attempt]
At this point I thought there must be a way to get all words with a specific distance from a start word.
I did some research and found the BKTree. Burkhard-Keller Trees are a tree-based data structure engineered 
for quickly finding near-matches to a string. I found a python implementation here https://github.com/ahupp/bktree/blob/master/bktree.py.
To search the BKTree I used a BFS. 
There were three problems:
1. everytime i executed the script it would take around 40 seconds to build the tree
2. the pathes were too short because string replacements were allowed
3. it would take too long for some word combinations to find a solution
I solved them the following way: 
[Solution to 1] 
I found the python package Pickel which I used to serialize the BKTree and save it to the hard disc. So I had 
to calculate it only the first time and then just load it from disc. This reduced setup time from 40s to 4s. 
I looked further to optimize it even more and found a c-Version of it called cPickle which reduced the setup time
further from 4s to <1s.
[Solution to 2]
In order to create and search the BKTree, a way to compare strings is needed. The canonical method for this is the Levenshtein Distance, which takes two strings, and returns a number representing the minimum number of insertions, deletions and replacements required to translate one string into the other.
One requirement of the exercise was that one can only insert or delete one letter per step. So I figured I had to change the Levenshtein function to meet 
the requirement. I changed the cost for the substitution to a very high value (1000) so that it is not a reasonable option anymore.
[Solution to 3]
I decided to replace the BFS by a A*serach. I found a python solution for A*search (http://www.redblobgames.com/pathfinding/a-star/implementation.html) and 
customized it to work with the rest of my script.

 
Python version:
Python 2.7.12

Used packages: 
from itertools import imap, ifilter
import sys
import time
import cPickle
import os.path
import heapq

Additional information:
The implementation of (class: PriorityQueue; methods: reconstruct_path, heuristic, a_start_search) is based on this article:
http://www.redblobgames.com/pathfinding/a-star/implementation.html

The implementation of (class: BKTree; methods: levenshtein, dict_words) is based on the description in this article:
http://blog.notdot.net/2007/4/Damn-Cool-Algorithms-Part-1-BK-Trees
Licensed under the PSF license: http://www.python.org/psf/license/
by Adam Hupp <adam@hupp.org>
Found at https://github.com/ahupp/bktree/blob/master/bktree.py



