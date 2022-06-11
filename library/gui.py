'''

GUI support.

'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import library.exec as exec
from library.openpyxl import load_workbook
import os
import json
import library.utility as util

class GUI:
    # Initialization. Must give a initialized GUI, i.e. init_gui = tk.Tk()
    def __init__(self, init_gui):
        self.gui = self.set_gui(init_gui)

        self.input_label = tk.Label(self.gui, text="Your input", font=('Calibri', 20))
        self.input_label.place(x=15, y=10)

        self.json_info_label = tk.Label(self.gui, text="JSON config file", font=('Calibri', 20))
        self.json_info_label.place(x=500, y=10)

        self.browser_label = tk.Label(self.gui, text="Data Select", font=('Calibri', 20))
        self.browser_label.place(x=500, y=500)

        self.info_text = tk.Text(self.gui, width=62, height=25, state='disabled', font=('Courier New', 10))
        self.info_text.place(x=500, y=80)

        self.current_info = tk.StringVar(value='init')

        self.info_radio_init = tk.Radiobutton(self.gui, text='Seat Initialization', font=('Calibri', 15), variable=self.current_info, value='init', command=self.info_button)
        self.info_radio_init.place(x=540, y=580, anchor=tk.W)

        self.info_radio_modif = tk.Radiobutton(self.gui, text='Seat Modification',  font=('Calibri', 15), variable=self.current_info, value='modif', command=self.info_button)
        self.info_radio_modif.place(x=540, y=630, anchor=tk.W)

        self.info_radio_special = tk.Radiobutton(self.gui, text='Special Seating', font=('Calibri', 15), variable=self.current_info, value='special', command=self.info_button)
        self.info_radio_special.place(x=540, y=680, anchor=tk.W)

        self.special = Special(self)

        self.run_button = tk.Button(self.gui, text='Get Seat!', width=45, height=1, font=('Calibri', 15), command=exec.safe_exec)
        self.run_button.place(x=15, y=680)

        self.file_button_form = tk.Button(self.gui, text='Upload your template', width=45, height=1, font=('Calibri', 15), command=self.pick_form)
        self.file_button_form.place(x=15, y=500)

        self.file_button_confirm = tk.Button(self.gui, text='Confirm', width=15, height=1, font=('Calibri', 15), command=self.confirm_form_upload)
        self.file_button_confirm.place_forget()

        self.file_button_discard = tk.Button(self.gui, text='Discard', width=15, height=1, font=('Calibri', 15), command=self.discard_form_upload)
        self.file_button_discard.place_forget()

        self.file_entry_form = tk.Entry(self.gui, textvariable='', width=45, font=('Courier New', 13), state='disabled')
        self.file_entry_form.place(x=15, y=570)

        self.entry_label = tk.Label(self.gui, text='Entry: ', font=('Calibri', 15))

        # Initialize the info area.
        self.info_button()

    def pick_form(self):
        my_path = filedialog.askopenfilename(title='Select your seat template file', filetypes=[('Excel file', ['*.xlsx', '*.xlsm', '*.xltx', '*.xltm'])], initialdir=os.getcwd())
        if my_path:
            self.file_entry_form['state'] = 'normal'
            self.file_entry_form.delete(0, tk.END)
            self.file_entry_form.insert(0, my_path)
            self.file_button_confirm.place(x=15, y=610)
            self.file_button_discard.place(x=200, y=610)
    
    def confirm_form_upload(self):
        self.form_file = load_workbook(self.file_entry_form.get())
        self.form_file.save(f'./library/seat_template.xlsx')
        self.file_entry_form.delete(0, tk.END)
        self.file_entry_form.insert(0, 'Upload successful.')
        self.file_entry_form['state'] = 'disabled'
        self.file_button_confirm.place_forget()
        self.file_button_discard.place_forget()
        self.form_file = None

    def discard_form_upload(self):
        self.file_entry_form.delete(0, tk.END)
        self.file_entry_form['state'] = 'disabled'
        self.file_button_confirm.place_forget()
        self.file_button_discard.place_forget()
        self.form_file = None
    
    def write_file_info(self, path, text):
        with open(path, encoding='utf-8', mode='w') as file:
            file.truncate()
            file.write(text)

    def set_gui(self, gui):
        gui.title('Seat Arranging Tool by Zimo Luo')
        gui.geometry('1024x768+400+100')
        gui.resizable(0, 0)
    
    def refresh_info(self, content=''):
        self.info_text['state'] = 'normal'
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, content)
        self.info_text['state'] = 'disabled'
            
    def info_button(self):
        for entry in [self.special]:
            if self.current_info.get == entry.symbol:
                entry.show()
                entry.refresh()
            else:
                entry.hide()

class SeatingConfig:
    def __init__(self, belong):
        self.tree = ttk.Treeview(belong.gui, selectmode='browse')

        self.info = util.get_file_info('./library/special_seating.json')
        self.data = json.loads(self.info)
        self.parent = belong

        self.btn_add = tk.Button(belong.gui, text='Add another', width=15, height=1, font=('Calibri', 15), command=lambda: self.add(layer='major'))
        self.btn_del = tk.Button(belong.gui, text='Delete this', width=15, height=1, font=('Calibri', 15), command=lambda: self.delete(layer='major'))
    
    def hide(self):
        for widget in self.all_widget:
            widget.place_forget()
    
    def show(self):
        self.major_entry_label.place(x=25, y=80)
        self.major_btn_back.place(x=120, y=80)
        self.major_btn_next.place(x=300, y=80)
        self.major_btn_add.place(x=50, y=160)
        self.major_btn_del.place(x=280, y=160)

    def refresh(self):
        self.parent.refresh_info(self.info)

    def delete(self, layer='major'):
        pass
    
    def add(self, layer='major'):
        pass
    
    def save(self, path=''):
        self.info = json.dumps(self.data, sort_keys=True, indent=4, ensure_ascii=False)
        with open(path, encoding='utf-8', mode='w') as data_json:
            data_json.truncate()
            data_json.write(self.info)
    
    def surf(self, mode='next', layer='major'):
        pass

class SeatingConfig:
    def __init__(self, belong):
        self.index = {'major': 0}
        self.info = ''
        self.data = ''
        self.symbol = ''
        self.parent = belong

        self.major_entry_label = tk.Label(belong.gui, text=f"Entry: {self.index['major']}", font=('Calibri', 15))

        self.major_btn_back = tk.Button(belong.gui, text='Back', width=15, height=1, font=('Calibri', 15), command=lambda: self.surf('back'))
        self.major_btn_next = tk.Button(belong.gui, text='Next', width=15, height=1, font=('Calibri', 15), command=lambda: self.surf('next'))

        self.major_btn_add = tk.Button(belong.gui, text='Add', width=15, height=1, font=('Calibri', 15), command=lambda: self.add(layer='major'))
        self.major_btn_del = tk.Button(belong.gui, text='Delete', width=15, height=1, font=('Calibri', 15), command=lambda: self.delete(layer='major'))

        self.all_widget = [self.major_entry_label, self.major_btn_add, self.major_btn_back, self.major_btn_del, self.major_btn_next]
    
    def hide(self):
        for widget in self.all_widget:
            widget.place_forget()
    
    def show(self):
        self.major_entry_label.place(x=25, y=80)
        self.major_btn_back.place(x=120, y=80)
        self.major_btn_next.place(x=300, y=80)
        self.major_btn_add.place(x=50, y=160)
        self.major_btn_del.place(x=280, y=160)

    def refresh(self):
        self.parent.refresh_info(self.info)

    def delete(self, layer='major'):
        pass
    
    def add(self, layer='major'):
        pass
    
    def save(self, path=''):
        self.info = json.dumps(self.data, sort_keys=True, indent=4, ensure_ascii=False)
        with open(path, encoding='utf-8', mode='w') as data_json:
            data_json.truncate()
            data_json.write(self.info)
    
    def surf(self, mode='next', layer='major'):
        pass


class Special(SeatingConfig):
    def __init__(self, belong):
        super().__init__(belong)

        self.info = util.get_file_info('./library/special_seating.json')
        self.data = json.loads(self.info)
        self.index['l1'] = 0
        self.symbol = 'special'

        self.l1_entry = tk.Entry(belong.gui, width=10, font=('Microsoft Yahei', 20), state='normal', textvariable={self.data[self.index['major']]['name_list'][self.index['l1']]})
        self.l1_btn_save = tk.Button(belong.gui, text='Save', width=15, height=1, font=('Calibri', 15), command=lambda: self.save_refresh(mode='entry'))
        self.l1_btn_del = tk.Button(belong.gui, text='Delete', width=15, height=1, font=('Calibri', 15), command=lambda: self.delete(layer='l1'))
        self.l1_btn_add = tk.Button(belong.gui, text='Add', width=15, height=1, font=('Calibri', 15), command=lambda: self.add(layer='l1'))
        self.l1_btn_next = tk.Button(belong.gui, text='Next', width=15, height=1, font=('Calibri', 15), command=lambda: self.surf(layer='l1'))
        self.l1_btn_back = tk.Button(belong.gui, text='Back', width=15, height=1, font=('Calibri', 15), command=lambda: self.surf(layer='l1', mode='back'))

        self.all_widget = self.all_widget + [self.l1_btn_del, self.l1_btn_save, self.l1_entry, self.l1_btn_add, self.l1_btn_next, self.l1_btn_back]

    def show(self):
        super().show()
        self.l1_entry.place(x=50, y=240)
        self.l1_btn_save.place(x=50, y=320)
        self.l1_btn_add.place(x=50, y=400)
        self.l1_btn_back.place(x=280, y=320)
        self.l1_btn_next.place(x=280, y=240)
        self.l1_btn_del.place(x=280, y=400)

    def save(self, mode='normal'):
        if mode == 'normal':
            pass
        elif mode == 'entry':
            self.data[self.index['major']]['name_list'][self.index['l1']] = self.l1_entry.get()
        
        super().save(path='./library/special_seating.json')
    
    def save_refresh(self, mode='normal'):
        self.save(mode=mode)
        self.refresh()

    def refresh(self):
        self.l1_entry.delete(0, tk.END)
        self.l1_entry.insert(0, self.data[self.index['major']]['name_list'][self.index['l1']])
        super().refresh()

    def delete(self, layer='major'):
        if layer == 'major':
            self.index['l1'] = 0
            del self.data[self.index['major']]
        elif layer == 'l1':
            del self.data[self.index['major']]['name_list'][self.index['l1']]
        
        self.save_refresh()

    def add(self, layer='major'):
        if layer == 'major':
            self.index['l1'] = 0
            self.data.insert(self.index['major'], {'name_list': [''], 'is_shuffled': False})
        if layer == 'l1':
            self.data[self.index['major']]['name_list'].insert(self.index['l1'], '')

        self.save_refresh()
    
    def surf(self, mode='next', layer='major'):
        self.l1_entry.delete(0, tk.END)
        if mode == 'next':
            if layer == 'major':
                self.index['major'] = min(self.index['major'] + 1, len(self.data) - 1)
                self.major_entry_label['text'] = f'Entry: {self.index[layer]}'
                self.index['l1'] = 0
            elif layer == 'l1':
                self.index['l1'] = min(self.index['l1'] + 1, len(self.data[self.index['major']]['name_list']) - 1)

        elif mode == 'back':
            if layer == 'major':
                self.index['major'] = max(self.index['major'] - 1, 0)
                self.major_entry_label['text'] = f'Entry: {self.index[layer]}'
                self.index['l1'] = 0
            elif layer == 'l1':
                self.index['l1'] = max(self.index['l1'] - 1, 0)
        
        self.l1_entry.insert(0, self.data[self.index['major']]['name_list'][self.index['l1']])

class Modif(SeatingConfig):
    def __init__(self, belong):
        super().__init__(belong)

        self.info = util.get_file_info('./library/seat_modification.json')
        self.data = json.loads(self.info)
        self.index['major'] = 'fixed'
        self.index['sub'] = 0
        self.symbol = 'modif'

        self.generic_entry_name = tk.Entry(belong.gui, width=10, font=('Microsoft Yahei', 20), state='normal', textvariable={self.data[self.index['major']][0]['name']})
        self.generic_entry_col = tk.Entry(belong.gui, width=10, font=('Microsoft Yahei', 20), state='normal', textvariable={self.data[self.index['major']][0]['col']})
        self.generic_entry_row = tk.Entry(belong.gui, width=10, font=('Microsoft Yahei', 20), state='normal', textvariable={self.data[self.index['major']][0]['row']})
        self.mate_entry_name_1 = tk.Entry(belong.gui, width=10, font=('Microsoft Yahei', 20), state='normal', textvariable={self.data[self.index['major']][0]['name']})
        self.mate_entry_name_2 = tk.Entry(belong.gui, width=10, font=('Microsoft Yahei', 20), state='normal', textvariable={self.data[self.index['major']][0]['name']})
        self.generic_entry_pref = tk.Entry(belong.gui, width=10, font=('Microsoft Yahei', 20), state='normal', textvariable={self.data[self.index['major']][0]['name']})
        self.generic_btn_save = tk.Button(belong.gui, text='Save', width=15, height=1, font=('Calibri', 15), command=lambda: self.save_refresh(mode='entry'))
        self.pref_entry = tk.Entry(belong.gui, width=10, font=('Microsoft Yahei', 20), state='normal')

        self.all_widget = self.all_widget + [self.generic_btn_save, self.generic_entry_col, self.generic_entry_name, self.generic_entry_pref, self.generic_entry_row, self.mate_entry_name_1, self.mate_entry_name_2]

    def show(self):
        super().show()
        self.l1_entry.place(x=50, y=240)
        self.l1_btn_save.place(x=50, y=320)
        self.l1_btn_add.place(x=50, y=400)
        self.l1_btn_back.place(x=280, y=320)
        self.l1_btn_next.place(x=280, y=240)
        self.l1_btn_del.place(x=280, y=400)

    def save(self, mode='normal'):
        if mode == 'normal':
            pass
        elif mode == 'entry':
            self.data[self.index['major']]['name_list'][self.index['l1']] = self.l1_entry.get()
        
        super().save(path='./library/special_seating.json')
    
    def save_refresh(self, mode='normal'):
        self.save(mode=mode)
        self.refresh()

    def refresh(self):
        self.l1_entry.delete(0, tk.END)
        self.l1_entry.insert(0, self.data[self.index['major']]['name_list'][self.index['l1']])
        super().refresh()

    def delete(self, layer='major'):
        if layer == 'major':
            self.index['l1'] = 0
            del self.data[self.index['major']]
        elif layer == 'l1':
            del self.data[self.index['major']]['name_list'][self.index['l1']]
        
        self.save_refresh()

    def add(self, layer='major'):
        if layer == 'major':
            self.index['l1'] = 0
            self.data.insert(self.index['major'], {'name_list': [''], 'is_shuffled': False})
        if layer == 'l1':
            self.data[self.index['major']]['name_list'].insert(self.index['l1'], '')

        self.save_refresh()
    
    def surf(self, mode='next', layer='major'):
        self.l1_entry.delete(0, tk.END)
        if mode == 'next':
            if layer == 'major':
                self.index['major'] = min(self.index['major'] + 1, len(self.data) - 1)
                self.major_entry_label['text'] = f'Entry: {self.index[layer]}'
                self.index['l1'] = 0
            elif layer == 'l1':
                self.index['l1'] = min(self.index['l1'] + 1, len(self.data[self.index['major']]['name_list']) - 1)

        elif mode == 'back':
            if layer == 'major':
                self.index['major'] = max(self.index['major'] - 1, 0)
                self.major_entry_label['text'] = f'Entry: {self.index[layer]}'
                self.index['l1'] = 0
            elif layer == 'l1':
                self.index['l1'] = max(self.index['l1'] - 1, 0)
        
        self.l1_entry.insert(0, self.data[self.index['major']]['name_list'][self.index['l1']])