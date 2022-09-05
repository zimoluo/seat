import json
from src.constants import *
from src.seat import Seats
from typing import Union
import time
import random
import math

class Parser:

    @staticmethod
    def rules(rules: list[dict]) -> tuple:
        raw = []
        for rule in rules:
            ref = {ROW: None, COL: None}
            for i in (ROW, COL):
                ref[i] = Parser.interval(rule[i])
            for row in ref[ROW]:
                for col in ref[COL]:
                    if rule[MODE] == ADD:
                        raw.append((row, col))
                    elif rule[MODE] == DEL:
                        while (row, col) in raw:
                            raw.remove((row, col))
                    else:
                        raise ValueError('Illegal mode.')
        return tuple(set(raw))
    
    @staticmethod
    def rotate(config: dict) -> tuple:
        week = time.time() // (86400 * 7)
        i = int(week % len(config[NAMES]))

        if i < len(config[NAMES]) - 1:
            return tuple(config[NAMES][i: i + 2])
        else:
            return (config[NAMES][-1], config[NAMES][0])

    @staticmethod
    def interval(given: Union[int, tuple, list]) -> Union[tuple, range]:
        if type(given) is int:
            return (given, )
        elif type(given) in (list, tuple):
            if not len(given) in (2, 3):
                raise ValueError('Illegal interval list.')
            return range(*tuple(given))
        else:
            raise TypeError('Illegal interval type.')

    @staticmethod
    def pref(pref: dict, rowMax: int, colMax: int) -> tuple:
        if type(pref) is not dict:
            raise TypeError('Illegal pref.')
        
        mode = pref[MODE]
        if not mode in (SIMPLE, SELECT):
            raise ValueError('Illegal mode.')
        if mode == SELECT:
            pref = random.choice(pref[CHOICE])
        rowB, colB = Parser.boundParser(pref[ROW], rowMax), Parser.boundParser(pref[COL], colMax)
        
        return rowB, colB

    @staticmethod
    def boundParser(raw: dict, maxB: int) -> tuple:
        mode = raw[MODE]

        if mode == ANY:
            return 0, maxB
        
        elif mode == RANGE:
            value = tuple(raw[VALUE])
            if value[0] > value[1]:
                value = value[1], value[0]
            if value[0] < 0 or value[1] > maxB:
                raise ValueError('Out of bound!')
            return value
        
        elif mode == SCALE:
            value = tuple(raw[VALUE])
            if value[0] > value[1]:
                value = value[1], value[0]
            if value[0] < 0 or value[1] > 1:
                raise ValueError('Out of bound!')
            lower = math.floor(maxB * value[0]) if value[0] >= 0.5 else math.ceil(maxB * value[0])
            upper = math.floor(maxB * value[1]) if value[1] >= 0.5 else math.ceil(maxB * value[1])
            lower, upper = min(lower, maxB - 1), max(1, upper)
            while lower >= upper:
                upper = lower + 1
            return lower, upper
        
        else:
            raise ValueError('Illegal mode.')

class Config:
    def __init__(self, config: dict):
        self._config = config

        self._noSit = config[NOSIT]
        self._noSit = self._noSitGen()

        self._row = config[ROW]
        self._col = config[COL]
        self._seed = None if config[SEED] == 0 else config[SEED]
        self._nameList = config[NAMELIST]
        self._modif = config[MODIF]

        for _ in range(MAX_TRIAL):
            try:
                self._getSeatObject()
            except IndexError:
                random.seed(self._seed)
                self._seed = random.random()
            else:
                break
        else:
            raise ValueError('Incomplete run. Try increasing maximum trial number or changing a seed.')
    
    def _noSitGen(self):
        mode = self._noSit[MODE]
        if mode == SIMPLE:
            out = []
            for each in self._noSit[CONFIG][VALUE]:
                out.append(tuple(each))
            return tuple(set(out))
        elif mode == RULES:
            return Parser.rules(self._noSit[CONFIG][RULES])
        elif mode == EMPTY:
            return tuple()
        else:
            raise ValueError('Illegal mode.')
    
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

            if mode == MATE:
                if PREF in each:
                    pref = Parser.pref(each[PREF], self._row, self._col)
                else:
                    pref = None, None
                self.seats.setMate(each[NAME], each[MATE], *pref)
            elif mode == PREF:
                pref = Parser.pref(each[PREF], self._row, self._col)
                self.seats.setPref(each[NAME], *pref)
            elif mode == ROTATE: 
                self.seats.setMate(*Parser.rotate(each))