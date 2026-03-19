from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib
import tkinter as tk
import csv

matplotlib.rcParams['font.family'] = 'MS Gothic'
students = []
ranking_mode = False

def add_student():
    name = entry_name.get()

    try:
        score = int(entry_score.get())
    except:
        label_result.config(text="点数は数字で入力してください")
        return

    if score < 0 or score > 100:
        label_result.config(text="点数は0～100で入力してください")
        return

    if name == "":
        label_result.config(text="名前を入力してください")
        return
    
    data = name + ":" + str(score)
    listbox.insert(tk.END, data)

    students.append((name, score))

    save_data()

    label_result.config(text=f"{name} を追加しました")

    entry_name.delete(0, tk.END)
    entry_score.delete(0, tk.END)

    update_count()

def delete_student():

    global ranking_mode

    if ranking_mode:
        label_result.config(text="ランキング表示中は削除できません")
        return

    result = messagebox.askyesno("確認", "本当に削除しますか?")

    if not result:
        return

    selected = listbox.curselection()

    if not selected:
        label_result.config(text="削除するデータを選択してください")
        return

    index = selected[0]

    listbox.delete(index)

    name, score = students[index]
    students.remove((name, score))

    save_data()

    update_count()

def update_count():
    count = len(students)
    count_label.config(text=f"登録人数: {count}")

def show_average():
    if len(students) == 0:
        label_result.config(text="データがありません")
        return

    total = 0
    for name, score in students:
        total += score
        
    avg = total / len(students)
    
    label_result.config(text=f"平均点：{avg:.1f}")

def save_data():
    with open("students.csv", "w", newline="") as f:
        writer = csv.writer(f)
        
        for name, score in students:
            writer.writerow([name, score])

def load_data():

    students.clear()
    listbox.delete(0, tk.END)

    try:
        with open("students.csv", "r") as f:
            reader = csv.reader(f)
            
            for row in reader:
                name = row[0]
                score = int(row[1])

                students.append((name, score))
                listbox.insert(tk.END, name + ":" + str(score))

    except FileNotFoundError:
        pass

def show_ranking():

    global ranking_mode

    if len(students) == 0:
        label_result.config(text="データがありません")
        return

    if ranking_mode:
        listbox.delete(0, tk.END)

        for name, score in students:
            listbox.insert(tk.END, f"{name}:{score}")

        ranking_mode = False
        return

    sorted_students = sorted(students, key=lambda x: x[1], reverse=True)

    listbox.delete(0, tk.END)

    listbox.insert(tk.END, "---ランキング---")

    rank = 1
    for name, score in sorted_students:
        listbox.insert(tk.END, f"{rank}位 {name} {score}点")
        rank += 1

    ranking_mode = True

def show_max_min():

    if len(students) == 0:
        label_result.config(text="データがありません")
        return

    max_student = max(students, key=lambda x: x[1])
    min_student = min(students, key=lambda x: x[1])

    label_result.config(
        text=f"最高点:{max_student[0]} {max_student[1]}点 / 最低点:{min_student[0]} {min_student[1]}点"
        )

def search_student():

    name = entry_name.get()

    if name == "":
        label_result.config(text="名前を入力してください")
        return

    found = False

    for student_name, score in students:
        if student_name == name:
            label_result.config(text=f"{student_name} の点数:{score}点")
            found = True
            break

    if not found:
        label_result.config(text="その名前は見つかりません")

def edit_score():

    selected = listbox.curselection()

    if not selected:
        label_result.config(text="編集するデータを選択してください")
        return

    try:
        new_score = int(entry_score.get())
    except:
        label_result.config(text="点数は数字で入力してください")
        return

    index = selected[0]
    name, old_score = students[index]

    students[index] = (name, new_score)

    save_data()

    listbox.delete(index)
    listbox.insert(index, f"{name}:{new_score}")

    label_result.config(text=f"{name} の点数を更新しました")

def select_data(event):

    if not listbox.curselection():
        return
    
    selected = listbox.get(listbox.curselection())

    if "ランキング" in selected or "---" in selected:
        return
    
    name, score = selected.split(":")

    entry_name.delete(0, tk.END)
    entry_name.insert(0, name)

    entry_score.delete(0, tk.END)
    entry_score.insert(0, score)

def sort_score():

    listbox.delete(0, tk.END)

    sorted_data = sorted(students.items(), key=lambda x: x[1], reverse=True)

    for name, score in sorted_data:
        listbox.insert(tk.END, f"{name} : {score}")

def show_graph():

    if len(students) == 0:
        label_result.config(text="データがありません")
        return

    names = []
    scores = []

    for name, score in students:
        names.append(name)
        scores.append(score)

    plt.bar(names, scores)

    avg = sum(scores) / len(scores)
    plt.axhline(avg, linestyle="--")

    plt.title("成績グラフ")
    plt.xlabel("名前")
    plt.ylabel("点数")

    plt.show()

def exit_app():
    save_data()
    root.destroy()

root = tk.Tk()

root.title("成績管理アプリ v1.0")

title = tk.Label(root, text="成績管理アプリ")
title.grid(row=0, column=0)

label_name = tk.Label(root, text="名前")
label_name.grid(row=1, column=0)

entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

label_score = tk.Label(root, text="点数")
label_score.grid(row=2, column=0)

entry_score = tk.Entry(root)
entry_score.grid(row=2, column=1)

button_add = tk.Button(root, text="データ追加", command=add_student)
button_add.grid(row=3, column=0)

button_search = tk.Button(root, text="名前検索", command=search_student)
button_search.grid(row=3, column=1)

label_result = tk.Label(root, text="")
label_result.grid(row=4, column=0)

listbox = tk.Listbox(root)
listbox.bind("<<ListboxSelect>>", select_data)
listbox.grid(row=5, column=0, columnspan=3)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=5, column=3, sticky="ns")

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

count_label = tk.Label(root, text="登録人数: 0")
count_label.grid(row=6, column=1)

button_avg = tk.Button(root, text="平均点", command=show_average)
button_avg.grid(row=7, column=0)

button_rank = tk.Button(root, text="ランキング", command=show_ranking)
button_rank.grid(row=7, column=1)

button_maxmin = tk.Button(root, text="最高・最低点", command=show_max_min)
button_maxmin.grid(row=7, column=2)

button_delete = tk.Button(root, text="データ削除", command=delete_student)
button_delete.grid(row=8, column=0)

button_edit = tk.Button(root, text="点数更新", command=edit_score)
button_edit.grid(row=8, column=1)

button_graph = tk.Button(root, text="グラフ表示", command=show_graph)
button_graph.grid(row=8, column=2)

sort_button = tk.Button(root, text="点数順ソート", command=sort_score)
sort_button.grid(row=9, column=0)

button_exit = tk.Button(root, text="終了", command=exit_app)
button_exit.grid(row=10, column=0)

load_data()

root.mainloop()
