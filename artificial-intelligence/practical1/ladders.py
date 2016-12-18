from itertools import imap, ifilter
import sys
import time
import cPickle
import os.path
import heapq

def main(argv):

    start_time = time.time()

    if len(argv) != 3:
        print "Please provide exactly two arguments: [startWord] [endWord]"
        return

    start_word = argv[1]
    end_word = argv[2]

    tree_filename = "tree.p"
    word_list_filename = "wordList.txt"

    sorted_start = "".join(sorted(start_word))
    sorted_end = "".join(sorted(end_word))

    word_list = [line.rstrip('\n') for line in open(word_list_filename)]
    sorted_word_list_filename = map(lambda x:  "".join(sorted(x)), word_list)

    if start_word not in word_list:
        print "Start word " + start_word + " not in " + word_list_filename
        return
    if end_word not in word_list:
        print "End word " + end_word + " not in " + word_list_filename
        return

    # Step 1: Build BK-Tree or load from hard disc
    #print "Building tree..."
    if os.path.isfile(tree_filename):
        tree = cPickle.load( open( tree_filename, "rb" ) )
    else:
        tree = BKTree(levenshtein, dict_words(sorted_word_list_filename))
        cPickle.dump( tree, open( tree_filename, "wb" ) )
    #print "Done in %s seconds" % (time.time() - start_time)

    # Step 2: A* search to find path
    came_from, cost = a_star_search(tree, sorted_start, sorted_end)

    # Step 3: Reconstruct path and find original words to sorted words
    sorted_path = reconstruct_path(came_from, sorted_start, sorted_end)
    path = unsort_path(sorted_path, word_list, start_word, end_word)

    # Step 4: Print results
    print "<solution to " + start_word + " - " + end_word + ">"
    print "Path: " + path
    print "Steps: " + str(cost[sorted_end])
    print "--- %s seconds ---" % (time.time() - start_time)

def unsort_path(sorted_path, word_list, start, end):
    path = start
    sorted_path = sorted_path[1:-1]
    symbol = " --> "
    for word in sorted_path:
        unsorted_words = filter(lambda x: filter_words(x, word), word_list)
        path = path + symbol + unsorted_words[0]
    return path + symbol + end

def filter_words(word, sortedWord):
    if len(word) == len(sortedWord):
        if "".join(sorted(word)) == sortedWord:
            return True
    return False

"""
The implementation of (PriorityQueue, reconstruct_path, heuristic, a_start_search) is based on this article:
http://www.redblobgames.com/pathfinding/a-star/implementation.html
"""
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse() # optional
    return path

def heuristic(a, b):
    return levenshtein(a, b)

def a_star_search(tree, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in tree.query(current, 1):
            next = next[1]
            new_cost = cost_so_far[current] + heuristic(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

"""
The implementation is based on the description in this article:
http://blog.notdot.net/2007/4/Damn-Cool-Algorithms-Part-1-BK-Trees
Licensed under the PSF license: http://www.python.org/psf/license/
- Adam Hupp <adam@hupp.org>
"""
class BKTree:
    def __init__(self, distfn, words):
        """
        Create a new BK-tree from the given distance function and
        words.

        Arguments:

        distfn: a binary function that returns the distance between
        two words.  Return value is a non-negative integer.  the
        distance function must be a metric space.

        words: an iterable.  produces values that can be passed to
        distfn

        """
        self.distfn = distfn

        it = iter(words)
        root = it.next()
        self.tree = (root, {})

        for i in it:
            self._add_word(self.tree, i)

    def _add_word(self, parent, word):
        pword, children = parent
        #print pword
        d = self.distfn(word, pword)
        if d in children:
            self._add_word(children[d], word)
        else:
            children[d] = (word, {})

    def query(self, word, n):
        """
        Return all words in the tree that are within a distance of `n'
        from `word`.

        Arguments:

        word: a word to query on

        n: a non-negative integer that specifies the allowed distance
        from the query word.

        Return value is a list of tuples (distance, word), sorted in
        ascending order of distance.

        """
        def rec(parent):
            pword, children = parent
            d = self.distfn(word, pword)
            results = []
            if d <= n:
                results.append( (d, pword) )

            for i in range(d-n, d+n+1):
                child = children.get(i)
                if child is not None:
                    results.extend(rec(child))
            return results

        # sort by distance
        return sorted(rec(self.tree))


# http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
def levenshtein(s, t):
    #if levenshteinBrain.has_key((s,t)):
    #    return levenshteinBrain[(s,t)]
    m, n = len(s), len(t)
    d = [range(n+1)]
    d += [[i] for i in range(1,m+1)]
    for i in range(0,m):
        for j in range(0,n):
            cost = 1000
            if s[i] == t[j]: cost = 0

            d[i+1].append( min(d[i][j+1]+1, # deletion
                               d[i+1][j]+1, #insertion
                               d[i][j]+cost) #substitution
                           )
    return d[m][n]

def dict_words(iteralable):
    "Return an iterator that produces words in the given dictionary."
    return ifilter(len, iteralable)

main(sys.argv)
