from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'bingo_numbers.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS bingo_numbers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return '歡迎來到賓果號碼系統！'
    
@app.route('/api/clear_numbers', methods=['POST'])
def clear_numbers():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM bingo_numbers')  # bingo_numbers 是你的表名
            conn.commit()
            return jsonify({'status': 'success', 'message': '所有號碼已清除！'})
    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
        return jsonify({'status': 'error', 'message': '無法清除號碼'}), 500

@app.route('/input', methods=['GET'])
def input_page():
    return render_template('input.html')


@app.route('/display', methods=['GET'])
def display_page():
    return render_template('display.html')


@app.route('/api/add_number', methods=['POST'])
def add_number():
    data = request.get_json()
    number = data.get('number')
    if number is None or not isinstance(number, int):
        return jsonify({'status': 'error', 'message': '請輸入有效的號碼'}), 400

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO bingo_numbers (number) VALUES (?)', (number,))
            conn.commit()
        return jsonify({'status': 'success', 'message': f'號碼 {number} 已新增'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/get_numbers', methods=['GET'])
def get_numbers():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT number FROM bingo_numbers ORDER BY id ASC')
            numbers = [row[0] for row in c.fetchall()]
        return jsonify({'status': 'success', 'numbers': numbers})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)
