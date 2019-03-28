import tkinter as tk
from tkinter import font, messagebox, Menu, Message
from lessons.Lesson_Transition import get_next_lesson, get_previous_lesson, append_new_lesson
from gui.ReferenceWindow import draw_reference
from gui.LessonPage import submit_code, get_text
from gui.Utilities import transfer_to, get_relative_file_path
from lessons.Lesson_Workbook import initialize_workbook

SIDEBAR_COLUMN_WIDTH = 5
registers = []


def draw_menu(root, ttk, next_lesson):
    # Resize in case window has been adjusted
    if root.winfo_width() > 700:
        root.minsize(700, root.winfo_screenheight())
    # Set fonts for the menu widgets.
    # print(font.families()) to print available font families.
    menuLabel_font = font.Font(family="Loma", size=24, weight="bold")
    menuButton_font = font.Font(family="Loma", size=22, weight="normal")
    text_announce = font.Font(family="Gentium Book Basic", size=16, weight="normal")

    # background="..." doesn't work...
    ttk.Style().configure('green/black.TLabel', foreground='black', background='DarkOrange1', font=menuLabel_font)
    ttk.Style().configure('green/black.TButton', foreground='black', background='DarkOrange1', font=menuButton_font,
                          width=25)
    ttk.Style().configure('textBox.TLabel', foreground='black', background='cornflower blue', font=text_announce)

    main_frame = tk.Frame(master=root, bg="medium blue", width=root.winfo_width(), height=root.winfo_height())
    # Fill the empty space of the screen.
    main_frame.pack(expand=True, fill="both")

    label_banner = ttk.Label(main_frame, text='\tWelcome to SMIP.\n Your Best Friend for Learning MIPS ',
                             style='green/black.TLabel', width=700, anchor="center")
    label_plug = ttk.Label(main_frame, style='textBox.TLabel', text=' Our repo: https://github.com/coreyrop/SMIP\n\t'
                                                                    '-Last Updated: 03/26/2019-')

    label_banner.pack(pady=10)
    label_plug.pack(side="bottom", pady=5)

    button1 = ttk.Button(main_frame, text='Start', style='green/black.TButton',
                         command=lambda: transfer_to(
                             lambda: draw_lesson(root, ttk, get_next_lesson(), submit_code, messagebox.showinfo), main_frame))
    button2 = ttk.Button(main_frame, text='Select Lesson', style='green/black.TButton')
    button3 = ttk.Button(main_frame, text='Practice', style='green/black.TButton')
    button4 = ttk.Button(main_frame, text='Reference', style='green/black.TButton', command=draw_reference)
    create_lesson_button = ttk.Button(main_frame, text='Create Lesson', style='green/black.TButton', command=lambda: transfer_to(lambda: draw_create_lessons_form(root, ttk), main_frame))
    button5 = ttk.Button(main_frame, text='Exit', style='green/black.TButton', command=quit)

    button1.pack(pady=30)
    button2.pack(pady=30)
    button3.pack(pady=30)
    button4.pack(pady=30)
    create_lesson_button.pack(pady=30)
    button5.pack(pady=30)
    pass


def draw_lesson(root, ttk, lesson, submit_function, hint_function):
    # Set fonts for the menu widgets.
    # print(font.families()) to print available font families.
    menuLabel_font = font.Font(family="Loma", size=22, weight="bold")
    menuButton_font = font.Font(family="Loma", size=20, weight="normal")
    # background="..." doesn't work...
    ttk.Style().configure('B_DO1.TLabel', foreground='black', background='DarkOrange1', font=menuLabel_font)
    ttk.Style().configure('B_DO1.TButton', foreground='black', background='DarkOrange1', font=menuButton_font, width=15)

    lesson_header = tk.Frame(master=root, bg="medium blue")
    center_frame = tk.Frame(master=root, bg="medium blue")
    bottom_frame_top = tk.Frame(master=root, bg="medium blue")
    bottom_frame_bottom = tk.Frame(master=root, bg="medium blue")
    register_frame = tk.Frame(root, width=200, bg='white', height=500, relief='sunken', borderwidth=2)

    registers = []
    draw_sidebar(register_frame, registers)

    # Pack lesson_header Frame over the top of the center_frame.
    register_frame.pack(expand=True, fill='both', side='left')
    lesson_header.pack(fill="x")
    center_frame.pack(expand=True, fill="both")
    bottom_frame_top.pack(expand=True, fill="both")
    bottom_frame_bottom.pack(expand=True, fill="both", side="bottom")

    label_instruction = ttk.Label(center_frame, text=lesson.lesson_prompt, style='B_DO1.TLabel')
    lesson_input = tk.Text(center_frame, height=30, width=100)
    lesson_input.insert(tk.END, get_text(lesson.code_base))

    label_instruction.pack(side="top", pady=5)
    lesson_input.pack(pady=20, padx=10)

    menu_escape = ttk.Button(bottom_frame_top, text='Main Menu', style='B_DO1.TButton', cursor="target",
                             command=lambda: transfer_to(lambda: draw_menu(root, ttk, lesson), center_frame,
                                                         bottom_frame_top, bottom_frame_bottom, register_frame))
    hint_button = ttk.Button(bottom_frame_bottom, text='Hint', style='B_DO1.TButton',
                             cursor="target", command=lambda: hint_function("Hint", lesson.lesson_hint))
    reference_button = ttk.Button(bottom_frame_bottom, text='Reference', style='B_DO1.TButton',
                                  cursor="target", command=draw_reference)
    submit_button = ttk.Button(bottom_frame_top, text='Submit Code', style='B_DO1.TButton',
                               cursor="target", command=lambda: submit_function(lesson_input, registers, lesson))

    menu_escape.pack(side='left', padx=10)
    submit_button.pack(side='right', padx=10)
    hint_button.pack(side='left', padx=10)
    reference_button.pack(side='right', padx=10)
    pass


def draw_sidebar(sidebar, registers):
    tk.Label(sidebar, text="NAME", width=SIDEBAR_COLUMN_WIDTH).grid(row=0, column=0)
    tk.Label(sidebar, text="NUM", width=SIDEBAR_COLUMN_WIDTH).grid(row=0, column=1)
    tk.Label(sidebar, text="VALUE", width=SIDEBAR_COLUMN_WIDTH).grid(row=0, column=2)

    for i in range(32):
        label = tk.Label(sidebar, text="0", width="5")
        label.grid(row=i + 1, column=2)
        registers.append(label)  # global arr so labels can be updated

    tk.Label(sidebar, text="$zero", width=SIDEBAR_COLUMN_WIDTH).grid(row=1, column=0)
    tk.Label(sidebar, text="$at", width=SIDEBAR_COLUMN_WIDTH).grid(row=2, column=0)
    tk.Label(sidebar, text="$v0", width=SIDEBAR_COLUMN_WIDTH).grid(row=3, column=0)
    tk.Label(sidebar, text="$v1", width=SIDEBAR_COLUMN_WIDTH).grid(row=4, column=0)
    tk.Label(sidebar, text="$a0", width=SIDEBAR_COLUMN_WIDTH).grid(row=5, column=0)
    tk.Label(sidebar, text="$a1", width=SIDEBAR_COLUMN_WIDTH).grid(row=6, column=0)
    tk.Label(sidebar, text="$a2", width=SIDEBAR_COLUMN_WIDTH).grid(row=7, column=0)
    tk.Label(sidebar, text="$a3", width=SIDEBAR_COLUMN_WIDTH).grid(row=8, column=0)
    tk.Label(sidebar, text="$t0", width=SIDEBAR_COLUMN_WIDTH).grid(row=9, column=0)
    tk.Label(sidebar, text="$t1", width=SIDEBAR_COLUMN_WIDTH).grid(row=10, column=0)
    tk.Label(sidebar, text="$t2", width=SIDEBAR_COLUMN_WIDTH).grid(row=11, column=0)
    tk.Label(sidebar, text="$t3", width=SIDEBAR_COLUMN_WIDTH).grid(row=12, column=0)
    tk.Label(sidebar, text="$t4", width=SIDEBAR_COLUMN_WIDTH).grid(row=13, column=0)
    tk.Label(sidebar, text="$t5", width=SIDEBAR_COLUMN_WIDTH).grid(row=14, column=0)
    tk.Label(sidebar, text="$t6", width=SIDEBAR_COLUMN_WIDTH).grid(row=15, column=0)
    tk.Label(sidebar, text="$t7", width=SIDEBAR_COLUMN_WIDTH).grid(row=16, column=0)
    tk.Label(sidebar, text="$s0", width=SIDEBAR_COLUMN_WIDTH).grid(row=17, column=0)
    tk.Label(sidebar, text="$s1", width=SIDEBAR_COLUMN_WIDTH).grid(row=18, column=0)
    tk.Label(sidebar, text="$s2", width=SIDEBAR_COLUMN_WIDTH).grid(row=19, column=0)
    tk.Label(sidebar, text="$s3", width=SIDEBAR_COLUMN_WIDTH).grid(row=20, column=0)
    tk.Label(sidebar, text="$s4", width=SIDEBAR_COLUMN_WIDTH).grid(row=21, column=0)
    tk.Label(sidebar, text="$s5", width=SIDEBAR_COLUMN_WIDTH).grid(row=22, column=0)
    tk.Label(sidebar, text="$s6", width=SIDEBAR_COLUMN_WIDTH).grid(row=23, column=0)
    tk.Label(sidebar, text="$s7", width=SIDEBAR_COLUMN_WIDTH).grid(row=24, column=0)
    tk.Label(sidebar, text="$t8", width=SIDEBAR_COLUMN_WIDTH).grid(row=25, column=0)
    tk.Label(sidebar, text="$t9", width=SIDEBAR_COLUMN_WIDTH).grid(row=26, column=0)
    tk.Label(sidebar, text="$k0", width=SIDEBAR_COLUMN_WIDTH).grid(row=27, column=0)
    tk.Label(sidebar, text="$k1", width=SIDEBAR_COLUMN_WIDTH).grid(row=28, column=0)
    tk.Label(sidebar, text="$gp", width=SIDEBAR_COLUMN_WIDTH).grid(row=29, column=0)
    tk.Label(sidebar, text="$sp", width=SIDEBAR_COLUMN_WIDTH).grid(row=30, column=0)
    tk.Label(sidebar, text="$fp", width=SIDEBAR_COLUMN_WIDTH).grid(row=31, column=0)
    tk.Label(sidebar, text="$ra", width=SIDEBAR_COLUMN_WIDTH).grid(row=32, column=0)
    for i in range(32):
        tk.Label(sidebar, text=i, width=SIDEBAR_COLUMN_WIDTH).grid(row=i + 1, column=1)
    pass


def draw_create_lessons_form(root, ttk):
    # Need extra room because we have 3 rows of info.
    root.minsize(900, root.winfo_screenheight())
    # Cover the whole screen with the frame.
    main_frame = tk.Frame(root, bg='medium blue', width=root.winfo_width(), height=root.winfo_height())
    # Fill the frame with the background.
    main_frame.pack(expand=True, fill="both")
    # Include separate font choices for human readable text.
    menuButton_font = font.Font(family="Loma", size=22, weight="bold")
    create_field_font = font.Font(family="Loma", size=20, weight="normal")
    create_button_font = font.Font(family="Loma", size=18, weight="bold")
    register_label_font = font.Font(family="Latin Modern Roman", size=14, weight="bold")
    register_entry_font = font.Font(family="Latin Modern Roman", size=14, weight="normal")
    # Apply style settings.
    ttk.Style().configure('B_DO1.TLabel', foreground='black', background='DarkOrange1', width=20,
                          font=create_field_font, anchor="CENTER")
    ttk.Style().configure('B_DO1.TButton', foreground='black', background='DarkOrange1', font=create_button_font, width=15)
    ttk.Style().configure('menu_buttons.TButton', foreground='black', background='DarkOrange1', font=menuButton_font,
                          width=15, padx=5)
    ttk.Style().configure('references.TLabel', foreground='black', background='DarkOrange1', width=12,
                          font=create_field_font, anchor="CENTER")
    ttk.Style().configure('TMenuButton', background='DarkOrange1')

    # Define register fields.
    register_fields = {i: {} for i in range(32)}

    references = []

    # Make an "added reference dropdown" which reflects added references.
    str_var = tk.StringVar(root)
    included_references = ['None']
    str_var.set('None')
    reference_menu = tk.OptionMenu(main_frame, str_var, *included_references)

    lesson_title_label = ttk.Label(main_frame, text='Lesson Title', style='B_DO1.TLabel')
    lesson_prompt_label = ttk.Label(main_frame, text='Lesson Prompt', style='B_DO1.TLabel')
    lesson_hint_label = ttk.Label(main_frame, text='Lesson Hint', style='B_DO1.TLabel')
    lesson_filepath_label = ttk.Label(main_frame, text='Relative File Path', style='B_DO1.TLabel')
    reference_menu_label = ttk.Label(main_frame, text='References', style='references.TLabel')

    for i in register_fields.keys():
        register_fields[i]['label'] = ttk.Label(main_frame, text='$r'+str(i)+' ', font=register_label_font)

    lesson_title_label.grid(row=0, column=0, pady=10, padx=20)
    lesson_prompt_label.grid(row=1, column=0, pady=10)
    lesson_hint_label.grid(row=2, column=0, pady=10)
    lesson_filepath_label.grid(row=3, column=0, pady=20)
    reference_menu_label.grid(row=0, column=2)
    reference_menu.grid(row=1, column=2)

    for i in register_fields.keys():
        if i < 16:
            if i > 9:
                new_text = register_fields[i]['label'].cget("text")
                register_fields[i]['label'] = ttk.Label(main_frame, text=new_text[:4], font=register_label_font)
            register_fields[i]['label'].grid(row=i+4, column=1, sticky='w', padx=10)
        else:
            new_text = register_fields[i]['label'].cget("text")
            register_fields[i]['label'] = ttk.Label(main_frame, text=new_text[:4], font=register_label_font)
            register_fields[i]['label'].grid(row=i-16+4, column=1, stick='e', padx=3)

    lesson_title_entry = ttk.Entry(main_frame, font=create_button_font)
    lesson_prompt_entry = ttk.Entry(main_frame, font=create_button_font)
    lesson_hint_entry = ttk.Entry(main_frame, font=create_button_font)
    lesson_filepath_current_label = ttk.Label(main_frame, text='None Set', font=create_field_font, width=9,
                                              anchor='center')
    for i in register_fields.keys():
        register_fields[i]['entry'] = ttk.Entry(main_frame, font=register_entry_font)

    lesson_title_entry.grid(row=0, column=1)
    lesson_prompt_entry.grid(row=1, column=1)
    lesson_hint_entry.grid(row=2, column=1)
    lesson_filepath_current_label.grid(row=3, column=1)
    for i in register_fields.keys():
        if i < 16:
            register_fields[i]['entry'].grid(row=i+4, column=0, sticky='e', padx=3)
        else:
            register_fields[i]['entry'].grid(row=i-16+4, column=2, padx=3)

    lesson_filepath_button = ttk.Button(main_frame, text='Select', cursor='target', style='B_DO1.TButton',
                                        command=lambda: lesson_filepath_current_label.config(text=get_relative_file_path([('MIPS code files', '*.s')])))
    lesson_filepath_button.grid(row=3, column=2)

    main_menu_button = ttk.Button(main_frame, text='Main Menu', cursor='target', style='menu_buttons.TButton',
                                  command=lambda: transfer_to(lambda: draw_menu(root, ttk, None), main_frame))

    def submit_confirmation():
        append_new_lesson(initialize_workbook('../lesson_files/' + lesson_title_entry.get(),
                                              lesson_title=lesson_title_entry.get(),
                                              lesson_prompt=lesson_prompt_entry.get(),
                                              lesson_hint=lesson_hint_entry.get(),
                                              lesson_filepath=lesson_filepath_current_label
                                              ['text'],
                                              registers={
                                                  j: register_fields[j]['entry'].get() for j in
                                                  register_fields.keys()}, references=references))

        lesson_title_entry.delete(0, 'end')
        lesson_prompt_entry.delete(0, 'end')
        lesson_hint_entry.delete(0, 'end')
        lesson_filepath_current_label.config(text='None Set')

        included_references.clear()
        reference_menu['menu'].delete(0, 'end')
        reference_menu['menu'].add_command(label='None', command=lambda : str_var.set('None'))

        for i in register_fields.keys():
            register_fields[i]['entry'].delete(0, 'end')
        pass

    submit_lesson_button = ttk.Button(main_frame, text='Create Lesson', cursor='target', style='menu_buttons.TButton',
                                      command=submit_confirmation)

    def submit_ref(ref, dict, win):
        ref.append(dict)
        included_references.append(dict['Name'])
        reference_menu['menu'].add_command(label = dict['Name'], command=lambda value=dict['Name']: str_var.set(value))
        win.destroy()
        pass

    def add_pdf_reference_form(references):

        win = tk.Toplevel()
        win.wm_title("Add PDF Reference")

        name_label = tk.Label(win, text="Reference Name")
        name_label.grid(row=0, column=0)

        name_entry = tk.Entry(win, font=create_field_font)
        name_entry.grid(row=0, column=1)

        current_path_label = tk.Label(win, text='None Set', font=create_field_font)
        select_file_button = ttk.Button(win, text="Select PDF", command=lambda: current_path_label.config(text=get_relative_file_path([('PDF files','*.pdf')])))
        select_file_button.grid(row=1, column=0)
        current_path_label.grid(row=1, column=1)

        submit_button = tk.Button(win, text='Add Reference', command=lambda: submit_ref(references, {'Name': name_entry.get(), 'Type': 'local_file', 'Path': current_path_label['text']}, win))
        submit_button.grid(row=2, column=0)
        pass

    def add_link_reference_form(references):

        win = tk.Toplevel()
        win.wm_title("Add Link Reference")

        name_label = tk.Label(win, text="Reference Name")
        name_label.grid(row=0, column=0)

        name_entry = tk.Entry(win, font=create_field_font)
        name_entry.grid(row=0, column=1)

        url_label = tk.Label(win, text='URL')
        url_entry = tk.Entry(win, font=create_field_font)
        url_label.grid(row=1, column=0)
        url_entry.grid(row=1, column=1)

        submit_button = tk.Button(win, text='Add Reference',
                      command=lambda: submit_ref(references, {'Name': name_entry.get(), 'Type': 'web_link', 'Path': url_entry.get()},
                                                 win))
        submit_button.grid(row=2, column=0)
        pass

    popup = Menu(root, tearoff=0, bg='#f27446', font=20)
    popup.add_command(label='PDF', command=lambda: add_pdf_reference_form(references))
    popup.add_command(label='Link', command=lambda : add_link_reference_form(references))

    reference_menu_button = ttk.Button(main_frame, text='Add a Reference', cursor='target', style='menu_buttons.TButton')
    reference_menu_button.bind("<ButtonRelease-1>", lambda event: popup.tk_popup(event.x_root, event.y_root, 0))

    reference_menu_button.grid(row=2, column=2, padx=10)
    main_menu_button.grid(row=40, column=0, sticky='s')
    submit_lesson_button.grid(row=40, column=1, sticky='s')
    pass
