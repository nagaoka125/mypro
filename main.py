import pygame as pg
import threading
from add import word_add
from wordview import wordviewer
from wordtester import word_test

data_file = "words.json"

class mainapp:
  def __init__(self):
    # 初期化
    pg.init()

    # サイズ
    pg.display.set_caption("単語帳アプリ")
    self.disp_w, self.disp_h = 800, 700
    self.screen = pg.display.set_mode((self.disp_w, self.disp_h))

    # 背景
    self.bg_color = (30, 30, 30)

    # タイトル設定
    self.title = pg.font.Font(None, 70)
    self.title_color = (255, 255, 255)

    # メニュー設定
    self.menu = ["単語帳", "単語編集", "単語テスト"]
    self.menu_select = 0
    self.font_path = "fonts/NotoSansJP-VariableFont_wght.ttf"
    self.font = pg.font.Font(self.font_path, 48)
    self.font_color = (255, 255, 255)
    self.length = len(self.menu)
    text = self.font.render("", True, self.font_color)
    text_rect = text.get_rect(center=(0, 0))

  # ディスプレイ描画
  def set_disp(self):
    self.screen.fill(self.bg_color)
    for i, j in enumerate(self.menu):
      # メニュー選択時の色
      if i == self.menu_select:
        text_color = (200, 100, 50)
      else:
        text_color = self.font_color
      # メニューの位置
      title_text = self.font.render("単語帳アプリ", True, self.title_color)
      title_rect = title_text.get_rect(
          center=(self.disp_w // 2, self.disp_h // 4))
      text = self.font.render(j, True, text_color)
      text_rect = text.get_rect(
          center=(self.disp_w // 2, self.disp_h // self.length + i * 60))
      # 描画
      self.screen.blit(title_text, title_rect)
      self.screen.blit(text, text_rect)
    pg.display.flip()

  def run(self):
    global menu_select

    # 終了
    exit_flag = False
    while not exit_flag:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          exit_flag = True

        # メニュー選択
        if event.type == pg.KEYDOWN:
          # 上に移動
          if event.key == pg.K_UP:
            self.menu_select = (self.menu_select - 1) % len(self.menu)
            self.set_disp()
          # 下に移動
          elif event.key == pg.K_DOWN:
            self.menu_select = (self.menu_select + 1) % len(self.menu)
            self.set_disp()
          # enterで機能に移行
          elif event.key == pg.K_RETURN:
            # 単語帳を起動
            if self.menu_select == 0:
              viewer = wordviewer("words.json")
              viewer.run()
            # 単語編集を起動
            elif self.menu_select == 1:
              threading.Thread(target=self.add_app).start()
            # 単語テストを起動
            elif self.menu_select == 2:
              word_tester = word_test("words.json")
              word_tester.run_test()

      self.set_disp()

    pg.quit()

  def add_app(self):
    app = word_add()
    app.run()

if __name__ == "__main__":
  app = mainapp()
  app.run()
