import library.gen as gen
import sys
import os
import library.get_excel as excel

# Restart the entire program. Used to prevent dead loop.
def restart_program():
    print('Restarting')
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Main function.
def main(times=1):
    for _ in range(times):
        excel.get_form(gen.gen('ICC S1C5 Seat'))

# Run the main function with the exception of errors.
if __name__ == '__main__':
    try:
        main()
    except MemoryError:
        restart_program()