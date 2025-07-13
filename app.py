from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import csv
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

ADMIN_PASSWORD = "1234"  # 관리자 비밀번호
CSV_FILE = "coupon_records.csv"

# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")

# 쿠폰 지급
@app.route("/issue", methods=["GET", "POST"])
def issue():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        quantity = request.form.get("quantity", "").strip()
        admin_pw = request.form.get("admin_password", "").strip()

        if admin_pw != ADMIN_PASSWORD:
            flash("관리자 비밀번호가 틀렸습니다!")
            return redirect(url_for("issue"))

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = [name, "지급", quantity, now]
        save_record(record)
        flash(f"{name}님에게 쿠폰 {quantity}장 지급 완료!")
        return redirect(url_for("index"))

    return render_template("issue.html")

# 쿠폰 사용
@app.route("/use", methods=["GET", "POST"])
def use():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        quantity = request.form.get("quantity", "").strip()
        admin_pw = request.form.get("admin_password", "").strip()

        if admin_pw != ADMIN_PASSWORD:
            flash("관리자 비밀번호가 틀렸습니다!")
            return redirect(url_for("use"))

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = [name, "사용", quantity, now]
        save_record(record)
        flash(f"{name}님이 쿠폰 {quantity}장 사용했습니다!")
        return redirect(url_for("index"))

    return render_template("use.html")

# 기록 저장 함수
def save_record(data):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["이름", "기록종류", "수량", "시간"])
        writer.writerow(data)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

