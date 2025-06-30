from flask import Flask, render_template, request, jsonify, json
from query import query_vector_store, create_vector_store
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
    botText = str(query_vector_store(userText))
    log_message(userText, botText)
    return botText

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
        create_vector_store(filename)
        return jsonify({'message': 'Upload successful'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

CHAT_LOG_FILE = 'log/' + datetime.datetime.now().strftime("%Y-%m-%dd") + '_log.json'


def log_message(user_msg, bot_msg):
    # 로그 항목 만들기
    new_entry = {
        "time" : datetime.datetime.now().strftime("%T"),
        "user": user_msg,
        "bot": bot_msg
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
        json.dump(chat_log, f, ensure_ascii=False, indent=2, sort_keys = False)

    return {'status': 'ok'}


if __name__ == '__main__':
#  app.run('0.0.0.0',port=5000,debug=True)
   app.run(debug = True)
   

'''
1. Read me 추가하기(사용된 기술 스택)
2. langchain 구현하기
3. 프론트엔드 가꾸기
4. rag 성능개선 고민해보기(pdf 파일 몇 개 추가하기)

'''