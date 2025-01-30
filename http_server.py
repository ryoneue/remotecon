from flask import Flask, request, send_from_directory
import pyautogui

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
    if new_x >= screen_width or new_x <= 0:
        new_x = current_x
    
    if new_y >= screen_width or new_y <= 0:
        new_y = current_y
    
    # マウスカーソルを移動
    pyautogui.moveTo(new_x, new_y)
    return 'Mouse moved', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
