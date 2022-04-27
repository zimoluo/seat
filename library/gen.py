from multiprocessing.sharedctypes import Value
from library.seat import Seats
import library.utility as util
import json
import random

# Evaluate the generator.
def eval_generator(config):
    # Create an empty forbidden list.
    forbidden = []
    # Get the rules used for config.
    rules = config['rules']
    
    # Process each rule in the rules.
    for rule in rules:
        # Initialize the forbidden list every time; remove the redundant elements as well as convert all positions into tuples.
        forbidden = list(set(util.get_tupled_list(forbidden)))
        # Add mode.
        if rule['mode'] == 'add':
            for each in rule['content']:
                forbidden.append(each)
        # Iter mode.
        elif rule['mode'] == 'iter':
            # Get the raw ones.
            row_raw = rule['content']['row']
            col_raw = rule['content']['col']

            raw_list = [row_raw, col_raw]
            rule_list = [None, None]

            # Process the iteration file.
            for i in range(2):
                # Range mode.
                if raw_list[i]['mode'] == 'range':
                    try:
                        rule_list[i] = range(raw_list[i]['content']['lower_bound'], raw_list[i]['content']['upper_bound'], raw_list[i]['content']['step'])
                    except KeyError:
                        rule_list[i] = range(raw_list[i]['content']['lower_bound'], raw_list[i]['content']['upper_bound'])
                # Given mode.
                elif raw_list[i]['mode'] == 'given':
                    rule_list[i] = tuple(raw_list[i]['content'])
                # Otherwise raise an error.
                else:
                    raise ValueError('Illegal mode.')
            
            # After the initialization is complete, append the corresponding rows and cols.
            for row in rule_list[0]:
                for col in rule_list[1]:
                    forbidden.append((row, col))

        # Remove mode.
        elif rule['mode'] == 'remove':
            for each in rule['content']:
                each = tuple(each)
                while each in forbidden:
                    forbidden.remove(each)

        # If there's an unexpected mode, just raise an error.
        else:
            raise ValueError('Illegal mode.')
    
    # Finalize the list before returning.
    forbidden = tuple(set(util.get_tupled_list(forbidden)))

    return forbidden

# Get seat data for initialization.
def get_init_data():
    seat_data = util.get_json_data('./library/seat_initialization.json')
    name_list = seat_data['name_list']
    max_row = seat_data['row']
    max_col = seat_data['col']

    # Processing the forbidden list, which makes it support the older version of the forbidden list (some changes still have to be done).
    if seat_data['forbidden']['mode'] == 'given':
        forbidden = util.get_tupled_list(seat_data['forbidden']['config'])
    
    elif seat_data['forbidden']['mode'] == 'generator':
        forbidden = eval_generator(seat_data['forbidden']['config'])

    else:
        raise ValueError('Illegal mode for forbidden list.')
    
    return (max_row, max_col, name_list, forbidden)

def set_modif_return_override(seats):
    # Load the seat arrangement data.
    seat_data = util.get_json_data('./library/seat_modification.json')
    fixed_seat = seat_data['fixed']
    seat_mate = seat_data['mate']
    seat_with_pref = seat_data['pref']
    override = seat_data['override']

    # Manipulate the seats through methods written.
    # seats.set_fixed_seat('NAME', row, col)
    for cell in fixed_seat:
        seats.set_fixed_seat(cell['name'], cell['row'], cell['col'])

    # seats.set_seat_with_pref('NAME', PREFERENCE)
    for cell in seat_with_pref:
        seats.set_seat_with_pref(cell['name'], util.get_tupled_list(cell['pref']))

    # seats.set_seat_mate('NAME1', 'NAME2)
    for cell in seat_mate:
        try:
            seats.set_seat_mate(cell['name_1'], cell['name_2'], util.get_tupled_list(cell['pref']))
        except KeyError:
            seats.set_seat_mate(cell['name_1'], cell['name_2'])

    # Special seating.
    special_seating_data = get_special_seating('./library/special_seating.json')
    for entry in special_seating_data:
        members_this_week = util.get_pair_by_week(entry['name_list'])
        seats.set_seat_mate(members_this_week[0], members_this_week[1])

    return override

# Get special seating data.
def get_special_seating(path):
    # Grab the data.
    data = util.get_json_data(path)
    # Shuffling the unshuffled lists.
    for i in range(len(data)):
        try:
            if not(data[i]['is_shuffled']):
                random.shuffle(data[i]['name_list'])
                data[i]['is_shuffled'] = True
        except KeyError:
            random.shuffle(data[i]['name_list'])
            data[i]['is_shuffled'] = True
    
    # Write the file back.
    with open(path, encoding='utf-8', mode='w') as data_json:
        new_json = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
        data_json.truncate()
        data_json.write(new_json)
    
    # Then return the data.
    return data

# The main function.
def gen(written_file_name):
    # Get initialization data.
    init_data = get_init_data()

    # Initialization
    seats = Seats(init_data[0], init_data[1], init_data[2], init_data[3])

    override = set_modif_return_override(seats)

    # Print the string.
    print(seats.generate_string(override))
    seats.get_written_file(written_file_name, override)

    return seats