import library.gen as gen
import library.get_excel as excel
import library.utility as util

# Main function.
def main(times=1):
    file_name = util.get_json_data('./library/seat_initialization.json')['file_name']
    for _ in range(times):
        excel.get_form(gen.gen(file_name), file_name)

def safe_exec():
    try:
        main()
    except MemoryError:
        safe_exec()