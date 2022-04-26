from library.seat import Seats
import library.utility as util
import json
import random


# Get special seating data.
def get_special_seating(path):
    data = util.get_json_data(path)
    for i in range(len(data)):
        try:
            if not(data[i]['is_shuffled']):
                random.shuffle(data[i]['name_list'])
                data[i]['is_shuffled'] = True
        except KeyError:
            random.shuffle(data[i]['name_list'])
            data[i]['is_shuffled'] = True
    
    with open(path, encoding='utf8', mode='w') as data_json:
        new_json = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
        data_json.truncate()
        data_json.write(new_json)
    
    return data

# The main function.
def gen(written_file_name):
    # Get seat data for initialization.
    seat_data = util.get_json_data('./library/seat_initialization.json')
    name_list = seat_data['name_list']
    forbidden = util.get_tupled_list(seat_data['forbidden'])
    max_row = seat_data['row']
    max_col = seat_data['col']

    # Initialization
    seats = Seats(max_row, max_col, name_list, forbidden)

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


    # Print the string.
    print(seats.generate_string(override))
    seats.get_written_file(written_file_name, override)

    return seats