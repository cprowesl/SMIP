import tkinter as tk
from lessons.Submission import run_MIPS
from lessons.Lesson_Transition import lessons, write_completed
"""
Draws a lesson to the frame
root: tkinter root to draw to 
ttk: tkinter ttk used for styling
lesson: the lesson to be drawn to the screen
"""


def submit_code(user_input, register_labels, lesson):
    filename = '../lesson_files/Submissions/'+lesson.lesson_title + '(Submission).s'
    f = open(filename, 'w')
    f.write(user_input.get("1.0", tk.END))
    f.close()

    results = run_MIPS(filename)
    update_registers(results, register_labels)


    if lesson.check_solution(results):
        lesson.lesson_completed = True
        write_completed(lesson.lesson_title, True)
        print('Passed!!')
    else:
        lesson.lesson_completed = False
        write_completed(lesson.lesson_title, False)
        print('Failed!!')
    pass


def run_practice(user_input, register_labels):
    filename = '../lesson_files/Submissions/(Practice).s'
    f = open(filename, 'w')
    f.write(user_input.get("1.0", tk.END))
    f.close()
    results = run_MIPS(filename)
    update_registers(results, register_labels)
    print(" SMIP RUNS YOUR  CODE ")
    pass


def get_text(filename):
    try:
        f = open(filename, 'r')
        output = ""
        for x in f.readlines():
            output += x
        f.close()
        return output
    except FileNotFoundError:
        return "No base code"


def update_registers(answers, register_labels):
    for register, value in answers.items():
        register_labels[register].config(text=value)
    pass


def populate_lesson_completed(dict):
    for title in dict:
        for i in range(len(lessons)):
            if (title == lessons[i].lesson_title):
                lessons[i].lesson_completed = True
    return lessons
