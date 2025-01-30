from flask import Flask, request, send_from_directory
import pyautogui
import subprocess
import win32gui
import win32con
import pygetwindow as gw
from pywinauto.application import Application
import pyperclip


app = Flask(__name__)

# PCの画面サイズを取得
screen_width, screen_height = pyautogui.size()

@app.route('/')
def index():
    return send_from_directory('.', 'remote_control.html')

@app.route('/move_mouse', methods=['POST'])
def move_mouse():
    data = request.json
    # iPhoneから送信された移動量を取得
    dx = data['dx']
    dy = data['dy']
    
    # 現在のマウス位置を取得
    current_x, current_y = pyautogui.position()
    
    # 新しいマウス位置を計算
    new_x = current_x + int(dx)
    new_y = current_y + int(dy)
    
    # マウスカーソルがスクリーンの範囲内に収まるように調整
    new_x = max(0, min(new_x, screen_width - 1))
    new_y = max(0, min(new_y, screen_height - 1))
    
    if new_x <= 0 or new_x >= screen_width:
        new_x = current_x
    if new_y <= 0 or new_y >= screen_height:
        new_y = current_y
    # マウスカーソルを移動
    pyautogui.moveTo(new_x, new_y)
    return 'Mouse moved', 200

@app.route('/press_key', methods=['POST'])
def press_key():
    key = request.form['key']
    if key == 'click':
        pyautogui.click()
    elif key == 'netflix':
        # Netflixアプリを起動するコマンド
        # subprocess.Popen(['start', 'shell:AppsFolder\\4DF9E0F8.Netflix_mcm4njqhnhss8'], shell=True)
        # Google Chromeのウィンドウを取得
        chrome_window = gw.getWindowsWithTitle('Netflix')[0]

        # Google Chromeを最前面に持ってくる
        app = Application().connect(handle=chrome_window._hWnd)
        app.top_window().set_focus()
        pyautogui.hotkey('win', 'up')
    elif key == 'up':
        pyautogui.press('up')
    elif key == 'down':
        pyautogui.press('down')
    elif key == 'youtube':
        # ChromeでインストールされたYouTubeアプリのウィンドウを取得
        # youtube_window = gw.getWindowsWithTitle('YouTube - Google Chrome')[0]
        # 現在開いているすべてのウィンドウのタイトルを取得
        windows = gw.getAllTitles()

        # 'YouTube'を含むウィンドウタイトルのリストを作成
        youtube_title = [title for title in windows if title.startswith('YouTube')][0]
        # Google Chromeを最前面に持ってくる
        youtube_window = gw.getWindowsWithTitle(youtube_title)[0]
        app = Application().connect(handle=youtube_window._hWnd)
        
        app.top_window().set_focus()
        pyautogui.hotkey('win', 'up')
    elif key == 'back':
        # 特定のアプリを最前面に持ってくる処理を追加
        pyautogui.hotkey('altleft', 'left')
    return 'Key pressed', 200

def bring_window_to_foreground(window_name):
    def enum_windows_callback(hwnd, window_name):
        if win32gui.IsWindowVisible(hwnd) and window_name in win32gui.GetWindowText(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return False
        return True
    
    win32gui.EnumWindows(enum_windows_callback, window_name)

@app.route('/send_text', methods=['POST'])
def send_text():
    text = request.form['text']
    # テキストを入力する処理を実行
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    return 'Text sent', 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
