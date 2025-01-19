import tkinter as tk
from tkinter import messagebox
import json
import os

# データファイルのパス
data_file = "words.json"

class word_add:
  # 初期単語データをファイルから読み込む
  def __init__(self):
    self.word_list = self.load_words()
  # jsonファイルから読み取り

  def load_words(self):
    if os.path.exists(data_file):
      with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)
    return {}

  # jsonファイルに保存
  def save_words(self):
    with open(data_file, "w", encoding="utf-8") as file:
      json.dump(self.word_list, file, ensure_ascii=False, indent=4)

  # 単語を追加
  def add_word(self):
    word = self.word_entry.get()
    meaning = self.meaning_entry.get()

    if word and meaning:
      # 入力した単語がなかったら追加
      if word not in self.word_list:
        self.word_list[word] = meaning
        self.update_word_listbox()
        self.word_entry.delete(0, tk.END)
        self.meaning_entry.delete(0, tk.END)
        messagebox.showinfo("追加完了", f"単語 '{word}' がリストに追加されました。")
      else:
        messagebox.showwarning("エラー", "この単語はすでに存在します。")
    # 記入漏れ防止
    else:
      messagebox.showwarning("入力エラー", "単語と意味を両方入力してください。")

# 単語を削除
  def delete_word(self):
    selected_index = self.word_listbox.curselection()
    if selected_index:
      selected_word = self.word_listbox.get(
          selected_index).split(":")[0].strip()
      if selected_word in self.word_list:
        del self.word_list[selected_word]
        self.update_word_listbox()
        messagebox.showinfo("削除完了", f"単語 '{selected_word}' がリストから削除されました。")
    else:
      messagebox.showwarning("削除エラー", "削除する単語を選択してください。")

  # リスト欄の更新
  def update_word_listbox(self):
    self.word_listbox.delete(0, tk.END)
    for word, meaning in self.word_list.items():
      self.word_listbox.insert(tk.END, f"{word}: {meaning}")

  # 単語データを保存
  def save_list(self):
    self.save_words()
    self.root.destroy()

  # メインウィンドウ設定
  def run(self):
    self.root = tk.Tk()
    self.root.title("単語リスト")

    # 入力フォーム
    frame = tk.Frame(self.root)
    frame.pack(padx=10, pady=10)

    # 単語入力欄の設定
    tk.Label(frame, text="単語").grid(row=0, column=0, padx=5, pady=5)
    self.word_entry = tk.Entry(frame)
    self.word_entry.grid(row=0, column=1, padx=5, pady=5)

    # 意味入力欄の設定
    tk.Label(frame, text="意味").grid(row=1, column=0, padx=5, pady=5)
    self.meaning_entry = tk.Entry(frame)
    self.meaning_entry.grid(row=1, column=1, padx=5, pady=5)

    # 追加ボタン
    add_button = tk.Button(frame, text="追加", command=self.add_word)
    add_button.grid(row=2, column=0, pady=10)

    # 削除ボタン
    delete_button = tk.Button(frame, text="削除", command=self.delete_word)
    delete_button.grid(row=2, column=1, pady=10)

    # 単語リスト表示
    self.word_listbox = tk.Listbox(self.root, width=50)
    self.word_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # リスト欄を更新
    self.update_word_listbox()

    # ウィンドウが閉じられるときにデータを保存
    self.root.protocol("WM_DELETE_WINDOW", self.save_list)

    # Tkinterメインループ開始
    self.root.mainloop()

if __name__ == "__main__":
  app = word_add()
  app.run()
