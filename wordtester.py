import pygame as pg
import os
import json
import random as ran

data_file = "words.json"

class word_test:
  def __init__(self, data_file):
    # 初期化
    pg.init()

    # サイズ
    pg.display.set_caption("単語テスト")
    self.disp_w, self.disp_h = 800, 700
    self.screen = pg.display.set_mode((self.disp_w, self.disp_h))

    # 背景
    self.bg_color = (30, 30, 30)

    # フォント
    self.font_path = "fonts/NotoSansJP-VariableFont_wght.ttf"
    self.font = pg.font.Font(self.font_path, 30)
    self.font_color = (255, 255, 255)

    self.data_file = data_file

    self.word_dict = {}

    # エラーメッセージ用
    self.error_mes = "このファイルは適していません"
    self.error_disp = self.font.render(self.error_mes, True, self.font_color)

    self.load_word(self.data_file)

  def load_word(self, data_file):
    if os.path.exists(data_file):
      with open(data_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        if isinstance(data, dict):
          self.word_dict.update(data)
        else:
          self.screen.blit(
              self.error_disp, (self.disp_w // 2, self.disp_h // 2))

  def run_test(self):
    if not self.word_dict:
      print("単語リストが空です。単語を追加してください。")
      return

    running = True
    clock = pg.time.Clock()
    questions = ran.sample(list(self.word_dict.items()),
                           min(10, len(self.word_dict)))
    point = 0
    incorrect_ques = []

    for word, meaning in questions:
      # 問題ごとにランダムにテストタイプを選択
      test_type = ran.choice(['spelling', 'meaning'])

      user_input = ""
      answered = False
      options = []

      if test_type == 'meaning':
        options = ran.sample(list(self.word_dict.values()), 3)
        if meaning not in options:
          options[0] = meaning
        ran.shuffle(options)

      while running:
        self.screen.fill(self.bg_color)

        # イベント処理
        for event in pg.event.get():
          if event.type == pg.QUIT:
            running = False
          elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
              answered = True
            elif event.key == pg.K_BACKSPACE:
              user_input = user_input[:-1]
            elif event.unicode.isprintable():
              user_input += event.unicode

        word_disp = self.font.render(word, True, self.font_color)

        if test_type == 'spelling':
          # スペルのテスト
          text = self.font.render(f"スペルを入力: {meaning}", True, self.font_color)
          answer_check = user_input.lower() == word.lower()
          input_text = self.font.render(user_input, True, self.font_color)
          text_rect = text.get_rect(center=(self.disp_w // 2, self.disp_h // 3))
        else:
          text = self.font.render(
              f"{word} の意味を選択してください ", True, self.font_color)
          text_rect = text.get_rect(center=(self.disp_w // 2, self.disp_h // 3))
          for idx, opt in enumerate(options):
            option_text = self.font.render(
                f"{idx + 1}. {opt}", True, self.font_color)
            self.screen.blit(option_text, ((
                self.disp_w - 2 * word_disp.get_width()) // 2, self.disp_h // 2 + idx * 40))
          input_text = self.font.render(user_input, True, self.bg_color)

          if len(user_input) == 1 and user_input.isdigit():
            choice = int(user_input) - 1
            if 0 <= choice < len(options):
              answer_check = options[choice] == meaning

        self.screen.blit(text, text_rect)
        self.screen.blit(
            input_text, ((self.disp_w - word_disp.get_width()) // 2, self.disp_h // 2))
        pg.display.flip()

        if answered:
          input_text = ""
          if answer_check:
            point += 1

          else:
            incorrect_ques.append((word, meaning))
          break
    # 結果を表示
    self.screen.fill(self.bg_color)
    result_point = self.font.render(
        f"全問終了！あなたの得点は {point}/{len(questions)} 点です", True, self.font_color)
    result_point_rect = result_point.get_rect(
        center=(self.disp_w // 2, self.disp_h // 3))
    self.screen.blit(result_point, result_point_rect)

    if incorrect_ques:
      incorrect = self.font.render("間違えた問題:", True, self.font_color)
      incorrect_rect = incorrect.get_rect(
          center=(self.disp_w // 2, self.disp_h // 2))
      self.screen.blit(incorrect, incorrect_rect)
      for idx, (word, meaning) in enumerate(incorrect_ques):
        incorrect_no = self.font.render(
            f"{idx + 1}. {word}: {meaning}", True, self.font_color)
        incorrect_no_rect = incorrect_no.get_rect(
            center=(self.disp_w // 2, (self.disp_h // 2 + (idx + 1) * 40)))
        self.screen.blit(incorrect_no, incorrect_no_rect)

    pg.display.flip()

    # ユーザーがウィンドウを閉じるかキーを押すのを待つ
    waiting = True
    while waiting:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          waiting = False
        elif event.type == pg.KEYDOWN:
          waiting = False

      clock.tick(30)
    pg.quit()

if __name__ == "__main__":
  word_tester = word_test("words.json")
  word_tester.run_test()
