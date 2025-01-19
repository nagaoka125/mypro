import pygame as pg
import sys
import os
import json

data_file = "words.json"

class wordviewer:
  def __init__(self, datafile):
    # 初期化
    pg.init()

    # サイズ
    pg.display.set_caption("単語帳")
    self.disp_w, self.disp_h = 800, 700
    self.screen = pg.display.set_mode((self.disp_w, self.disp_h))

    # 背景
    self.bg_color = (30, 30, 30)

    # フォント
    self.font_path = "fonts/NotoSansJP-VariableFont_wght.ttf"
    self.font = pg.font.Font(self.font_path, 30)
    self.font_color = (255, 255, 255)

    self.data_file = data_file

    # 単語の辞書
    self.word_dict = {}

    # エラーメッセージ用
    self.error_mes = "このファイルは対応していません"
    self.error_disp = self.font.render(self.error_mes, True, self.font_color)

    self.load_word(self.data_file, self.word_dict)

    # 単語のリストを保持
    self.words = list(self.word_dict.keys())
    self.current_word_index = 0

  def load_word(self, data_file, terget_dict):
    if os.path.exists(data_file):
      with open(data_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        if isinstance(data, dict):
          terget_dict.update(data)
        else:
          self.screen.blit(
              self.error_disp, (self.disp_w // 2, self.disp_h // 2))

  def run(self):
    while True:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          pg.quit()
          sys.exit()
        elif event.type == pg.KEYDOWN:
          # スペースキーで次の単語に進む
          if event.key == pg.K_SPACE:
            self.current_word_index = (
                self.current_word_index + 1) % len(self.words)

      # 描画
      self.screen.fill(self.bg_color)

      # 現在の単語と意味を描画
      current_word = self.words[self.current_word_index]
      current_meaning = self.word_dict[current_word]

      word_disp = self.font.render(current_word, True, self.font_color)
      meaning_disp = self.font.render(current_meaning, True, self.font_color)

      # 単語をウィンドウの中心に描画
      self.screen.blit(word_disp, ((self.disp_w -
                                    word_disp.get_width()) // 2, self.disp_h // 3))
      self.screen.blit(meaning_disp, ((self.disp_w -
                                       meaning_disp.get_width()) // 2, self.disp_h // 2))

      # ウィンドウの更新
      pg.display.flip()

if __name__ == "__main__":
  viewer = wordviewer("words.json")
  viewer.run()
