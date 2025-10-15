import tkinter as tk #Лаб. раб. №10. Ченакин В.Г ИСТбд-24
from tkinter import messagebox as mb
root = tk.Tk()
root.title("Крестики-нолики")
root.geometry("400x400")
board = [""] * 9
player = "X"
def click(i):
    global player
    if board[i]: return
    board[i] = player
    btns[i]["text"] = player
    if any(board[a]==board[b]==board[c]==player for a,b,c in ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))):
        mb.showinfo("Результат", f"Победил {player}")
        reset(); return
    if all(board):
        mb.showinfo("Результат", "Ничья")
        reset(); return
    player = "O" if player == "X" else "X"
def reset():
    global board, player
    board = [""] * 9
    player = "X"
    for b in btns: b.config(text="", state="normal")
frm = tk.Frame(root)
frm.pack(expand=True)
btns = [tk.Button(frm, text="", width=5, height=2,font=("Arial", 32), command=lambda i=i: click(i)) for i in range(9)]
for i, b in enumerate(btns): b.grid(row=i//3, column=i%3, padx=5, pady=5)
for i in range(3):
    frm.grid_columnconfigure(i, weight=1)
    frm.grid_rowconfigure(i, weight=1)
root.mainloop()
