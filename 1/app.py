import random, copy
from enum import Enum
from typing import Set, Dict, Tuple, List, Union

import numpy
import pandas


def words_by_pattern(
        words: Set[str],
        index: Dict[Tuple[chr, int], Set[str]],
        pattern: List[Union[chr, None]]
) -> List[str]:
    target_set = words
    match = False
    for position, letter in enumerate(pattern):
        if letter is not None:
            if (letter, position) not in index:
                return list()
            if not match:
                match = True
                target_set = index[(letter, position)]
            else:
                target_set = target_set.intersection(index[(letter, position)])
    clear_set: List[str] = list()
    for word in target_set:
        if len(word) == len(pattern):
            clear_set.append(word)
    return clear_set


class Direction(Enum):
    HORIZ = 1
    VERT = 2
    MAIN_DIAG = 3
    SECOND_DIAG = 4


class Order(Enum):
    Direct = 1
    Indirect = 2


class Line:
    def __init__(self, matrix: List[List[chr]],
                 point: Tuple[int, int],
                 direct: Direction):
        self.__matrix = matrix
        self.__center = point
        self.__w, self.__h = len(matrix[0]), len(matrix)
        x0, y0 = point

        if direct == Direction.HORIZ:
            self.__left_point = (0, y0)
            self.__step = (1, 0)
        elif direct == Direction.VERT:
            self.__left_point = (x0, 0)
            self.__step = (0, 1)
        elif direct == Direction.MAIN_DIAG:
            if x0 >= y0:
                self.__left_point = (x0 - y0, 0)
            else:
                self.__left_point = (0, y0 - x0)
            self.__step = (1, 1)

        elif direct == Direction.SECOND_DIAG:
            if x0 < self.__h and y0 < self.__h - x0:
                self.__left_point = (0, y0 + x0)
            else:
                self.__left_point = (x0 - (self.__h - y0 - 1), self.__h - 1)
            self.__step = (1, -1)
        else:
            raise ValueError("error #1")
        self.__target = x0 - self.__left_point[0]
        self.__len = 0
        x, y = self.__left_point
        while 0 <= x < self.__w and 0 <= y < self.__h:
            x += self.__step[0]
            y += self.__step[1]
            self.__len += 1

    def __len__(self) -> int:
        return self.__len

    def list(self) -> (List[chr],):
        x, y = self.__left_point

        outcome = list()
        for i in range(len(self)):
            outcome.append(self.__matrix[y][x])
            x += self.__step[0]
            y += self.__step[1]
        return outcome

    def apply(self, changes: List[chr]):
        if len(changes) != len(self):
            raise ValueError("error #2")

        x, y = self.__left_point
        for i in range(len(self)):
            self.__matrix[y][x] = changes[i]
            x += self.__step[0]
            y += self.__step[1]

    def target(self) -> int:
        return self.__target

    def __str__(self):
        return "p: {}".format(self.__left_point)

    def __getitem__(self, item):
        if isinstance(item, slice):
            new = copy.copy(self)
            start, end, step = item.start, item.stop, item.step
            new.__target += start
            x, y = self.__left_point
            new.__left_point = (x + self.__step[0] * start, y + self.__step[1] * start)
            new.__len -= start
            return new
        elif isinstance(item, int):
            return
        else:
            raise Exception("error #3")


def gen(proportions: Tuple[int, int],
        words: Set[str],
        index: Dict[Tuple[chr, int], Set[str]],
        language: List[chr]) -> (List[List[chr]], List[str]):
    w, h = proportions
    matrix = [[None for _ in range(w)] for _ in range(h)]
    # generate random letters
    empties: List[Tuple[int, int]] = [(x, y) for x in range(w) for y in range(h)]
    lang_len = len(language)
    attempts = int(w * h / 2)
    for _ in range(attempts):
        i = random.randrange(0, len(empties))
        letter = language[random.randrange(0, lang_len)]
        x, y = empties[i]
        del empties[i]
        matrix[y][x] = letter

    # shake empties
    random.shuffle(empties)

    word_max_len = 0
    word_min_len = 0
    init = False
    for word in language:
        word_len = len(word)
        if not init:
            word_max_len = word_len
            word_min_len = word_len
            init = True
        if word_len > word_max_len:
            word_max_len = word_len
        if word_len < word_min_len:
            word_min_len = word_len

    directions = [Direction.HORIZ, Direction.VERT, Direction.MAIN_DIAG, Direction.SECOND_DIAG]
    order = [Order.Direct, Order.Indirect]
    inserted: List[str] = list()
    breaking = False
    # choose empty
    for [x, y] in empties:
        if matrix[y][x] is not None:
            continue
        random.shuffle(directions)
        # choose direction
        for direction in directions:
            line = Line(matrix, (x, y), direction)
            # choose interval
            intervals: List[Tuple[int, int]] = list()
            for start in range(line.target() + 1):
                for end in range(line.target(), len(line)):
                    length = end - start
                    if word_min_len <= length <= word_max_len:
                        intervals.append((start, end + 1))
            random.shuffle(intervals)
            for [i, j] in intervals:
                random.shuffle(order)
                piece = line[i:j]
                # choose direct or indirect order
                for o in order:
                    l = piece.list()
                    if o == Order.Indirect:
                        l.reverse()
                    proposals = words_by_pattern(words, index, l)
                    if len(proposals) > 0:
                        word = random.choice(proposals)
                        inserted.append(word)

                        word_list = list(word)
                        if o == Order.Indirect:
                            word_list.reverse()
                        piece.apply(word_list)
                        breaking = True
                        break
                if breaking:
                    break
            if breaking:
                break
        if breaking:
            breaking = False
            continue
        # fill it by random letter because
        # there is no word that can be placed
        letter = language[random.randrange(0, lang_len)]
        matrix[y][x] = letter

    return matrix, inserted


def play(words: Set[str], matrix: List[List[chr]], mask: List[List[chr]], word: str) -> bool:
    if word not in words:
        return False
    w, h = len(matrix[0]), len(matrix)
    dirs = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]
    matched: List[Tuple[int, int, int, int]] = list()
    for y0 in range(h):
        for x0 in range(w):
            if matrix[y0][x0] == word[0]:
                for [dx, dy] in dirs:
                    x, y = x0, y0
                    match = True
                    for letter in word:
                        if 0 <= x < w and 0 <= y < h and letter == matrix[y][x]:
                            x += dx
                            y += dy
                        else:
                            match = False
                            break
                    if match:
                        matched.append((x0, y0, dx, dy))
    for [x, y, dx, dy] in matched:
        for letter in word:
            mask[y][x] = letter.capitalize()
            x += dx
            y += dy
    if len(matched) > 0:
        return True
    return False


def pretty_matrix(matrix: List[List[chr]], mask: List[List[chr]]):
    new = copy.deepcopy(matrix)
    w, h = len(matrix[0]), len(matrix)
    for y in range(h):
        for x in range(w):
            if mask[y][x] is not None:
                new[y][x] = '^' + mask[y][x]  # '\033[1m' + mask[y][x] + '\033[0m'
    print(pandas.DataFrame(
        numpy.array(new),
        [y for y in range(len(matrix))],
        [x for x in range(len(matrix[0]))]
    ))


words: Set[str] = set()
index: Dict[Tuple[chr, int], Set[str]] = dict()
language: Set[chr] = set()
for word in open("secondary_dict.txt"):
    word = word.rstrip().lower()
    words.add(word)
    for position, letter in enumerate(word):
        language.add(letter)
        unit = (letter, position)
        if unit not in index:
            index[unit] = set()
        index[unit].add(word)

# for [unit, words] in index.items():
#    print(unit, words)

m, ins = gen((10, 8), words, index, list(language))
mask = [[None for _ in range(10)] for _ in range(8)]
pretty_matrix(m, mask)
# l = Line(m, (8, 5), Direction.SECOND_DIAG)
# print(l, len(l), l.list()[1:3], l.target())
# print(ins)
# l.apply(['a', 'b', 'c', 'd'])
# pretty_matrix(m)
print("Enter word, w for words, e to exit:")
while True:
    word = input()
    if word == "e":
        break
    if word == "w":
        print(ins)
    print(play(words, m, mask, word))
    pretty_matrix(m, mask)

print(gen.__name__)
print(dir(gen))
print(gen.__code__)
print(dir(gen.__code__))
print(gen.__code__.co_varnames)
print(gen.__code__.co_argcount)
