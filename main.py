import library.gen as gen
from library.openpyxl import load_workbook
import library.utility as util
import time
import sys
import os

# Generate excel form. Currently only suitable for C5.
def get_c5_excel_form(seats):
    # Alphabet used for sheet index
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Formatted date.
    date = [time.strftime('%d', time.localtime()).strip(), time.strftime('%b', time.localtime()).strip(), time.strftime('%Y', time.localtime()).strip()]

    # Load the sheet from workbook.
    wb = load_workbook('./library/seat_template.xlsx')
    sheet = wb.active

    # Fill the form.
    for row_seat in range(len(seats.seats)):
        row_form = row_seat + 4
        for col_seat in range(len(seats.seats[0]) - 1, -1, -1):
            col_form = alphabet[len(seats.seats[0]) - col_seat]
            coord_form = col_form + str(row_form)

            student = seats.seats[row_seat][col_seat]
            
            if student == 'NA' or 'EMPTY':
                continue

            sheet[coord_form] = student
    
    # Fill the header with date.
    header = sheet['K1'].value

    header = util.replace_str_word(header, 'DAY', date[0])
    header = util.replace_str_word(header, 'MONTH', date[1])
    header = util.replace_str_word(header, 'YEAR', date[2])
    
    sheet['K1'] = header

    # Save the document.
    wb.save('ICC S1C5 Seat.xlsx')

# Restart the entire program. Used to prevent dead loop.
def restart_program():
    print('Restarting')
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Main function.
def main(times=1):
    for _ in range(times):
        get_c5_excel_form(gen.gen('ICC S1C5 Seat'))

# Run the main function with the exception of errors.
if __name__ == '__main__':
    try:
        main()
    except MemoryError:
        restart_program()