from flask import Flask, render_template, request, jsonify, json
from query import query_vector_store
from werkzeug.utils import secure_filename
import datetime 
import os

app = Flask(__name__)

app.config.update(
   UPLOAD_FOLDER = "doctrine"
)

@app.route('/')
def login():
   return render_template('index.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(query_vector_store(userText))

@app.route('/upload')
def upload():
    return render_template('upload.html')  # 팝업 전용 HTML

ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'Upload successful'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

CHAT_LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '_log.json'

@app.route('/log', methods=['POST'])
def log_message():
    data = request.get_json()
    user_message = data.get('user')
    bot_message = data.get('bot')

    # 로그 항목 만들기
    new_entry = {
        "time" : datetime.datetime.now().strftime("%T"),
        "user": user_message,
        "bot": bot_message
    }

    # 기존 로그 파일 읽기 (없으면 빈 리스트)
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, 'r', encoding='utf-8') as f:
            chat_log = json.load(f)
    else:
        chat_log = []

    # 새 항목 추가
    chat_log.append(new_entry)

    # 다시 저장
    with open(CHAT_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(chat_log, f, ensure_ascii=False, indent=2)

    return {'status': 'ok'}


if __name__ == '__main__':
   #app.run('0.0.0.0',port=5000,debug=True)
   app.run(debug = True)