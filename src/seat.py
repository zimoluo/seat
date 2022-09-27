import random
import numpy as np
from src.constants import *
from typing import Union

# An error reported for not finding a solution.
# Whenever a NoSolutionError is encountered, the seed is changed and the program is retried.
class NoSolutionError(Exception): ...

# A class for utility purpose. Staticmethod only.
class Util:

    # A staticmethod for replacing a word in a string with another word.
    @staticmethod
    def lineWordReplace(line: str, word: str, replace: str) -> str:
        for i in range(len(line) - len(word) + 1):
            if line[i: i + len(word)] == word:
                crit = i
                break
    
        before = line[0: crit]
        after = line[crit + len(word):]

        return before + replace + after

# A single seat in a pattern. Contains the sitter's name and a boolean tag for whether the sitter can be swapped.
class SingleSeat:
    def __init__(self, sitter: str, canSwap: bool=True):
        # Sitter must be a string, and canSwap must be a boolean value.
        if not (type(sitter), type(canSwap)) == (str, bool):
            raise ValueError('Invalid input.')

        self._sitter = sitter
        self._canSwap = canSwap
    
    @property
    def canSwap(self):
        return self._canSwap
    
    @canSwap.setter
    def canSwap(self, val: bool) -> None:
        if type(val) is bool:
            self._canSwap = val
            return
        raise ValueError('Invalid input.')
    
    @property
    def sitter(self):
        return self._sitter
    
    def sit(self, name: str) -> None:
        if type(name) is str:
            self._sitter = name
            return
        raise ValueError('Invalid name.')
    
    # Swap another SingleSeat instance with this one.
    def swap(self, other) -> None:
        if type(other) is SingleSeat:
            self._sitter, other._sitter = other._sitter, self._sitter
            return
        raise ValueError('Invalid swap.')
    
    def __str__(self):
        return self._sitter
    
    def __len__(self):
        return len(self._sitter)

# The main class for a seating pattern.
class Seats:
    # Contains the number of rows and columns, a list of names, a list of coordinates not for sitting, and the seed to generate.
    def __init__(self, rows: int, cols: int, nameList: list, noSit: tuple, seed: Union[int, float, None]=None):
        random.seed(seed)
        self._seed = seed
        self._seat = np.empty((rows, cols), dtype=SingleSeat)
        self._noSit = noSit
        self._row = rows
        self._col = cols
        
        # The number of names bust be no greater than the number of available seats.
        if len(nameList) > rows * cols - len(noSit):
            raise IndexError('Too many sitters!')
        # No sit list cannot exceed the rows and cols limit.
        for each in noSit:
            if not(each[0] in range(rows)) or not(each[1] in range(cols)):
                raise IndexError('No sit list out of range!')
        # When the number of available seats is greater than the number of names, fill the rest with 'empty.'
        while len(nameList) < rows * cols - len(noSit):
            nameList.append(EMPTY)
        
        random.shuffle(nameList)

        # Fill the seat list with SingleSeat. Unavailable positions are marked with canSwap = False.
        i = 0
        for row in range(rows):
            for col in range(cols):
                if not (row, col) in noSit:
                    self._seat[row, col] = SingleSeat(nameList[i])
                    i += 1
                else:
                    self._seat[row, col] = SingleSeat(EMPTY, False)

    # The seed is read-only. 
    @property
    def seed(self):
        return self._seed
    
    # Find the corresponding position for a name by indexing through the list.
    def _getNamePos(self, name: str) -> tuple:
        for row in range(self._row):
            for col in range(self._col):
                if self._seat[row, col].sitter == name:
                    return (row, col)
        raise ValueError(f'Cannot find corresponding pos for {name}')

    # To determine whether a position has an available pair next to it.
    def _hasPair(self, *pos: tuple) -> bool:
        row, col = pos
        if col == len(self._seat[0]) - 1:
            return False
        
        if not ((row, col) in self._noSit or (row, col + 1) in self._noSit):
            return True
        
        return False
    
    # To deterpine whether a pair is swappable.
    def _hasPairSwappable(self, pos: tuple) -> bool:
        row, col = pos
        if not self._hasPair(row, col):
            return False
        return self._seat[row, col].canSwap and self._seat[row, col + 1].canSwap

    # Get a random pair for swapping.
    def _getRandomSwap(self, pref: Union[tuple[tuple], list[tuple]], pair: bool=False) -> tuple:
        # First try several times randomly selecting a few possible choices.
        for _ in range(len(pref)):
            pos = random.choice(pref)
            if pair:
                if self._hasPairSwappable(pos):
                    return pos, (pos[0], pos[1] + 1)
            else:
                if self._seat[pos].canSwap:
                    return pos

        # If that doesn't work then find all possible choices and randomly pick one. If there's no choice then raise an error.
        cand = []
        for eachPos in pref:
            if pair:
                if self._hasPairSwappable(eachPos):
                    cand.append((eachPos, (eachPos[0], eachPos[1] + 1)))
            else:
                if self._seat[eachPos].canSwap:
                    cand.append(eachPos)
        if not cand:
            raise NoSolutionError('No solution.')
        
        return random.choice(cand)

    # With given preference list assign a sit for this name.
    def setPref(self, name: str, pref: Union[tuple[tuple], list[tuple]]) -> None:
        myRow, myCol = self._getNamePos(name)
        row, col = self._getRandomSwap(pref)
        self._seat[row, col].swap(self._seat[myRow, myCol])
        self._seat[row, col].canSwap = False
    
    # Set a fixed seat.
    def setFixed(self, name: str, *pos: tuple) -> None:
        myPos = self._getNamePos(name)
        if not self._seat[pos].canSwap:
            raise IndexError('Cannot swap to this seat.')
        self._seat[pos].swap(self._seat[myPos])
        self._seat[pos].canSwap = False
    
    # Assign a mate for a name.
    def setMate(self, name: str, mate: str, pref: Union[tuple[tuple], list[tuple]]) -> None:
        newPair = list(self._getRandomSwap(pref, pair=True))
        
        myNew = newPair.pop(random.randint(0, 1))
        self._seat[myNew].swap(self._seat[self._getNamePos(name)])
        self._seat[myNew].canSwap = False

        self._seat[newPair[0]].swap(self._seat[self._getNamePos(mate)])
        self._seat[newPair[0]].canSwap = False
    
    # Generate the string version of the finalized seat.
    def __str__(self):
        lines = ''
        fullSpc = '　'
        maxLen = 0
        placeHdr = '&'

        for row in self._seat:
            for each in row:
                if len(each) > maxLen:
                    maxLen = len(each)
        
        for row in range(len(self._seat)):
            line = ''
            for col in range(len(self._seat[0]) - 1, -1, -1):
                name = self._seat[row, col].sitter
                if name == EMPTY:
                    name = placeHdr * maxLen
                else:
                    name = name + max(0, (maxLen - len(name))) * placeHdr

                line = line + fullSpc + name
            line = line.strip(fullSpc)

            while placeHdr in line:
                line = Util.lineWordReplace(line, placeHdr, fullSpc)
            lines = lines + line + ('\n' if row != len(self._seat) - 1 else '')
        return lines
    
    def __len__(self) -> int:
        return len(self._seat)
    
    def __getitem__(self, key: Union[int, tuple]) -> Union[np.ndarray, SingleSeat]:
        return self._seat[key]