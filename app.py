from flask import Flask, render_template

app = Flask(__name__)

# 루트 경로 처리
@app.route('/')
def index():
    return render_template('palm_reading.html')

# Render 환경 포트 반영
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
