from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox, Checkbutton, Radiobutton


def clicked():
    res = f"Hello {entry_hello.get()}"
    lbl_hello.configure(text=res)


def radio():
    messagebox.showinfo('name', 'text')


def open_file():
    file = filedialog.askopenfilename()


window = Tk()
window.title("welcome")
window.geometry("400x250")

menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label="open", command=open_file)
new_item.add_separator()
new_item.add_command(label="text", command=clicked)
menu.add_cascade(label="file", menu=new_item)
window.config(menu=menu)

lbl_hello = Label(window, text="hello")
lbl_hello.grid(column=0, row=0)

btn_press = Button(window, text="press", command=clicked)
btn_press.grid(column=1, row=0)

entry_hello = Entry(window, width=10)
entry_hello.grid(column=1, row=1)
entry_hello.focus()

combo = Combobox(window)
combo['values'] = (1, 2, 3, 4, 5, "text")
combo.current(1)
combo.grid(column=0, row=2)

chk_state = BooleanVar()
chk_state.set(True)
chk = Checkbutton(window, text="select")
chk.grid(column=0, row=3)

rad1 = Radiobutton(window, text="text", value=1, command=radio)
rad1.grid(column=0, row=4)
rad2 = Radiobutton(window, text="file", value=2, command=open_file)
rad2.grid(column=1, row=4)

window.mainloop()
