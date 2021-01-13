# pyinstaller --onedir --icon=MapData/EagleIcon.ico SS_GUI.py
# Made by Tyler McCamley 2019

import sys
import tkinter.ttk as ttk
import tkinter as tk
import MapQuery
import ReportScraper
import platform
import shutil
import AddressQuery
import pyperclip
import configparser
from Tooltips import CreateToolTip
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image


version_number = str(1.14)

# Grab Config file and read settings

config = configparser.RawConfigParser()
config.read(r'MapData\SS_CONFIG.properties')


def vp_start_gui():
    # Starting point when module is the main routine.
    global val, w, root
    root = tk.Tk()
    top = SearchWindow(root)
    init(root, top)
    root.mainloop()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


py3 = True
w = None

lot_num, house_num, unit_num, road_name, road_type, suburb, postcode = '', '', '', '', '', '', ''
response_list = []


def destroy_search_window():
    global w
    w.destroy()
    w = None


def create_option_window():

    def save_folder_search():
        folder_selected = filedialog.askdirectory()
        browse_button.configure()
        map_dir_entry.delete(0, tk.END)
        map_dir_entry.insert(0, folder_selected)

    def update_config():
        print('Updating config file.')
        config.set('OPTIONS', 'MAP_SAVE_DIRECTORY', str(map_dir_entry.get()))
        config.set('OPTIONS', 'map_save_prompt', str(w.map_save_prompt_var.get()))
        with open(r'MapData\SS_CONFIG.properties', 'w') as configfile:
            config.write(configfile)

    option_window = tk.Toplevel(root)
    option_window.wm_transient(root)
    option_window.geometry("367x220+533+327")
    option_window.title('Site Search Options')
    option_window.configure(background="#d9d9d9")
    option_window.configure(highlightbackground="#d9d9d9")
    option_window.configure(highlightcolor="black")
    option_window.iconbitmap(r'MapData/EagleIcon.ico')

    map_dir_label = tk.Label(option_window)
    map_dir_label.place(relx=0.082, rely=0.136, height=21, width=96)
    map_dir_label.configure(activebackground="#f9f9f9")
    map_dir_label.configure(activeforeground="black")
    map_dir_label.configure(background="#d9d9d9")
    map_dir_label.configure(disabledforeground="#a3a3a3")
    map_dir_label.configure(foreground="#000000")
    map_dir_label.configure(highlightbackground="#d9d9d9")
    map_dir_label.configure(highlightcolor="black")
    map_dir_label.configure(text='''Save Map Folder:''')

    map_dir_entry = tk.Entry(option_window)
    map_dir_entry.place(relx=0.381, rely=0.136,height=20, relwidth=0.311)
    map_dir_entry.configure(background="white")
    map_dir_entry.configure(disabledforeground="#a3a3a3")
    map_dir_entry.configure(font="TkTextFont")
    map_dir_entry.configure(foreground="#000000")
    map_dir_entry.configure(insertbackground="black")
    map_dir_entry.insert(0, config.get('OPTIONS', 'MAP_SAVE_DIRECTORY'))

    browse_button = tk.Button(option_window)
    browse_button.place(relx=0.736, rely=0.126, height=24, width=67)
    browse_button.configure(activebackground="#ececec")
    browse_button.configure(activeforeground="#000000")
    browse_button.configure(background="#d9d9d9")
    browse_button.configure(disabledforeground="#a3a3a3")
    browse_button.configure(foreground="#000000")
    browse_button.configure(highlightbackground="#d9d9d9")
    browse_button.configure(highlightcolor="black")
    browse_button.configure(pady="0")
    browse_button.configure(text='''Browse''')
    browse_button.configure(command=save_folder_search)

    map_save_prompt_chk = tk.Checkbutton(option_window)
    map_save_prompt_chk.place(relx=0.082, rely=0.286, height=21, width=157)
    map_save_prompt_chk.configure(activebackground="#ececec")
    map_save_prompt_chk.configure(activeforeground="#000000")
    map_save_prompt_chk.configure(background="#d9d9d9")
    map_save_prompt_chk.configure(disabledforeground="#a3a3a3")
    map_save_prompt_chk.configure(foreground="#000000")
    map_save_prompt_chk.configure(highlightbackground="#d9d9d9")
    map_save_prompt_chk.configure(highlightcolor="black")
    map_save_prompt_chk.configure(justify='left')
    map_save_prompt_chk.configure(text='''Show Save Map Prompt?''')
    map_save_prompt_chk.configure(variable=w.map_save_prompt_var)

    save_config_button = tk.Button(option_window)
    save_config_button.place(relx=0.456, rely=0.818, height=24, width=87)
    save_config_button.configure(activebackground="#ececec")
    save_config_button.configure(activeforeground="#000000")
    save_config_button.configure(background="#d9d9d9")
    save_config_button.configure(disabledforeground="#a3a3a3")
    save_config_button.configure(foreground="#000000")
    save_config_button.configure(highlightbackground="#d9d9d9")
    save_config_button.configure(highlightcolor="black")
    save_config_button.configure(pady="0")
    save_config_button.configure(text='''Save Changes''')
    save_config_button.configure(command=update_config)

    quit_config_button = tk.Button(option_window)
    quit_config_button.place(relx=0.736, rely=0.818, height=24, width=67)
    quit_config_button.configure(activebackground="#ececec")
    quit_config_button.configure(activeforeground="#000000")
    quit_config_button.configure(background="#d9d9d9")
    quit_config_button.configure(disabledforeground="#a3a3a3")
    quit_config_button.configure(foreground="#000000")
    quit_config_button.configure(highlightbackground="#d9d9d9")
    quit_config_button.configure(highlightcolor="black")
    quit_config_button.configure(pady="0")
    quit_config_button.configure(text='''Close''')
    quit_config_button.configure(command=option_window.destroy)

    # This makes it that the option window needs to be closed before doing anything else.
    option_window.grab_set()
    option_window.tk.eval('tk::PlaceWindow {0} widget {1}'.format(option_window, root))


class SearchWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        top.geometry("886x320+500+300")
        top.title("Site Search (" + version_number + ")")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.iconbitmap(r'MapData/EagleIcon.ico')

        # // MENU BAR

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_ana1color, fg=_ana1color)
        top.configure(menu=self.menubar)

        # File Menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0, font="TkMenuFont")
        self.filemenu.add_command(label='Clear Search Fields', command=self.clear_all_input)
        self.filemenu.add_command(label='Options', command=create_option_window)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=top.quit)
        # Info Menu
        self.infomenu = tk.Menu(self.menubar, tearoff=0, font="TkMenuFont")
        self.infomenu.add_command(label='Created By: Tyler McCamley')
        self.infomenu.add_separator()
        self.infomenu.add_command(label='Version: ' + version_number)

        # List of cascade menus to add
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='Info', menu=self.infomenu)

        # // VARIABLES AND CONFIG

        # Variables to assign input values to
        self.right_click_check = tk.IntVar(value=(config.get('OPTIONS', 'disable_right_click')))
        self.map_ref_check = tk.IntVar(value=1)
        self.map_save_prompt_var = tk.IntVar(value=(config.get('OPTIONS', 'map_save_prompt')))
        # Need to add map save directory here also

        self.street_type_options = ['', 'Avenue', 'Boulevard', 'Circle', 'Circuit', 'Close', 'Crescent', 'Court', 'Drive', 'Esplanade', 'Grove',
                                    'Highway', 'Lane', 'Parade', 'Place', 'Ridge', 'Rise', 'Road', 'Street', 'Terrace', 'View', 'Walk', 'Way',
                                    'Wynd']

        # /// ENTER HEADER

        self.search_header = tk.Label(top)
        self.search_header.place(relx=0.023, rely=0.031, height=21, width=192)
        self.search_header.configure(background="#d9d9d9")
        self.search_header.configure(disabledforeground="#a3a3a3")
        self.search_header.configure(foreground="#000000")
        self.search_header.configure(text='''Enter Site Info:''')

        # /// LOT NO.

        self.lot_label = tk.Label(top)
        self.lot_label.place(relx=0.023, rely=0.125, height=21, width=74)
        self.lot_label.configure(activebackground="#f9f9f9")
        self.lot_label.configure(activeforeground="black")
        self.lot_label.configure(background="#d9d9d9")
        self.lot_label.configure(disabledforeground="#a3a3a3")
        self.lot_label.configure(foreground="#000000")
        self.lot_label.configure(highlightbackground="#d9d9d9")
        self.lot_label.configure(highlightcolor="black")
        self.lot_label.configure(text='''Lot No. :''')

        self.lot_entry = tk.Entry(top)
        self.lot_entry.place(relx=0.113, rely=0.125,height=20, relwidth=0.129)
        self.lot_entry.configure(background="white")
        self.lot_entry.configure(disabledforeground="#a3a3a3")
        self.lot_entry.configure(font="TkTextFont")
        self.lot_entry.configure(foreground="#000000")
        self.lot_entry.configure(insertbackground="black")
        self.lot_entry.bind('<Return>', self.search)

        # /// HOUSE NO.

        self.house_label = tk.Label(top)
        self.house_label.place(relx=0.023, rely=0.219, height=21, width=74)
        self.house_label.configure(background="#d9d9d9")
        self.house_label.configure(disabledforeground="#a3a3a3")
        self.house_label.configure(foreground="#000000")
        self.house_label.configure(text='''House No. :''')

        self.house_entry = tk.Entry(top)
        self.house_entry.place(relx=0.113, rely=0.219, height=20, relwidth=0.129)
        self.house_entry.configure(background="white")
        self.house_entry.configure(disabledforeground="#a3a3a3")
        self.house_entry.configure(font="TkTextFont")
        self.house_entry.configure(foreground="#000000")
        self.house_entry.configure(insertbackground="black")
        self.house_entry.bind('<Return>', self.search)

        # /// UNIT NO.

        self.unit_label = tk.Label(top)
        self.unit_label.place(relx=0.023, rely=0.313, height=21, width=74)
        self.unit_label.configure(background="#d9d9d9")
        self.unit_label.configure(disabledforeground="#a3a3a3")
        self.unit_label.configure(foreground="#000000")
        self.unit_label.configure(text='''Unit No. :''')

        self.unit_entry = tk.Entry(top)
        self.unit_entry.place(relx=0.113, rely=0.313,height=20, relwidth=0.129)
        self.unit_entry.configure(background="white")
        self.unit_entry.configure(disabledforeground="#a3a3a3")
        self.unit_entry.configure(font="TkTextFont")
        self.unit_entry.configure(foreground="#000000")
        self.unit_entry.configure(insertbackground="black")
        self.unit_entry.bind('<Return>', self.search)

        # /// STREET NAME

        self.street_name_label = tk.Label(top)
        self.street_name_label.place(relx=0.023, rely=0.406, height=21, width=74)
        self.street_name_label.configure(background="#d9d9d9")
        self.street_name_label.configure(disabledforeground="#a3a3a3")
        self.street_name_label.configure(foreground="#000000")
        self.street_name_label.configure(text='''Street Name :''')

        self.street_name_entry = tk.Entry(top)
        self.street_name_entry.place(relx=0.113, rely=0.406, height=20, relwidth=0.129)
        self.street_name_entry.configure(background="white")
        self.street_name_entry.configure(disabledforeground="#a3a3a3")
        self.street_name_entry.configure(font="TkTextFont")
        self.street_name_entry.configure(foreground="#000000")
        self.street_name_entry.configure(insertbackground="black")
        self.street_name_entry.bind('<Return>', self.search)

        # /// STREET TYPE

        self.street_type_label = tk.Label(top)
        self.street_type_label.place(relx=0.023, rely=0.5, height=21, width=74)
        self.street_type_label.configure(background="#d9d9d9")
        self.street_type_label.configure(disabledforeground="#a3a3a3")
        self.street_type_label.configure(foreground="#000000")
        self.street_type_label.configure(text='''Street Type :''')

        self.street_type_entry = ttk.Combobox(top)
        self.street_type_entry.place(relx=0.113, rely=0.5, relheight=0.066, relwidth=0.128)
        self.street_type_entry.configure(takefocus="")
        self.street_type_entry.set(self.street_type_options[0])
        self.street_type_entry.configure(values=self.street_type_options)
        self.street_type_entry.bind('<Return>', self.search)

        # /// SUBURB

        self.suburb_label = tk.Label(top)
        self.suburb_label.place(relx=0.023, rely=0.594, height=21, width=74)
        self.suburb_label.configure(background="#d9d9d9")
        self.suburb_label.configure(disabledforeground="#a3a3a3")
        self.suburb_label.configure(foreground="#000000")
        self.suburb_label.configure(text='''Suburb :''')

        self.suburb_entry = tk.Entry(top)
        self.suburb_entry.place(relx=0.113, rely=0.594, height=20, relwidth=0.129)
        self.suburb_entry.configure(background="white")
        self.suburb_entry.configure(disabledforeground="#a3a3a3")
        self.suburb_entry.configure(font="TkTextFont")
        self.suburb_entry.configure(foreground="#000000")
        self.suburb_entry.configure(insertbackground="black")
        self.suburb_entry.bind('<Return>', self.search)

        # /// POSTCODE

        self.postcode_label = tk.Label(top)
        self.postcode_label.place(relx=0.023, rely=0.688, height=21, width=74)
        self.postcode_label.configure(background="#d9d9d9")
        self.postcode_label.configure(disabledforeground="#a3a3a3")
        self.postcode_label.configure(foreground="#000000")
        self.postcode_label.configure(text='''Postcode :''')

        self.postcode_entry = tk.Entry(top)
        self.postcode_entry.place(relx=0.113, rely=0.688, height=20, relwidth=0.129)
        self.postcode_entry.configure(background="white")
        self.postcode_entry.configure(disabledforeground="#a3a3a3")
        self.postcode_entry.configure(font="TkTextFont")
        self.postcode_entry.configure(foreground="#000000")
        self.postcode_entry.configure(insertbackground="black")
        self.postcode_entry.bind('<Return>', self.search)

        # /// MAP CHECK

        self.get_map_chk = tk.Checkbutton(top)
        self.get_map_chk.place(relx=0.034, rely=0.813, relheight=0.078, relwidth=0.082)
        self.get_map_chk.configure(activebackground="#ececec")
        self.get_map_chk.configure(activeforeground="#000000")
        self.get_map_chk.configure(background="#d9d9d9")
        self.get_map_chk.configure(disabledforeground="#a3a3a3")
        self.get_map_chk.configure(foreground="#000000")
        self.get_map_chk.configure(highlightbackground="#d9d9d9")
        self.get_map_chk.configure(highlightcolor="black")
        self.get_map_chk.configure(justify='left')
        self.get_map_chk.configure(text='''Map Ref''')
        self.get_map_chk.configure(variable=self.map_ref_check)

        # /// SEARCH BTN

        self.search_button = tk.Button(top)
        self.search_button.place(relx=0.124, rely=0.813, height=24, width=107)
        self.search_button.configure(activebackground="#ececec")
        self.search_button.configure(activeforeground="#000000")
        self.search_button.configure(background="#d9d9d9")
        self.search_button.configure(disabledforeground="#a3a3a3")
        self.search_button.configure(foreground="#000000")
        self.search_button.configure(highlightbackground="#d9d9d9")
        self.search_button.configure(highlightcolor="black")
        self.search_button.configure(pady="0")
        self.search_button.configure(text='''Search''')
        self.search_button.configure(command=self.search)

        # -------------------------------------------------------
        # /// SEARCH RESULTS

        self.search_results_label = tk.Label(top)
        self.search_results_label.place(relx=0.395, rely=0.031, height=21, width=119)
        self.search_results_label.configure(background="#d9d9d9")
        self.search_results_label.configure(disabledforeground="#a3a3a3")
        self.search_results_label.configure(foreground="#000000")
        self.search_results_label.configure(text='''List of Search Results:''')

        self.results_list_box = ScrolledListBox(top)
        self.results_list_box.place(relx=0.26, rely=0.125, relheight=0.766, relwidth=0.43)
        self.results_list_box.configure(background="white")
        self.results_list_box.configure(disabledforeground="#a3a3a3")
        self.results_list_box.configure(font="TkTextFont")
        self.results_list_box.configure(foreground="black")
        self.results_list_box.configure(highlightbackground="#d9d9d9")
        self.results_list_box.configure(highlightcolor="#d9d9d9")
        self.results_list_box.configure(selectbackground="#c4c4c4")
        self.results_list_box.configure(selectforeground="black")
        self.results_list_box.configure(selectmode='SINGLE')
        self.results_list_box.bind("<<ListboxSelect>>", self.on_select)
        self.results_list_box.bind("<Button-3>", self.r_context_menu)

        # -------------------------------------------------------
        # /// INDIVIDUAL INFO

        self.r_site_header_label = tk.Label(top)
        self.r_site_header_label.place(relx=0.779, rely=0.031, height=21, width=103)
        # self.r_site_header_label.place(relx=0.779, rely=0.031, height=21, width=103)
        self.r_site_header_label.configure(background="#d9d9d9")
        self.r_site_header_label.configure(disabledforeground="#a3a3a3")
        self.r_site_header_label.configure(foreground="#000000")
        self.r_site_header_label.configure(text='''Returned Site Info:''')

        # /// ZONE INFO

        self.r_zone_label = tk.Label(top)
        self.r_zone_label.place(relx=0.914, rely=0.031, height=21, width=39)
        self.r_zone_label.configure(background="#d9d9d9")
        self.r_zone_label.configure(disabledforeground="#a3a3a3")
        self.r_zone_label.configure(foreground="#000000")
        self.r_zone_label.configure(text='''Zone X''')

        # /// ZONE TOOLTIP

        self.r_zone_tooltip = CreateToolTip(self.r_zone_label, 'Suburb zone number')

        # /// ADDRESS

        self.r_address_label = tk.Label(top)
        self.r_address_label.place(relx=0.7, rely=0.125, height=21, width=64)
        self.r_address_label.configure(background="#d9d9d9")
        self.r_address_label.configure(disabledforeground="#a3a3a3")
        self.r_address_label.configure(foreground="#000000")
        self.r_address_label.configure(text='''Address :''')

        self.address_textbox = tk.Text(top)
        self.address_textbox.place(relx=0.779, rely=0.125, relheight=0.075, relwidth=0.117)
        self.address_textbox.configure(background="white")
        self.address_textbox.configure(font="TkTextFont")
        self.address_textbox.configure(foreground="black")
        self.address_textbox.configure(highlightbackground="#d9d9d9")
        self.address_textbox.configure(highlightcolor="black")
        self.address_textbox.configure(insertbackground="black")
        self.address_textbox.configure(selectbackground="#c4c4c4")
        self.address_textbox.configure(selectforeground="black")
        self.address_textbox.configure(wrap="word")

        self.copy_address_btn = tk.Button(top)
        self.copy_address_btn.place(relx=0.914, rely=0.125, height=24, width=39)
        self.copy_address_btn.configure(activebackground="#ececec")
        self.copy_address_btn.configure(activeforeground="#000000")
        self.copy_address_btn.configure(background="#d9d9d9")
        self.copy_address_btn.configure(disabledforeground="#a3a3a3")
        self.copy_address_btn.configure(foreground="#000000")
        self.copy_address_btn.configure(highlightbackground="#d9d9d9")
        self.copy_address_btn.configure(highlightcolor="black")
        self.copy_address_btn.configure(pady="0")
        self.copy_address_btn.configure(text='''Copy''')
        self.copy_address_btn.configure(command=lambda: copy_box(self.address_textbox.get("1.0", "999.0")))

        # /// SUBURB

        self.r_suburb_label = tk.Label(top)
        self.r_suburb_label.place(relx=0.7, rely=0.219, height=21, width=60)
        self.r_suburb_label.configure(background="#d9d9d9")
        self.r_suburb_label.configure(disabledforeground="#a3a3a3")
        self.r_suburb_label.configure(foreground="#000000")
        self.r_suburb_label.configure(text='''Suburb :''')

        self.suburb_textbox = tk.Text(top)
        self.suburb_textbox.place(relx=0.779, rely=0.219, relheight=0.075, relwidth=0.117)
        self.suburb_textbox.configure(background="white")
        self.suburb_textbox.configure(font="TkTextFont")
        self.suburb_textbox.configure(foreground="black")
        self.suburb_textbox.configure(highlightbackground="#d9d9d9")
        self.suburb_textbox.configure(highlightcolor="black")
        self.suburb_textbox.configure(insertbackground="black")
        self.suburb_textbox.configure(selectbackground="#c4c4c4")
        self.suburb_textbox.configure(selectforeground="black")
        self.suburb_textbox.configure(wrap="word")

        self.copy_sub_btn = tk.Button(top)
        self.copy_sub_btn.place(relx=0.914, rely=0.219, height=24, width=39)
        self.copy_sub_btn.configure(activebackground="#ececec")
        self.copy_sub_btn.configure(activeforeground="#000000")
        self.copy_sub_btn.configure(background="#d9d9d9")
        self.copy_sub_btn.configure(disabledforeground="#a3a3a3")
        self.copy_sub_btn.configure(foreground="#000000")
        self.copy_sub_btn.configure(highlightbackground="#d9d9d9")
        self.copy_sub_btn.configure(highlightcolor="black")
        self.copy_sub_btn.configure(pady="0")
        self.copy_sub_btn.configure(text='''Copy''')
        self.copy_sub_btn.configure(command=lambda: copy_box(self.suburb_textbox.get("1.0", "999.0")))

        # /// POSTCODE

        self.r_postcode_label = tk.Label(top)
        self.r_postcode_label.place(relx=0.7, rely=0.313, height=21, width=60)
        self.r_postcode_label.configure(activebackground="#f9f9f9")
        self.r_postcode_label.configure(activeforeground="black")
        self.r_postcode_label.configure(background="#d9d9d9")
        self.r_postcode_label.configure(disabledforeground="#a3a3a3")
        self.r_postcode_label.configure(foreground="#000000")
        self.r_postcode_label.configure(highlightbackground="#d9d9d9")
        self.r_postcode_label.configure(highlightcolor="black")
        self.r_postcode_label.configure(text='''Postcode :''')

        self.postcode_textbox = tk.Text(top)
        self.postcode_textbox.place(relx=0.779, rely=0.313, relheight=0.075, relwidth=0.117)
        self.postcode_textbox.configure(background="white")
        self.postcode_textbox.configure(font="TkTextFont")
        self.postcode_textbox.configure(foreground="black")
        self.postcode_textbox.configure(highlightbackground="#d9d9d9")
        self.postcode_textbox.configure(highlightcolor="black")
        self.postcode_textbox.configure(insertbackground="black")
        self.postcode_textbox.configure(selectbackground="#c4c4c4")
        self.postcode_textbox.configure(selectforeground="black")
        self.postcode_textbox.configure(wrap="word")

        self.copy_postcode_btn = tk.Button(top)
        self.copy_postcode_btn.place(relx=0.914, rely=0.313, height=24, width=39)
        self.copy_postcode_btn.configure(activebackground="#ececec")
        self.copy_postcode_btn.configure(activeforeground="#000000")
        self.copy_postcode_btn.configure(background="#d9d9d9")
        self.copy_postcode_btn.configure(disabledforeground="#a3a3a3")
        self.copy_postcode_btn.configure(foreground="#000000")
        self.copy_postcode_btn.configure(highlightbackground="#d9d9d9")
        self.copy_postcode_btn.configure(highlightcolor="black")
        self.copy_postcode_btn.configure(pady="0")
        self.copy_postcode_btn.configure(text='''Copy''')
        self.copy_postcode_btn.configure(command=lambda: copy_box(self.postcode_textbox.get("1.0", "999.0")))

        # /// SITENAME

        self.r_sitename_label = tk.Label(top)
        self.r_sitename_label.place(relx=0.7, rely=0.406, height=21, width=60)
        self.r_sitename_label.configure(activebackground="#f9f9f9")
        self.r_sitename_label.configure(activeforeground="black")
        self.r_sitename_label.configure(background="#d9d9d9")
        self.r_sitename_label.configure(disabledforeground="#a3a3a3")
        self.r_sitename_label.configure(foreground="#000000")
        self.r_sitename_label.configure(highlightbackground="#d9d9d9")
        self.r_sitename_label.configure(highlightcolor="black")
        self.r_sitename_label.configure(text='''Sitename :''')

        self.sitename_textbox = tk.Text(top)
        self.sitename_textbox.place(relx=0.779, rely=0.406, relheight=0.075, relwidth=0.117)
        self.sitename_textbox.configure(background="white")
        self.sitename_textbox.configure(font="TkTextFont")
        self.sitename_textbox.configure(foreground="black")
        self.sitename_textbox.configure(highlightbackground="#d9d9d9")
        self.sitename_textbox.configure(highlightcolor="black")
        self.sitename_textbox.configure(insertbackground="black")
        self.sitename_textbox.configure(selectbackground="#c4c4c4")
        self.sitename_textbox.configure(selectforeground="black")
        self.sitename_textbox.configure(wrap="word")

        self.copy_sitename_btn = tk.Button(top)
        self.copy_sitename_btn.place(relx=0.914, rely=0.406, height=24, width=39)
        self.copy_sitename_btn.configure(activebackground="#ececec")
        self.copy_sitename_btn.configure(activeforeground="#000000")
        self.copy_sitename_btn.configure(background="#d9d9d9")
        self.copy_sitename_btn.configure(disabledforeground="#a3a3a3")
        self.copy_sitename_btn.configure(foreground="#000000")
        self.copy_sitename_btn.configure(highlightbackground="#d9d9d9")
        self.copy_sitename_btn.configure(highlightcolor="black")
        self.copy_sitename_btn.configure(pady="0")
        self.copy_sitename_btn.configure(text='''Copy''')
        self.copy_sitename_btn.configure(command=lambda: copy_box(self.sitename_textbox.get("1.0", "999.0")))

        # /// MAP REF

        self.r_mapref_label = tk.Label(top)
        self.r_mapref_label.place(relx=0.7, rely=0.5, height=21, width=60)
        self.r_mapref_label.configure(activebackground="#f9f9f9")
        self.r_mapref_label.configure(activeforeground="black")
        self.r_mapref_label.configure(background="#d9d9d9")
        self.r_mapref_label.configure(disabledforeground="#a3a3a3")
        self.r_mapref_label.configure(foreground="#000000")
        self.r_mapref_label.configure(highlightbackground="#d9d9d9")
        self.r_mapref_label.configure(highlightcolor="black")
        self.r_mapref_label.configure(text='''Map Ref. :''')

        self.mapref_textbox = tk.Text(top)
        self.mapref_textbox.place(relx=0.779, rely=0.5, relheight=0.075, relwidth=0.117)
        self.mapref_textbox.configure(background="white")
        self.mapref_textbox.configure(font="TkTextFont")
        self.mapref_textbox.configure(foreground="black")
        self.mapref_textbox.configure(highlightbackground="#d9d9d9")
        self.mapref_textbox.configure(highlightcolor="black")
        self.mapref_textbox.configure(insertbackground="black")
        self.mapref_textbox.configure(selectbackground="#c4c4c4")
        self.mapref_textbox.configure(selectforeground="black")
        self.mapref_textbox.configure(wrap="word")

        self.copy_mapref_btn = tk.Button(top)
        self.copy_mapref_btn.place(relx=0.914, rely=0.5, height=24, width=39)
        self.copy_mapref_btn.configure(activebackground="#ececec")
        self.copy_mapref_btn.configure(activeforeground="#000000")
        self.copy_mapref_btn.configure(background="#d9d9d9")
        self.copy_mapref_btn.configure(disabledforeground="#a3a3a3")
        self.copy_mapref_btn.configure(foreground="#000000")
        self.copy_mapref_btn.configure(highlightbackground="#d9d9d9")
        self.copy_mapref_btn.configure(highlightcolor="black")
        self.copy_mapref_btn.configure(pady="0")
        self.copy_mapref_btn.configure(text='''Copy''')
        self.copy_mapref_btn.configure(command=lambda: copy_box(self.mapref_textbox.get("1.0", "999.0")))

        # /// LATITUDE

        self.r_lat_label = tk.Label(top)
        self.r_lat_label.place(relx=0.7, rely=0.594, height=21, width=60)
        self.r_lat_label.configure(activebackground="#f9f9f9")
        self.r_lat_label.configure(activeforeground="black")
        self.r_lat_label.configure(background="#d9d9d9")
        self.r_lat_label.configure(disabledforeground="#a3a3a3")
        self.r_lat_label.configure(foreground="#000000")
        self.r_lat_label.configure(highlightbackground="#d9d9d9")
        self.r_lat_label.configure(highlightcolor="black")
        self.r_lat_label.configure(text='''Latitude :''')

        self.lat_textbox = tk.Text(top)
        self.lat_textbox.place(relx=0.779, rely=0.594, relheight=0.075, relwidth=0.117)
        self.lat_textbox.configure(background="white")
        self.lat_textbox.configure(font="TkTextFont")
        self.lat_textbox.configure(foreground="black")
        self.lat_textbox.configure(highlightbackground="#d9d9d9")
        self.lat_textbox.configure(highlightcolor="black")
        self.lat_textbox.configure(insertbackground="black")
        self.lat_textbox.configure(selectbackground="#c4c4c4")
        self.lat_textbox.configure(selectforeground="black")
        self.lat_textbox.configure(wrap="word")

        self.copy_lat_btn = tk.Button(top)
        self.copy_lat_btn.place(relx=0.914, rely=0.594, height=24, width=39)
        self.copy_lat_btn.configure(activebackground="#ececec")
        self.copy_lat_btn.configure(activeforeground="#000000")
        self.copy_lat_btn.configure(background="#d9d9d9")
        self.copy_lat_btn.configure(disabledforeground="#a3a3a3")
        self.copy_lat_btn.configure(foreground="#000000")
        self.copy_lat_btn.configure(highlightbackground="#d9d9d9")
        self.copy_lat_btn.configure(highlightcolor="black")
        self.copy_lat_btn.configure(pady="0")
        self.copy_lat_btn.configure(text='''Copy''')
        self.copy_lat_btn.configure(command=lambda: copy_box(self.lat_textbox.get("1.0", "999.0")))

        # /// LONGITUDE

        self.r_long_label = tk.Label(top)
        self.r_long_label.place(relx=0.7, rely=0.688, height=21, width=60)
        self.r_long_label.configure(activebackground="#f9f9f9")
        self.r_long_label.configure(activeforeground="black")
        self.r_long_label.configure(background="#d9d9d9")
        self.r_long_label.configure(disabledforeground="#a3a3a3")
        self.r_long_label.configure(foreground="#000000")
        self.r_long_label.configure(highlightbackground="#d9d9d9")
        self.r_long_label.configure(highlightcolor="black")
        self.r_long_label.configure(text='''Longitude :''')

        self.long_textbox = tk.Text(top)
        self.long_textbox.place(relx=0.779, rely=0.688, relheight=0.075, relwidth=0.117)
        self.long_textbox.configure(background="white")
        self.long_textbox.configure(font="TkTextFont")
        self.long_textbox.configure(foreground="black")
        self.long_textbox.configure(highlightbackground="#d9d9d9")
        self.long_textbox.configure(highlightcolor="black")
        self.long_textbox.configure(insertbackground="black")
        self.long_textbox.configure(selectbackground="#c4c4c4")
        self.long_textbox.configure(selectforeground="black")
        self.long_textbox.configure(wrap="word")

        self.copy_long_btn = tk.Button(top)
        self.copy_long_btn.place(relx=0.914, rely=0.688, height=24, width=39)
        self.copy_long_btn.configure(activebackground="#ececec")
        self.copy_long_btn.configure(activeforeground="#000000")
        self.copy_long_btn.configure(background="#d9d9d9")
        self.copy_long_btn.configure(disabledforeground="#a3a3a3")
        self.copy_long_btn.configure(foreground="#000000")
        self.copy_long_btn.configure(highlightbackground="#d9d9d9")
        self.copy_long_btn.configure(highlightcolor="black")
        self.copy_long_btn.configure(pady="0")
        self.copy_long_btn.configure(text='''Copy''')
        self.copy_long_btn.configure(command=lambda: copy_box(self.long_textbox.get("1.0", "999.0")))

        self.download_map_btn = tk.Button(top)
        self.download_map_btn.place(relx=0.7, rely=0.813, height=24, width=113)
        self.download_map_btn.configure(activebackground="#ececec")
        self.download_map_btn.configure(activeforeground="#000000")
        self.download_map_btn.configure(background="#d9d9d9")
        self.download_map_btn.configure(disabledforeground="#a3a3a3")
        self.download_map_btn.configure(foreground="#000000")
        self.download_map_btn.configure(highlightbackground="#d9d9d9")
        self.download_map_btn.configure(highlightcolor="black")
        self.download_map_btn.configure(pady="0")
        self.download_map_btn.configure(text='''Save Map File''')
        self.download_map_btn.configure(command=self.save_map)

        self.get_report_btn = tk.Button(top)
        self.get_report_btn.place(relx=0.831, rely=0.813, height=24, width=113)
        self.get_report_btn.configure(activebackground="#ececec")
        self.get_report_btn.configure(activeforeground="#000000")
        self.get_report_btn.configure(background="#d9d9d9")
        self.get_report_btn.configure(disabledforeground="#a3a3a3")
        self.get_report_btn.configure(foreground="#000000")
        self.get_report_btn.configure(highlightbackground="#d9d9d9")
        self.get_report_btn.configure(highlightcolor="black")
        self.get_report_btn.configure(pady="0")
        self.get_report_btn.configure(text='''Get Property Report''')
        self.get_report_btn.configure(command=self.get_report)

    def search(self, event=None):
        global lot_num, house_num, unit_num, road_name, road_type, suburb, postcode, response_list

        # FORMAT ENTRIES
        lot_num = str(self.lot_entry.get()).upper()
        house_num = str(self.house_entry.get()).upper()
        unit_num = str(self.unit_entry.get()).upper()
        road_name = str(self.street_name_entry.get()).upper()
        road_type = str(self.street_type_entry.get()).upper()
        suburb = str(self.suburb_entry.get()).upper()
        postcode = str(self.postcode_entry.get()).upper()

        # RUN SEARCH
        self.response = AddressQuery.search_to_use(lot_num, unit_num, house_num, road_name, road_type, suburb, postcode)

        if isinstance(self.response, str) is True:
            self.results_list_box.delete(0, tk.END)
            self.results_list_box.insert(tk.END, self.response)

        # SEND RESULTS TO LISTBOX
        if isinstance(self.response, str) is False:

            def format_site_info(line_unit_house, line_street_n, line_street_ty, line_suburb, line_lot):

                abr_type_list = {"ALLEY": "AL", "AMBLE": "AMB", "APPROACH": "APPR", "ARCADE": "ARC", "ARTERIAL": "ART", "AVENUE": "AV", "BAY": "BAY",
                                 "BEND": "BEND", "BRAE": "BRAE", "BREAK": "BRK", "BOULEVARD": "BVD", "BOARDWALK": "BWK", "BOWL": "BWL",
                                 "BYPASS": "BYP", "CIRCLE": "CCL", "CIRCUS": "CCS", "CIRCUIT": "CCT", "CHASE": "CHA", "CLOSE": "CL", "CORNER": "CNR",
                                 "COMMON": "COM", "CONCOURSE": "CON", "CRESCENT": "CR", "CROSS": "CROS", "COURSE": "CRSE", "CREST": "CRST",
                                 "CRUISEWAY": "CRY", "COURT": "CT", "COURTS": "CT", "COURT/S": "CT", "COVE": "CV", "DALE": "DALE", "DELL": "DELL",
                                 "DENE": "DENE", "DIVIDE": "DIV", "DOMAIN": "DOM", "DRIVE": "DR", "EAST": "EAST", "EDGE": "EDG", "ENTRANCE": "ENT",
                                 "ESPLANADE": "ESP", "EXTENSION": "EXTN", "FLATS": "FLTS", "FORD": "FORD", "FREEWAY": "FWY", "GATE": "GATE",
                                 "GARDENS": "GDN", "GARDEN": "GDN", "GARDEN/S": "GDN", "GLADES": "GLA", "GLADE": "GLA", "GLADE/S": "GLA",
                                 "GLEN": "GLN", "GULLY": "GLY", "GRANGE": "GRA", "GREEN": "GRN", "GROVE": "GV", "GATEWAY": "GWY", "HILL": "HILL",
                                 "HOLLOW": "HLW", "HEATH": "HTH", "HEIGHT": "HT", "HEIGHTS": "HTS", "HUB": "HUB", "HIGHWAY": "HWY", "ISLAND": "ID",
                                 "JUNCTION": "JCT", "LANE": "LA", "LINK": "LNK", "LOOP": "LOOP", "LOWER": "LWR", "LANEWAY": "LWY", "MALL": "MALL",
                                 "MEW": "MEW", "MEWS": "MWS", "NOOK": "NOOK", "NORTH": "NTH", "OUTLOOK": "OUT", "PATH": "PATH", "PARADE": "PDE",
                                 "POCKET": "PKT", "PARKWAY": "PKW", "PLACE": "PL", "PLAZA": "PLZ", "PROMENADE": "PRM", "PASS": "PS",
                                 "PASSAGE": "PSG", "POINT": "PT", "PURSUIT": "PUR", "PATHWAY": "PWAY", "QUADRANT": "QD", "QUAY": "QU",
                                 "REACH": "RCH", "ROAD": "RD", "RIDGE": "RDG", "RESERVE": "REST", "REST": "REST", "RETREAT": "RET",
                                 "RIDE": "RIDE", "RISE": "RISE", "ROUND": "RND", "ROW": "ROW", "RISING": "RSG", "RETURN": "RTN",
                                 "RUN": "RUN", "SLOPE": "SLO", "SQUARE": "SQ", "STREET": "ST", "SOUTH": "STH", "STRIP": "STP",
                                 "STEPS": "STPS", "SUBWAY": "SUB", "TERRACE": "TCE", "THROUGHWAY": "THRU", "TOR": "TOR", "TRACK": "TRK",
                                 "TRAIL": "TRL", "TURN": "TURN", "TOLLWAY": "TWY", "UPPER": "UPR", "VALLEY": "VLY", "VISTA": "VST", "VIEWS": "VW",
                                 "VIEW": "VW", "VIEW/S": "VW", "WAY": "WAY", "WOOD": "WD", "WEST": "WEST", "WALK": "WK", "WALKWAY": "WKWY",
                                 "WATERS": "WTRS", "WATERWAY": "WRY", "WYND": "WYD"}

                if line_street_ty in abr_type_list:
                    line_street_ty = abr_type_list[line_street_ty]

                if line_lot != '':
                    line_lot = 'L ' + str(line_lot) + ', '

                if line_unit_house != '':
                    line_unit_house = line_unit_house + ' '

                site_name = line_suburb + ' - ' + line_lot + line_unit_house + line_street_n + ' ' + line_street_ty
                site_address = line_lot + line_unit_house + line_street_n + ' ' + line_street_ty

                return site_name, site_address

            count = 0
            self.results_list_box.delete(0, tk.END)     # Clears list
            for line in self.response:
                count += 1
                formated_line = format_site_info(line.NUM_ADD, line.ROAD_NAME, line.ROAD_TYPE, line.LOCALITY, line.LOT_NUMBER)
                self.results_list_box.insert(tk.END, formated_line[0])      # Adds each line to list

            # Error msg if no results found
            if count == 0:
                self.results_list_box.delete(0, tk.END)
                self.results_list_box.insert(tk.END, '0 Search Results Found.')

    def on_select(self, event):
        try:

            widget = event.widget
            selection = widget.curselection()
            value = widget.get(selection[0])
            # print('SELECTION :' + str(selection))
            # print('VALUE :' + str(value))

            # print(self.response[selection[0]]['EZI_ADD'])
            self.site_name = value
            split_sitename = value.split(' - ')
            # print(split_sitename[0])
            # print(split_sitename[1])

            self.address_textbox.delete(1.0, tk.END)
            self.address_textbox.insert(tk.END, split_sitename[1])

            self.suburb_textbox.delete(1.0, tk.END)
            self.suburb_textbox.insert(tk.END, split_sitename[0])
            suburb_route = str(self.response[selection[0]].DEL_ZONE)

            self.postcode_textbox.delete(1.0, tk.END)
            self.postcode_textbox.insert(tk.END, self.response[selection[0]].POSTCODE)

            self.sitename_textbox.delete(1.0, tk.END)
            self.sitename_textbox.insert(tk.END, value)

            # COORDINATES
            try:
                # Grabs coordinates then removes unnecessary characters from the string then splits into x and y.
                coord_string = self.response[selection[0]].COORDINATES
                coord_string = coord_string.strip('[]')
                coord_string = coord_string.replace(' ', '')
                coord_string = coord_string.split(',')
                self.x_coord, self.y_coord = float(coord_string[1]), float(coord_string[0])

                # Clears long/lat fields then inserts amended data and rounds to 5 decimal places.
                self.lat_textbox.delete(1.0, tk.END)
                self.lat_textbox.insert(tk.END, round(self.x_coord, 5))

                self.long_textbox.delete(1.0, tk.END)
                self.long_textbox.insert(tk.END, round(self.y_coord, 5))
            except Exception as e:
                print("Error: Problem retrieving coordinates from database.")
                print(e)
                pass

            # GET MAP REF
            try:
                # Grabs property PFI from database, property reports are generated based on this number, joins PFI to URL for reportscraper to use.
                selected_pfi = self.response[selection[0]].PR_PFI
                url = 'https://services.land.vic.gov.au/landchannel/content/pdfreport?reportType=detailed&source=propertyportal&propertypfi='\
                      + str(selected_pfi)

                self.selected_report_url = url

                # Default text if no map ref available
                self.map_ref = ''

                # Looks at check box next to search button and decides whether to run the map ref check or not, speeds up searching when disabled.
                if self.map_ref_check.get() == 1:
                        self.map_ref = ReportScraper.report_reader(url)

                # Clears map ref box then inserts new fields.
                self.mapref_textbox.delete(1.0, tk.END)
                self.mapref_textbox.insert(tk.END, self.map_ref)

            except Exception as e:
                print("Error: Unable to detect map reference, property report may not include one.")
                # print(e)
                pass

            # GET DELIVERY ZONE (ALSO CHANGES ZONE TOOLTIP)
            try:
                del_zone = str(self.response[selection[0]].DEL_ZONE)
                del_zone_string = 'Zone ' + del_zone
                self.r_zone_label.configure(text=del_zone_string)

                if del_zone == '2':
                    self.r_site_header_label.configure(background="#b7e2a8")
                    self.r_site_header_label.configure(foreground="black")
                    self.r_zone_label.configure(background="#b7e2a8")
                    self.r_zone_label.configure(foreground="black")
                    self.r_zone_tooltip.text = 'Outer metro area'
                elif del_zone == '3':
                    self.r_site_header_label.configure(background="red")
                    self.r_site_header_label.configure(foreground="white")
                    self.r_zone_label.configure(background="red")
                    self.r_zone_label.configure(foreground="white")
                    self.r_zone_tooltip.text = 'Regional area'
                elif del_zone == '4':
                    self.r_site_header_label.configure(background="#f9ff7a")
                    self.r_site_header_label.configure(foreground="black")
                    self.r_zone_label.configure(background="#f9ff7a")
                    self.r_zone_label.configure(foreground="black")
                    self.r_zone_tooltip.text = 'Ballarat area'
                elif del_zone == '5':
                    self.r_site_header_label.configure(background="#fea41e")
                    self.r_site_header_label.configure(foreground="black")
                    self.r_zone_label.configure(background="#fea41e")
                    self.r_zone_label.configure(foreground="black")
                    self.r_zone_tooltip.text = 'Bendigo area'
                elif del_zone == '6':
                    self.r_site_header_label.configure(background="#7260B0")
                    self.r_site_header_label.configure(foreground="white")
                    self.r_zone_label.configure(background="#7260B0")
                    self.r_zone_label.configure(foreground="white")
                    self.r_zone_tooltip.text = 'Phillip Island area'
                elif del_zone == '7':
                    self.r_site_header_label.configure(background="#2b83ba")
                    self.r_site_header_label.configure(foreground="white")
                    self.r_zone_label.configure(background="#2b83ba")
                    self.r_zone_label.configure(foreground="white")
                    self.r_zone_tooltip.text = 'Geelong area'
                else:
                    self.r_site_header_label.configure(background="#d9d9d9")
                    self.r_site_header_label.configure(foreground="#000000")
                    self.r_zone_label.configure(background="#d9d9d9")
                    self.r_zone_label.configure(foreground="#000000")
                    self.r_zone_tooltip.text = 'Melbourne and surrounding area'

            except Exception as e:
                print(e)

        except Exception:
            pass

    def r_context_menu(self, event):
        if self.right_click_check.get() != 0:  # >>> THIS IS CURRENTLY NOT RETRIEVED FROM ANYWHERE, NEEDS TO BE CHANGEABLE FROM OPTIONS

            y_coord = event.y
            r_click_index = self.results_list_box.nearest(y_coord)
            self.results_list_box.selection_clear(0, tk.END)
            self.results_list_box.selection_set(r_click_index)
            self.results_list_box.activate(r_click_index)
            self.on_select(event)

            # create a menu
            rc_popup = tk.Menu(None, tearoff=0, takefocus=0)
            rc_popup.add_command(label="Copy")
            rc_popup.add_separator()
            rc_popup.add_command(label="Show Map", command=self.show_map)
            rc_popup.add_command(label="Get Property Report", command=self.get_report)
            rc_popup.add_command(label="Open In Google Maps", command=self.send_to_google)

            x, y = root.winfo_pointerxy()
            rc_popup.tk_popup(x, y)

        else:
            pass

    def show_map(self):
        try:
            def map_task():
                try:
                    MapQuery.get_map(self.x_coord, self.y_coord)
                    MapQuery.edit_map(self.site_name, self.map_ref, round(self.x_coord, 5), round(self.y_coord, 5))

                    map_img = Image.open('MapData/Combine_Map.png')
                    map_img.show()
                    map_root.destroy()
                except Exception as e:
                    print(e)
                    map_root.destroy()

            map_root = tk.Tk()
            map_root.title('Loading')
            map_root.resizable(50, 25)
            map_root.geometry("50x25+850+480")

            map_load_label = tk.Label(map_root, text='Loading Map')
            map_load_label.pack()

            map_root.after(200, map_task)
            map_root.mainloop()
        except Exception as e:
            # Throws 500 Server Error: 500 for url:
            # http://services.land.vic.gov.au/catalogue/publicproxy/guest/dv_geoserver/wms?service=WMS&request=GetCapabilities&version=1.3.0
            print(e)
            pass

    def save_map(self):
        try:

            print('Saving the Map')

            MapQuery.get_map(self.x_coord, self.y_coord)
            MapQuery.edit_map(self.site_name, self.map_ref, round(self.x_coord, 5), round(self.y_coord, 5))

            filename = '/' + self.site_name.replace('/', '_') + '.png'
            map_directory = config.get('OPTIONS', 'MAP_SAVE_DIRECTORY')
            copy_location = map_directory
            # print('Map saved to: ' + copy_location + filename)

            shutil.copyfile('MapData/Combine_Map.png', copy_location + filename)

            # Checks if map prompt is enabled or not, displays a message if option is enabled

            if self.map_save_prompt_var.get() == 1:
                messagebox.showinfo("Task Complete", f"Map saved to: {copy_location}{filename}")
            else:
                pass

        except Exception as e:
            # Throws 500 Server Error: 500 for url:
            # http://services.land.vic.gov.au/catalogue/publicproxy/guest/dv_geoserver/wms?service=WMS&request=GetCapabilities&version=1.3.0
            print(e)
            messagebox.showerror("Task Failure", "The map was unable to be saved.\n\n"
                                                 "This error may be due to a network issue or property issue, check your connection and/or the "
                                                 "property report.")
            pass

    def get_report(self):
        try:
            import webbrowser

            webbrowser.open(self.selected_report_url)

        except Exception as e:
            print(e)
            messagebox.showerror("Unable to get Report", "Error getting property report.\n\n"
                                                         "Check your internet connection and try again.")
            pass

    def send_to_google(self):
        try:
            import webbrowser

            google_url = 'https://google.com/maps/search/' + str(round(self.x_coord, 5)) + ',' + str(round(self.y_coord, 5))

            webbrowser.open(google_url)

        except Exception as e:
            print(e)
            messagebox.showerror("Browser Failure", 'Error sending to google maps.\n\n'
                                                    'Check your internet connection and try again.')
            pass

    def clear_all_input(self):
        try:
            self.lot_entry.delete(0, tk.END)
            self.house_entry.delete(0, tk.END)
            self.unit_entry.delete(0, tk.END)
            self.street_name_entry.delete(0, tk.END)
            self.street_type_entry.delete(0, tk.END)
            self.suburb_entry.delete(0, tk.END)
            self.postcode_entry.delete(0, tk.END)
        except:
            pass


def copy_box(box):
    try:
        pyperclip.copy(box)
    except:
        pass


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        # self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped


class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
    def size_(self):
        sz = tk.Listbox.size(self)
        return sz


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


if __name__ == '__main__':
    vp_start_gui()
