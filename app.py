from flask import Flask, render_template, request
from analyzer import analyze_palm  # 손금 분석 함수

app = Flask(__name__)

# 루트 페이지
@app.route('/')
def index():
    return render_template('palm_reading.html')

# 분석 엔드포인트
@app.route('/analyze_scores', methods=['POST'])
def analyze_scores():
    if 'image' not in request.files:
        return "No file uploaded", 400
    file = request.files['image']
    
    # analyzer.py에서 이미지 처리
    result = analyze_palm(file)
    
    # HTML, JSON, 문자열 등 반환 가능
    return result

# Render 환경 포트 반영
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


