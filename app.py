from flask import Flask, request, render_template
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets 인증 및 시트 가져오기 함수
def get_sheet():
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file('coupon-service-account-8c6fbed94166', scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("coupon").sheet1
    return sheet

# 기록 저장 함수
def record_to_sheet(name, count, action):
    sheet = get_sheet()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([name, count, action, now])

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 쿠폰 발급 처리
@app.route('/issue', methods=['POST'])
def issue():
    name = request.form.get('name')
    count = request.form.get('count')
    if not name or not count:
        return "이름과 매수를 모두 입력해주세요", 400
    record_to_sheet(name, count, "발급")
    return f"{name}님에게 쿠폰 {count}장 발급 완료!"

# 쿠폰 사용 처리
@app.route('/use', methods=['POST'])
def use():
    name = request.form.get('name')
    count = request.form.get('count')
    if not name or not count:
        return "이름과 매수를 모두 입력해주세요", 400
    record_to_sheet(name, count, "사용")
    return f"{name}님이 쿠폰 {count}장 사용 처리 완료!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
