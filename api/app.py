from flask import Flask, request, jsonify, send_file
from pathlib import Path
import json, os

app = Flask(__name__)

DATA_PATH = Path("/app/data/expenses.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]", encoding="utf-8")

@app.get("/healthz")
def healthz():
    return "ok", 200

# 아래 엔드포인트들을 구현하세요. ( 함수명은 임의로 지정한 내용임 )
@app.get("/api/records")
def get_records():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    return jsonify(records)

@app.post("/api/records")
def add_record():
    data = request.get_json()
    title = data.get("title")
    amount = data.get("amount")
    date = data.get("date")

    # 간단 유효성 검사
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Invalid title"}), 400
    if not (isinstance(amount, int) or isinstance(amount, float)) or amount < 0:
        return jsonify({"error": "Invalid amount"}), 400
    if not isinstance(date, str) or not date.strip():
        return jsonify({"error": "Invalid date"}), 400

    # 파일에서 기존 데이터 읽기
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    # 새 기록 추가
    records.append({"title": title, "amount": amount, "date": date})

    # 파일에 다시 저장
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "Record added"}), 201

@app.get("/api/summary")
def summary():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    count = len(records)
    total = sum(r.get("amount", 0) for r in records)
    return jsonify({"count": count, "total": total})

@app.get("/api/download")
def download_json():
    try:
        return send_file(
            str(DATA_PATH),
            mimetype="application/json",
            as_attachment=True,
            download_name="expenses.json"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 적절한 포트(예: 5000)로 0.0.0.0 에서 실행
    app.run(host="0.0.0.0", port=5000)