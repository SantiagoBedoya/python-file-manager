import tkinter
import explorer

MASTER_PATH = "./test"
exp = explorer.Explorer(MASTER_PATH)
nodes = sorted(exp.list(), key=lambda x: x.name, reverse=True)

def render_items(data):
    for node in data:
        if node.is_file:
            lb.insert(tkinter.END, f"- {node.name}")
        else:
            lb.insert(tkinter.END, f"> {node.name}")

def prev():
    if len(exp.history) >= 2:
        exp.history.pop()
        new_path = exp.history[-1]
        new_nodes = exp.list(new_path)
        lb.delete(0, tkinter.END)
        print(new_nodes)
        render_items(new_nodes)



t = tkinter.Tk()
t.geometry("500x500")
t.title("File Manager")
t.resizable(width=False, height=False)


prev_btn = tkinter.Button(t, text="<-", width=2, height=1, command=prev)
prev_btn.grid(row=0, column=0)

search_entry = tkinter.Entry(t, width=40)
search_entry.grid(row=0, column=100)

search_btn = tkinter.Button(t, text="Search", width=4, height=1)
search_btn.grid(row=0, column=101)

lb = tkinter.Listbox(
    t,
    font=('Times', 18),
    bd=0,
    width=55,
    height=20,
    fg='#464646',
    highlightthickness=0,
    selectbackground='#a6a6a6',
    activestyle="none",
)
lb.grid(row=3, columnspan=120, pady=10)

lb_scrollbar = tkinter.Scrollbar(t)
lb.config(yscrollcommand=lb_scrollbar.set)
lb_scrollbar.config(command=lb.yview)

def callback(event):
    selection = event.widget.curselection()
    data = event.widget.get(selection[0])
    data = data.replace("> ", "")
    if exp.is_folder(data):
        new_nodes = exp.list(data)
        lb.delete(0, tkinter.END)
        render_items(new_nodes)

lb.bind("<Double-1>", callback)

render_items(nodes)

t.mainloop()


