import db
import customtkinter as ctk

ctk.set_appearance_mode('light')
window = ctk.CTk(fg_color='#e2e2e2')
window.geometry('1000x800+{}+{}'.format(
    (window.winfo_screenwidth() // 2) - 500, (window.winfo_screenheight() // 2) - 400
))
window.resizable(False, False)

font_title = ctk.CTkFont(family='Helvetica', size=44)
font_text = ctk.CTkFont(family='Arial', size=20)
font_code = ctk.CTkFont(family='Calibri', size=14)
font_entry = ctk.CTkFont(family='Arial', size=16)
font_button = ctk.CTkFont(family='Cascadia Code', size=16)

color_green = '#0ba100'
color_red = '#d40000'



def command_login(label_status : ctk.CTkLabel, username : str, password : str):
    global window
    global color_red
  
    e = db.user_login(username, password)
    if e: 
        label_status.configure(text='username or password are incorrect', text_color=color_red)
        return
    for child in list(window.children.values()):
        child.destroy()
    window.unbind_all('<Return>')
    load_mainscreen()


def command_register(label_status : ctk.CTkLabel, username : str, password : str):
    global window
    global color_red
    global color_green

    e = db.user_insert(username, password)
    if e:
        if e.status == 101:
            label_status.configure(text='username must be at least 3 chars long and printable', text_color=color_red)
        elif e.status == 102:
            label_status.configure(text='password must be atleast 8 chars long', text_color=color_red)
        else:
            label_status.configure(text='this username already exist', text_color=color_red)
        return
    label_status.configure(text='user created, login to continue', text_color=color_green) 


def command_logout():
    global window

    db.user_logout()
    for child in list(window.children.values()):
        child.destroy()
    load_loginscreen()


def command_add(label_status : ctk.CTkLabel):
    global window
    global font_text
    global color_green
    global color_red

    dialog = ctk.CTkInputDialog(
        text="Type item's name:",
        font=font_text, 
        title="Add item: name",
    )
    dialog.geometry('300x200+{0}+{1}'.format(
        (window.winfo_x() + 500) - 150, (window.winfo_y() + 400) - 100
    ))
    name = dialog.get_input()
    if name == None: 
        label_status.configure(text='dialog window was closed', text_color=color_red)
        return
    
    dialog = ctk.CTkInputDialog(
        text="Type item's description:", 
        font=font_text, 
        title="Add item: description",
    )
    dialog.geometry('300x200+{0}+{1}'.format(
        (window.winfo_x() + 500) - 150, (window.winfo_y() + 400) - 100
    ))
    description = dialog.get_input()
    if description == None: 
        label_status.configure(text='dialog window was closed', text_color=color_red)
        return

    e = db.item_insert(name, description)
    if e: label_status.configure(text=e.__str__(), text_color=color_red)
    else: label_status.configure(text='item added to database', text_color=color_green)


def command_remove(label_status : ctk.CTkLabel):
    global window
    global font_text
    global color_green
    global color_red

    dialog = ctk.CTkInputDialog(
        text="Type item's id:",
        font=font_text, 
        title="Remove item: id",
    )
    dialog.geometry('300x200+{0}+{1}'.format(
        (window.winfo_x() + 500) - 150, (window.winfo_y() + 400) - 100
    ))
    id = dialog.get_input()
    if id == None: 
        label_status.configure(text='dialog window was closed', text_color=color_red)
        return
    if not id.isnumeric():
        label_status.configure(text='id input must be a number', text_color=color_red)
        return
    id = int(id)

    e = db.item_remove(id)
    if e: label_status.configure(text=e.__str__(), text_color=color_red)
    else: label_status.configure(text='item removed from database', text_color=color_green)


def command_book(label_status : ctk.CTkLabel, unbook : bool = False):
    global window
    global font_text
    global color_green
    global color_red

    dialog = ctk.CTkInputDialog(
        text="Type item's id:",
        font=font_text, 
        title="Book item: id",
    )
    dialog.geometry('300x200+{0}+{1}'.format(
        (window.winfo_x() + 500) - 150, (window.winfo_y() + 400) - 100
    ))
    id = dialog.get_input()
    if id == None: 
        label_status.configure(text='dialog window was closed', text_color=color_red)
        return
    if not id.isnumeric():
        label_status.configure(text='id input must be a number', text_color=color_red)
        return
    id = int(id)

    e = db.item_book(id, unbook)
    if e: label_status.configure(text=e.__str__(), text_color=color_red)
    else: label_status.configure(text='item was unbooked', text_color=color_green)


def command_update(label_status : ctk.CTkLabel):
    global window
    global font_text
    global color_green
    global color_red

    dialog = ctk.CTkInputDialog(
        text="Type item's id:",
        font=font_text, 
        title="Update item: id",
    )
    dialog.geometry('300x200+{0}+{1}'.format(
        (window.winfo_x() + 500) - 150, (window.winfo_y() + 400) - 100
    ))
    id = dialog.get_input()
    if id == None: 
        label_status.configure(text='dialog window was closed', text_color=color_red)
        return
    if not id.isnumeric():
        label_status.configure(text='id input must be a number', text_color=color_red)
        return
    id = int(id)

    dialog = ctk.CTkInputDialog(
        text="Type item's name (or press cancel to not change it's name):",
        font=font_text, 
        title="Update item: name",
    )
    dialog.geometry('400x250+{0}+{1}'.format(
        (window.winfo_x() + 500) - 200, (window.winfo_y() + 400) - 125
    ))
    name = dialog.get_input()
    
    dialog = ctk.CTkInputDialog(
        text="Type item's description (or press cancel to not change it's description):", 
        font=font_text, 
        title="Change item: description",
    )
    dialog.geometry('400x250+{0}+{1}'.format(
        (window.winfo_x() + 500) - 200, (window.winfo_y() + 400) - 125
    ))
    description = dialog.get_input()

    e = db.item_update(id, name, description)
    if e: label_status.configure(text=e.__str__(), text_color=color_red)
    else: label_status.configure(text='item updated in database', text_color=color_green)


def command_get(textbox_get : ctk.CTkTextbox, label_status : ctk.CTkLabel, fieldname : str, fieldvalue : str):
    global window
    global font_text
    global color_green
    global color_red

    if fieldname == 'id' or fieldname == 'last_user_id' or fieldname == 'current_user_id':
        if fieldvalue.isnumeric():
            fieldvalue = int(fieldvalue)
        else:
            label_status.configure(text='id input must be a number', text_color=color_red)
            return

    e = db.item_get(fieldname, fieldvalue)
    if isinstance(e, db.Error):
        label_status.configure(text=e.__str__(), text_color=color_red)
        return 
    textbox_get.delete('0.0', 'end')
    if len(e) == 0:
        textbox_get.insert('0.0', 'No results :(')
        return
    for row, data in enumerate(e):
        textbox_get.insert('0.0', '\n')
        textbox_get.insert('0.0', f'{data[0]} | {data[1]} | {data[2]} | {data[3]} | {data[4]} | {data[5]}')


def load_mainscreen():
    global window
    global font_title
    global font_text
    global font_entry
    global font_button

    window.title('Main Screen')

    frame_main = ctk.CTkFrame(
        window, 
        fg_color='#d5d5d5',
        height=500, 
        width=750, 
    )
    frame_main.place(
        anchor=ctk.CENTER,
        relx=0.5, 
        rely=0.5, 
    )
    frame_main.pack_propagate(False)
    
    button_add = ctk.CTkButton(
        frame_main,
        text='Add',
        font=font_button,
        command=lambda:command_add(label_status),
    )   
    button_add.pack(
        anchor=ctk.NW,
        pady=10,
        padx=10,
    )

    button_del = ctk.CTkButton(
        frame_main,
        text='Delete',
        font=font_button,
        command=lambda:command_remove(label_status),
    )   
    button_del.pack(
        anchor=ctk.NW,
        pady=10,
        padx=10,
    )

    button_book = ctk.CTkButton(
        frame_main,
        text='Book',
        font=font_button,
        command=lambda:command_book(label_status),
    )   
    button_book.pack(
        anchor=ctk.NW,
        pady=10,
        padx=10,
    )

    button_unbook = ctk.CTkButton(
        frame_main,
        text='Unbook',
        font=font_button,
        command=lambda:command_book(label_status, True),
    )   
    button_unbook.pack(
        anchor=ctk.NW,
        pady=10,
        padx=10,
    )

    button_update = ctk.CTkButton(
        frame_main,
        text='Update',
        font=font_button,
        command=lambda:command_update(label_status),
    )   
    button_update.pack(
        anchor=ctk.NW,
        pady=10,
        padx=10,
    )
    
    button_logout = ctk.CTkButton(
        frame_main,
        text='Logout',
        font=font_button,
        command=lambda:command_logout()
    )   
    button_logout.pack(
        anchor=ctk.SW,
        side='bottom',
        pady=10,
        padx=10,
    )

    label_status = ctk.CTkLabel(
        frame_main,
        text='',
        font=font_code,
    )
    label_status.pack(
        anchor=ctk.SW,
        side='bottom',
        pady=10,
        padx=10,
    )

    frame_get = ctk.CTkFrame(
        frame_main,
        width=140,
        border_color='#ffffff',
        border_width=1,
    )
    frame_get.pack(
        anchor=ctk.NW,
        pady=10,
        padx=10,
    )
    frame_get.pack_propagate(False)

    label_get = ctk.CTkLabel(
        frame_get,
        text='Get menu:',
        font=font_text,
    )
    label_get.pack(
        anchor=ctk.N,
        pady=5,
        padx=10,
    )

    options_menu = ctk.CTkOptionMenu(
        frame_get,
        values=[
            'all',
            'id',
            'name',
            'current_user_id',
            'last_user_id',
        ],
        height=22,
        font=font_button,
    )
    options_menu.pack(
        anchor=ctk.N,
        pady=5,
        padx=10,
    )

    entry_get = ctk.CTkEntry(
        frame_get,
        font=font_entry, 
        text_color='#333333',
        height=22
    )
    entry_get.pack(
        anchor=ctk.N,
        pady=5,
        padx=10,
    )
    
    button_get = ctk.CTkButton(
        frame_get,
        text='search',
        font=font_button,
        height=22,
        command=lambda:command_get(textbox_get, label_status, options_menu.get(), entry_get.get()),
    )
    button_get.pack(
        anchor=ctk.N,
        pady=5,
        padx=10
    )

    textbox_get = ctk.CTkTextbox(
        frame_main,
        width=frame_main.winfo_width()-220,
        height=frame_main.winfo_height()-20,
        border_color='#ffffff',
        border_width=1,
        fg_color='#e0e0e0',
        font=font_text,
    )
    textbox_get.insert('0.0', 'No data found :(\nUse get menu to search for items')
    textbox_get.place(
        x=185,
        y=10,
    )

    window.bind('<Return>', lambda e:command_get(textbox_get, label_status, options_menu.get(), entry_get.get()))


def load_loginscreen():
    global window
    global font_title
    global font_text
    global font_code
    global font_entry
    global font_button

    window.title('Login Screen')

    title = ctk.CTkLabel(
        window, 
        font=font_title,
        text='Institution Management Technique System', 
    )
    title.place(
        anchor=ctk.CENTER,
        relx=0.5, 
        rely=0.15, 
    )

    frame_main = ctk.CTkFrame(
        window, 
        fg_color='#d5d5d5',
        height=350, 
        width=500, 
    )
    frame_main.place(
        anchor=ctk.CENTER,
        relx=0.5, 
        rely=0.5, 
    )
    frame_main.pack_propagate(False)

    label_username = ctk.CTkLabel(
        frame_main, 
        font=font_text,
        text='Enter your username:',
    )
    label_username.pack(
        anchor=ctk.NW,
    )

    entry_username = ctk.CTkEntry(
        frame_main, 
        font=font_entry, 
        text_color='#333333',
        height=24,
        width=300,
    )
    entry_username.pack(
        anchor=ctk.NW,
    )

    emptyspace = ctk.CTkLabel(
        frame_main,
        text='',
        height=10
    )
    emptyspace.pack(
        anchor=ctk.NW,
    )

    label_password = ctk.CTkLabel(
        frame_main, 
        font=font_text,
        text='Enter password:',
    )
    label_password.pack(
        anchor=ctk.NW,
    )

    entry_password = ctk.CTkEntry(
        frame_main, 
        font=font_entry, 
        text_color='#333333',
        height=24,
        width=300,
        show='*',
    )
    entry_password.pack(
        anchor=ctk.NW,
    )

    label_status = ctk.CTkLabel(
        frame_main, 
        font=font_code,
        text='',
    )
    label_status.pack(
        anchor=ctk.N,
        pady=15,
    )

    button_register = ctk.CTkButton(
        frame_main,
        text='Register',
        font=font_button,
        command=lambda:command_register(label_status, entry_username.get(), entry_password.get()),
    )
    button_register.pack(
        side='bottom',
        pady=20,
    )

    button_login = ctk.CTkButton(
        frame_main,
        text='Login',
        font=font_button,
        command=lambda:command_login(label_status, entry_username.get(), entry_password.get()),
    )
    button_login.pack(
        side='bottom',
        pady=10,
    )

    window.bind('<Return>', lambda e:command_login(label_status, entry_username.get(), entry_password.get()))    



load_loginscreen()
window.mainloop()