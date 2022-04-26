import library.gen as gen
from library.openpyxl import load_workbook
import library.utility as util
import time

def get_c5_excel_form(seats):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    date = [time.strftime('%d', time.localtime()).strip(), time.strftime('%b', time.localtime()).strip(), time.strftime('%Y', time.localtime()).strip()]

    wb = load_workbook('./library/seat_template.xlsx')
    sheet = wb.active

    for row_seat in range(len(seats.seats)):
        row_form = row_seat + 4
        for col_seat in range(len(seats.seats[0]) - 1, -1, -1):
            col_form = alphabet[len(seats.seats[0]) - col_seat]
            coord_form = col_form + str(row_form)

            student = seats.seats[row_seat][col_seat]
            
            if student == 'NA':
                continue

            sheet[coord_form] = student
    
    header = sheet['K1'].value

    header = util.replace_str_word(header, 'DAY', date[0])
    header = util.replace_str_word(header, 'MONTH', date[1])
    header = util.replace_str_word(header, 'YEAR', date[2])
    
    sheet['K1'] = header

    wb.save('ICC S1C5 Seat.xlsx')

if __name__ == '__main__':
    get_c5_excel_form(gen.gen('ICC S1C5 Seat'))