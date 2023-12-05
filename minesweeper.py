# tkinter ライブラリをインポート
import tkinter as tk
from tkinter import messagebox
import random

# マインスイーパの盤面を生成する関数
def create_board(rows, cols, num_mines):
    # 初期化された盤面を作成
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # 地雷を配置, 地雷が配置されたマスは -1 
    for _ in range(num_mines):
        row, col = random.randint(0, rows-1), random.randint(0, cols-1)
        while board[row][col] == -1:
            row, col = random.randint(0, rows-1), random.randint(0, cols-1)
        board[row][col] = -1

    return board

# 特定のマスの周囲の地雷の数を数える関数
def count_adjacent_mines(board, row, col):
    if board[row][col] == -1:
        return -1
    
    count = 0
    for i in range(max(0, row-1), min(len(board), row+2)):
        for j in range(max(0, col-1), min(len(board[0]), col+2)):
            if board[i][j] == -1:
                count += 1

    return count

# 特定のマスをクリックした際の処理を行う関数
def click_cell(board, row, col):
    buttons[row][col]["bg"] = put_color
    if board[row][col] == -1:
        return False
    else:
        board[row][col] = count_adjacent_mines(board, row, col)
        return True

# ゲームクリアの条件を確認する関数
def check_clear(board):
    global game_over

    if all(board[i][j] == -1 or not button_state[i][j] for i in range(rows) for j in range(cols)):
        game_over = True

        # ゲームクリアメッセージを表示
        messagebox.showinfo("finish", "ゲームクリア")

# ボタンの状態を更新する関数
def update_buttons():
    for i in range(rows):
        for j in range(cols):
            if buttons[i][j]["text"] == "F":
                buttons[i][j].config(text="F", state=tk.DISABLED)
            elif not button_state[i][j]:
                buttons[i][j].config(text=str(board[i][j]), state=tk.DISABLED)
            else:
                buttons[i][j]["bg"] = buttons[i][j]["bg"]
                if buttons[i][j]["text"] == "?":
                    buttons[i][j].config(text="?", state=tk.NORMAL)
                else:
                    buttons[i][j].config(text="", state=tk.DISABLED)
    check_clear(board)

# 特定のマスにフラグを立てる関数
def flag_cell(row, col):
    global flags

    if button_state[row][col]:
        buttons[row][col].config(text="F")
        button_state[row][col] = False
        flags += 1

# 特定のマスのフラグを取り消す関数
def unflag_cell(row, col):
    global flags

    if not button_state[row][col] and buttons[row][col]["text"] == "F":
        buttons[row][col].config(text="?")
        button_state[row][col] = True
        flags -= 1

# 特定のマスのマークを取り消す関数
def unmark_cell(row, col):
    if not button_state[row][col]:
        return
    
    if buttons[row][col]["text"] == "?":
        buttons[row][col].config(text="")
        button_state[row][col] = True

# 左クリックが行われた際の処理を行う関数
def leftclick_button(row, col, event):    
    if not button_state[row][col]:
        return

    if not click_cell(board, row, col):
        game_over = True
        for i in range(rows):
            for j in range(cols):
                if buttons[i][j]["text"] != "":
                    buttons[i][j]["text"] = buttons[i][j]["text"]
                elif board[i][j] == -1:
                    buttons[i][j]["text"] = "Bomb"
        # ゲームオーバーメッセージを表示
        messagebox.showinfo("finish", "ゲームオーバー")
    else:
        button_state[row][col] = False
        update_buttons()

# 右クリックが行われた際の処理を行う関数
def rightclick_button(row, col, event):
    if button_state[row][col] and buttons[row][col]["text"] == "":
        flag_cell(row, col)
    elif buttons[row][col]["text"] == "F":
        unflag_cell(row, col)
    elif buttons[row][col]["text"] == "?":
        unmark_cell(row, col)

# ゲームを開始する関数
def start_game():
    global root, rows, cols, num_mines, board, buttons, button_state, game_over, put_color, restart_button, flags

    # 初期設定
    rows = 5
    cols = 5
    num_mines = 5
    game_over = False
    put_color = "#AAAAAA"
    flags = 0

    # 前回のフレームを削除
    for widget in root.winfo_children():
        widget.destroy()

    # ゲームの初期化
    board = create_board(rows, cols, num_mines)
    button_state = [[True for _ in range(cols)] for _ in range(rows)]

    # restart用ボタンと地雷の数を表示するフレームを作成
    control_frame = tk.Frame(root)
    control_frame.pack()

    restart_button = tk.Button(control_frame, text="やり直す", command=start_game)
    restart_button.pack()

    mines_label = tk.Label(control_frame, text="地雷: " + str(num_mines))
    mines_label.pack()

    # マスを設置するフレームを作成
    board_frame = tk.Frame(root)
    board_frame.pack()

    buttons = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            buttons[i][j] = tk.Button(board_frame, text="", width=5, height=2)
            buttons[i][j].bind("<Button-1>", lambda e, i = i, j = j: leftclick_button(i, j, e))
            buttons[i][j].bind("<Button-3>", lambda e, i = i, j = j: rightclick_button(i, j, e))
            buttons[i][j].grid(row=i, column=j)

    update_buttons()

# メイン関数
def main():
    global root

    root = tk.Tk()
    root.title("マインスイーパ")
    
    start_game()

    root.mainloop()

# スクリプトが直接実行された場合にメイン関数を実行
if __name__ == '__main__':
    main()
