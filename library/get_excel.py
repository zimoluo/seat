'''

Now we have custom excel form support.
You still have to make a suitable template, though.
Use %ROW% to mark starting row, and %COL% to mark starting col.
Use DAY MONTH, YEAR to mark the date. It currently supports only one format as shown below.

'''


from library.openpyxl import load_workbook
import time
import library.utility as util

def find_special_pos(sheet):
    start = {}

    for row in sheet.rows:
        for cell in row:
            if cell.value is None:
                continue
            
            if '$' in cell.value:
                if r'%ROW%' in cell.value:
                    start['row'] = cell.row

                if r'%COL%' in cell.value:
                    start['col'] = cell.column

                cell.value = None

            if 'DAY MONTH, YEAR' == cell.value:
                start['date'] = (cell.row, cell.column)
                

    
    if len(start) != 3:
        raise ValueError('Template inappropriate.')

    return start

# Need to provide a 
def get_form(seats):
    # Formatted date.
    date = [time.strftime('%d', time.localtime()).strip(), time.strftime('%b', time.localtime()).strip(), time.strftime('%Y', time.localtime()).strip()]

    # Load the sheet from workbook.
    wb = load_workbook('./library/seat_template.xlsx')
    sheet = wb.active

    # Find start.
    start = find_special_pos(sheet)

    # Fill the form.
    for row_seat in range(len(seats.seats)):
        row_form = row_seat + start['row']
        for col_seat in range(len(seats.seats[0]) - 1, -1, -1):
            col_form = len(seats.seats[0]) - 1 - col_seat + start['col']

            student = seats.seats[row_seat][col_seat]
            
            if student in ('NA', 'EMPTY'):
                continue

            sheet.cell(row=row_form, column=col_form).value = student
    
    # Fill the dateline with date.
    dateline = sheet.cell(row=start['date'][0], column=start['date'][1]).value

    dateline = util.replace_str_word(dateline, 'DAY', date[0])
    dateline = util.replace_str_word(dateline, 'MONTH', date[1])
    dateline = util.replace_str_word(dateline, 'YEAR', date[2])
    
    sheet.cell(row=start['date'][0], column=start['date'][1]).value = dateline

    # Save the document.
    wb.save('ICC S1C5 Seat.xlsx')