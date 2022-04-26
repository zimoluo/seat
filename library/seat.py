'''

This program is designed for bug fix for earlier versions.
On top of that, the basic algorithm is completely changed.
The program allows the user to set fixed seat as well as to bind seatmate.

'''


import random
import math
import library.utility as util
import copy


# Student class is a subclass of str(String) class.
# The only difference is that Student class has an attribute of 'can_swap', which controls whether a student can swap seat.
# Only used internally.
class Student(str):
    def __init__(self, name):
        self.can_swap = True

# The main class.
class Seats:

    # Initialization
    def __init__(self, rows, cols, name_list, forbidden_seats):
        seats = []

        # Initializing the list
        # VS Code needs a spell check for annotations. Nah.
        # Arrange shuffled student list into the two-dimensional list.

        # Check if there exists any error.
        if len(name_list) > rows * cols - len(forbidden_seats):
            raise IndexError('Too many students!')
        for forbidden in forbidden_seats:
            if not(forbidden[0] in range(rows)) or not(forbidden[1] in range(cols)):
                raise IndexError('Forbidden list out of range!')

        while len(name_list) < rows * cols - len(forbidden_seats):
            name_list.append('EMPTY')
        random.shuffle(name_list)

        for row in range(rows):
            seats.append([])
        for row in range(rows):
            for col in range(cols):
                seats[row].append(0)

        name_list_index = 0
        for row in range(rows):
            for col in range(cols):
                if not((row, col) in forbidden_seats):
                    seats[row][col] = Student(name_list[name_list_index])
                    name_list_index += 1
                else:
                    seats[row][col] = Student('NA')
                    seats[row][col].can_swap = False
                    
        
        # Setting properties
        # self.seats is the two-dimensional list for seats.
        # self.forbidden is the forbidden list.
        # self.max_name_length is used for generating a proper string.
        self.seats = seats
        self.forbidden = forbidden_seats

        max_name_length = 0
        for name in name_list:
            if not(name in ('EMPTY', 'NA')) and len(name) > max_name_length:
                max_name_length = len(name)
        self.max_name_length = max_name_length
    
    # These two magic methods might be useful, but mostly dedicated for preventing syntax errors.
    def __getitem__(self, key):
        return self.seats[key]
    
    def __setitem__(self, key, value):
        self.seats[key] = value
    
    # When a str form of the Seats class is called, return the generated seat string.
    def __str__(self):
        return self.generate_string()
    
    # Return the position of a given name. The name can be str or Student class.  
    # In fact, all methods that require a name input allows normal str class as well as Student class, for that all have codes for converting them into standarized Student class.
    # Student class is a subclass of str, though.
    def get_name_pos(self, name):
        for index in range(len(self.seats)):
            if name in self.seats[index]:
                col = self.seats[index].index(name)
                row = index
                return (row, col)
        raise ValueError('Cannot find correspondng name pos.')
    
    # Used to be get_mate_status, which is currently abandoned. get_pair_pos better serves its initial purpose.
    # Used for getting the position of a pair with given name. A boolean is also returned to indicate whether the process is successful.
    def get_pair_pos(self, name):
        # Get the position of the given name.
        pos = self.get_name_pos(name)

        row = pos[0]
        col = pos[1]
        
        # Seeks to find the mate of the given name.
        # If the name is in a forbidden list(though not being possible normally), return a False plus a None.
        if (row, col) in self.forbidden:
            return (False,)

        # Consider the case at the two sides of the classroom
        elif col == 0 and not((row, col + 1) in self.forbidden):
            return (True, (row, col), (row, col + 1))
        
        elif col == len(self.seats[0]) - 1 and not((row, col - 1) in self.forbidden):
            return (True, (row, col), (row, col - 1))
        
        # As for seats in the middle, use a score system to count both seats on the left and the right.
        elif col in range(1, len(self.seats[0])):
            scores = [0, 0, 0]
            if not((row, col + 1) in self.forbidden):
                scores[0] = 1
                scores[2] += 1
            if not((row, col - 1) in self.forbidden):
                scores[1] = 1
                scores[2] += 1
            
            # Evaluate the scores. If the total score is 2, then the seats on the left or the right are both available. Return a random pair of two.
            if scores[2] == 2:
                return (True, (row, col), (row, col + (1 if random.randint(0, 1) == 0 else -1)))
            
            # Otherwise return the corresponding available seat.
            elif scores[0] == 1:
                return (True, (row, col), (row, col + 1))
            
            elif scores[1] == 1:
                return (True, (row, col), (row, col - 1))

            # If none is applicable, return a False and a None.
            else:
                return (False,)
        
        # Otherwise return a False and a None.
        else:
            return (False,)

    # Generate a completely random pair in which both seats are not listed in the forbidden list, i.e. the list of pathways and wall corner.
    def get_random_pair(self, row_bound, col_bound):
        # Get a random row and a random column index that is in legal range.
        new_row = random.randint(row_bound[0], row_bound[1] - 1)
        new_col = random.randint(col_bound[0], col_bound[1] - 1)

        pair_pos = self.get_pair_pos(self.seats[new_row][new_col])

        # Use while sentence to force the program to find a pair whose both members are not in the forbidden list.
        while not(pair_pos[0]):
            new_row = random.randint(row_bound[0], row_bound[1] - 1)
            new_col = random.randint(col_bound[0], col_bound[1] - 1)

            pair_pos = self.get_pair_pos(self.seats[new_row][new_col])
        
        # Return the positions of the pair, disregarding the boolean value.
        return pair_pos[1:]

    # Returns a random swappable position.
    def get_random_swappable_pos(self, row_bound, col_bound):
        new_row = random.randint(row_bound[0], row_bound[1] - 1)
        new_col = random.randint(col_bound[0], col_bound[1] - 1)
        pos = (new_row, new_col)
        
        # Requires the position both not in forbidden list and is swappable.
        while not(not(pos in self.forbidden) and self.seats[pos[0]][pos[1]].can_swap):
            new_row = random.randint(row_bound[0], row_bound[1] - 1)
            new_col = random.randint(col_bound[0], col_bound[1] - 1)
            pos = (new_row, new_col)
        
        return pos

    # Returns a pair of seats in which both members are capable of swapping; in other words, both members have attribute can_swap = True.
    def get_swappable_pair(self, row_bound, col_bound):
        # Get a random pair from the previous method.
        pair_pos = self.get_random_pair(row_bound, col_bound)
        pair_pos_0 = pair_pos[0]
        pair_pos_1 = pair_pos[1]


        # Again implement while command to get a pair in which both members are swappable (can_swap is True).
        while not(not(pair_pos_0 in self.forbidden) and not(pair_pos_1 in self.forbidden) and self.seats[pair_pos_0[0]][pair_pos_0[1]].can_swap \
        and self.seats[pair_pos_1[0]][pair_pos_1[1]].can_swap):
            pair_pos = self.get_random_pair(row_bound, col_bound)
            pair_pos_0 = pair_pos[0]
            pair_pos_1 = pair_pos[1]
            
        return (pair_pos_0, pair_pos_1)

    # Swaps two position without modifying anything.
    # The current swap method is identical to its first generation. It was later renamed to swap_no_limit, before renaming back to its initial identity.
    # The current algorithm for swap method is reasonable.
    def swap(self, para_1, para_2):
        pos = [None, None]
        for i in range(2):
            para = (para_1, para_2)[i]
            if type(para) in (str, Student):
                pos[i] = self.get_name_pos(para)
            elif type(para) in (tuple, list):
                pos[i] = tuple(para)
            else:
                raise ValueError('Illegal data type.')
        
        pos_1 = pos[0]
        pos_2 = pos[1]

        self.seats[pos_1[0]][pos_1[1]], self.seats[pos_2[0]][pos_2[1]] = self.seats[pos_2[0]][pos_2[1]], self.seats[pos_1[0]][pos_1[1]]
    
    # Set seat mate. Preference is optional.
    # Used to be set_seat_mate_with_pref. Now merged into one single method.
    def set_seat_mate(self, name_1, name_2, pref=None):
        name_2_pos = self.get_name_pos(name_2)
        self.seats[name_2_pos[0]][name_2_pos[1]].can_swap = False

        if pref is None:
            pref = ((0, len(self.seats)), (0, len(self.seats[0])))

        bound = self.eval_pref(pref)
        pair_pos = list(self.get_swappable_pair(bound[0], bound[1]))
        
        name_1_new_pos = pair_pos.pop(random.randint(0, 1))
        self.swap(name_1, name_1_new_pos)
        temp_pos = pair_pos[0]

        self.seats[name_2_pos[0]][name_2_pos[1]].can_swap = True
        
        self.swap(temp_pos, name_2_pos)

        pair_pos = (self.get_name_pos(name_1), self.get_name_pos(name_2))
        self.seats[pair_pos[0][0]][pair_pos[0][1]].can_swap = False
        self.seats[pair_pos[1][0]][pair_pos[1][1]].can_swap = False

    # Set a student to be on a fixed seat.
    # Must be conducted before any set pair is specified.
    def set_fixed_seat(self, name, row, col):
        self.swap(name, (row, col))
        self.seats[row][col].can_swap = False
    
    # Decide whether a given input is a piece of code or straightforwardly bound tuples.
    def eval_pref(self, pref):
        if type(pref) in (tuple, list):
            bound = tuple(pref)
        
        elif type(pref) is dict:
            bound = ((pref['row_lower'], pref['row_upper']), (pref['col_lower'], pref['col_upper']))
            
        elif type(pref) is str:
            bound = self.find_seating_pref_bound(pref)

        else:
            raise ValueError('Illegal pref type.')

        return bound

    # Set seat based on preference.
    def set_seat_with_pref(self, name, pref):
        # Get the bound
        bound = self.eval_pref(pref)
        
        # Get a swappable position.
        swap = self.get_random_swappable_pos(bound[0], bound[1])

        # Swap the two seats.
        self.swap(name, swap)
        
        # Set the can_swap to False.
        new_pos = self.get_name_pos(name)
        self.seats[new_pos[0]][new_pos[1]].can_swap = False

    # The bound system allows you to set a bound for the random seat generator.
    # It allows candidates to choose seat within a certain range.
    # This method provides a simpler solution for setting up a bound by accepting a given code.
    def find_seating_pref_bound(self, pref):
        pref_list = pref.split()
        size = pref_list[-1]
        need = pref_list[:-1]
        # Remove redundant elements (if any).
        need = tuple(set(need))
        row_total = len(self.seats)
        col_total = len(self.seats[0])

        # Initial bound. [0, max_length)
        row_bound = [0, row_total]
        col_bound = [0, col_total]

        # Check if there are exclusive cases.
        error_cases = (('RIGHT', 'LEFT', 'MIDDLE_COL'), ('BACK', 'FRONT', 'MIDDLE_ROW'))
        for case in error_cases:
            score = 0
            for key in need:
                if key in case:
                    score += 1
            if score >= 2:
                return (row_bound, col_bound)
        
        # Modifying the bound according to the code given.
        if 'RIGHT' in need:
            if size == 'CLOSE':
                col_bound[1] = max(1, int(math.floor((col_total) / 3)))
            elif size == 'VERY_CLOSE':
                col_bound[1] = max(1, int(math.floor((col_total) / 7)))
        
        if 'LEFT' in need:
            if size == 'CLOSE':
                col_bound[0] = min(col_total, int(math.ceil((col_total) * 2 / 3)))
            elif size == 'VERY_CLOSE':
                col_bound[0] = min(col_total, int(math.ceil((col_total) * 6 / 7)))

        if 'MIDDLE_COL' in need:
            if size == 'CLOSE':
                col_bound[1] = max(1, int(math.floor((col_total) * 7 / 10)))
                col_bound[0] = min(col_total, int(math.ceil((col_total) * 3 / 10)))
            elif size == 'VERY_CLOSE':
                col_bound[1] = max(1, int(math.ceil((col_total) * 3 / 5)))
                col_bound[0] = min(col_total, int(math.floor((col_total) * 2 / 5)))
        
        if 'FRONT' in need:
            if size == 'CLOSE':
                row_bound[1] = max(1, int(math.ceil((row_total) / 3)))
            if size == 'VERY_CLOSE':
                row_bound[1] = max(1, int(math.floor((row_total) / 5)))
        
        if 'BACK' in need:
            if size == 'CLOSE':
                row_bound[0] = min(row_total, int(math.floor((row_total) * 2 / 3)))
            if size == 'VERY_CLOSE':
                row_bound[0] = min(row_total, int(math.floor((row_total) * 4 / 5)))

        if 'MIDDLE_ROW' in need:
            if size == 'CLOSE':
                row_bound[1] = min(row_total, int(math.floor((row_total) * 4 / 5)))
                row_bound[0] = min(row_total, int(math.ceil((row_total) / 5)))
            if size == 'VERY_CLOSE':
                row_bound[1] = min(row_total, int(math.ceil((row_total) * 2 / 3)))
                row_bound[0] = min(row_total, int(math.floor((row_total) / 3)))
        
        return (tuple(row_bound), tuple(col_bound))

    # Generate a string for printing and compiling into txt file.
    def generate_string(self, override=[]):
        # Initialization. Full space has a size same as that of a Chinese character.
        layers = ''
        full_space = '　'
        seat_prep = copy.deepcopy(self.seats)
        for each in override:
            seat_prep[each['row']][each['col']] = each['name']

        # Arrange the two-dimensional list into a string.
        for row in range(len(seat_prep)):
            layer = ''
            for col in range(len(seat_prep[0]) - 1, -1, -1):
                # We make any modification on a copied 'student' variable instead of the seats list itself.
                student = seat_prep[row][col]
                # If it is otherwise NA or EMPTY, convert it into spaces.
                if student in ('NA', 'EMPTY'):
                    student = '&' * self.max_name_length
                # Else, modify the name to make it consistent in size.
                else:
                    student = student + max(0, (self.max_name_length - len(student))) * '&'
                
                # Plug them in a string.
                layer = layer + full_space + student

            # Press 'Enter.'
            # Also to strip those spaces at both ends.
            layer = layer.strip(full_space)

            while '&' in layer:
                layer = util.replace_str_word(layer, '&', full_space)
            
            layers = layers + layer + ('\n' if row != len(seat_prep) - 1 else '')

        return layers

    def get_written_file(self, result_name, enable_ysl=True):
        get_string = self.generate_string(enable_ysl)
        with open(f'{result_name}.txt', 'w', encoding='utf-8') as seat:
            seat.truncate()
            seat.write(get_string)