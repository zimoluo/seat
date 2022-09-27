from src.constants import *
from src.seat import NoSolutionError, Seats
from typing import Union
import time
import random
import math

# A parser for reading formatted config files.
class Parser:

    # A pos-array reader.
    @staticmethod
    def posArrayProvider(data: dict, rowMax: int, colMax: int) -> tuple:
        mode = data[MODE]
        if mode == RULES:
            return Parser.rules(data[RULES], rowMax, colMax)
        elif mode == SIMPLE:
            out = []
            for each in data[VALUE]:
                out.append(tuple(each))
            return tuple(set(out))
        elif mode == EMPTY:
            return tuple()
        else:
            raise ValueError('Illegal mode.')
    
    allPreset = {MODE: RULES, RULES: [{MODE: ADD, COL: {MODE: ALL}, ROW: {MODE: ALL}}]}

    @staticmethod
    def rules(rules: list[dict], rowMax: int, colMax: int) -> tuple:
        raw = []
        for rule in rules:
            mode = rule[MODE]
            if mode == INVERT:
                total = []
                for rowI in range(rowMax):
                    for colI in range(colMax):
                        total.append((rowI, colI))
                for toDel in raw:
                    while toDel in total:
                        total.remove(toDel)
                raw = total
                continue

            col = Parser.evalPos(rule[COL], colMax)
            row = Parser.evalPos(rule[ROW], rowMax)
            finalPos = []
            for eachRow in row:
                for eachCol in col:
                    finalPos.append((eachRow, eachCol))
            
            if mode == ADD:
                for each in finalPos:
                    raw.append(each)
            elif mode == DEL:
                for each in finalPos:
                    while each in raw:
                        raw.remove(each)
            else:
                raise ValueError('Illegal mode.')
        return tuple(set(raw))
    
    @staticmethod
    def evalPos(pos: dict, maxVal: int) -> tuple:
        mode = pos[MODE]
        if mode == ALL:
            return tuple(range(maxVal))
        elif mode == DIRECT:
            if type(pos[VALUE]) is int:
                return (pos[VALUE],)
            elif type(pos[VALUE]) is list:
                return tuple(pos[VALUE])
        elif mode == RANGE:
            return tuple(range(*tuple(pos[VALUE])))
        elif mode == SCALE:
            val = tuple(pos[VALUE])
            if val[0] > val[1]:
                val = val[1], val[0]
            if val[0] < 0 or val[1] > 1:
                raise ValueError('Out of bound!')
            lower = math.floor(maxVal * val[0]) if val[0] >= 0.5 else math.ceil(maxVal * val[0])
            upper = math.floor(maxVal * val[1]) if val[1] >= 0.5 else math.ceil(maxVal * val[1])
            while lower >= upper:
                upper = lower + 1
            return tuple(range(lower, upper))
        else:
            raise ValueError('Illegal mode.')
    
    @staticmethod
    def rotate(config: dict) -> tuple:
        week = time.time() // (86400 * 7)
        i = int(week % len(config[NAMES]))

        if i < len(config[NAMES]) - 1:
            return tuple(config[NAMES][i: i + 2])
        else:
            return (config[NAMES][-1], config[NAMES][0])

class Config:
    def __init__(self, config: dict):
        self._config = config
        self._row = config[ROW]
        self._col = config[COL]
        self._noSit = Parser.posArrayProvider(config[NOSIT], self._row, self._col)
        self._seed = None if config[SEED] == 0 else config[SEED]
        self._nameList = config[NAMELIST]
        self._modif = config[MODIF]

        for _ in range(MAX_TRIAL):
            try:
                self._getSeatObject()
            except NoSolutionError:
                random.seed(self._seed)
                self._seed = random.random()
            else:
                break
        else:
            raise ValueError('Incomplete run. Try increasing maximum trial number or changing a seed.')
    
    def _getSeatObject(self):
        self.seats = Seats(self._row, self._col, self._nameList, self._noSit, self._seed)
        self._setModif()
    
    def _setModif(self):
        modif = self._modif

        for each in modif:
            mode = each[MODE]
            if mode == FIXED:
                self.seats.setFixed(each[NAME], tuple(each[POS]))

        for each in modif:
            mode = each[MODE]

            if mode == PREF:
                if PREF in each:
                    pref = Parser.posArrayProvider(each[PREF], self._row, self._col)
                else:
                    pref = Parser.posArrayProvider(Parser.allPreset, self._row, self._col)
                
                if MATE in each:
                    self.seats.setMate(each[NAME], each[MATE], pref)
                else:
                    self.seats.setPref(each[NAME], pref)
            elif mode == ROTATE:
                self.seats.setMate(*Parser.rotate(each), Parser.posArrayProvider(Parser.allPreset, self._row, self._col))