# app.py
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from flask import Flask, request, jsonify, send_from_directory
from analyzer import analyze_image, analyze_palm_part, PalmAnalyzer

app = Flask(__name__)

@app.after_request
def add_cors(resp):
    """CORS 설정"""
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    return resp

@app.route("/", methods=["GET"])
def index():
    """메인 페이지 서빙"""
    return send_from_directory(".", "palm_reading.html")

@app.route("/analyze_scores", methods=["POST"])
def analyze_scores():
    """전체 점수 분석 (인터랙티브 UI용)"""
    try:
        f = request.files.get("file")
        dominant = request.form.get("dominant", "오른손")
        
        if not f:
            return jsonify({"error": "파일이 없습니다"}), 400

        # 이미지 디코딩
        file_bytes = np.frombuffer(f.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "이미지 디코딩에 실패했습니다"}), 400

        # 전체 분석 (점수만)
        analyzer = PalmAnalyzer()
        result = analyzer.get_full_analysis(img, dominant)
        
        return jsonify({
            "success": True,
            "dominant_hand": result['dominant_hand'],
            "scores": result['scores'],
            "message": "분석 완료! 궁금한 부위를 선택해주세요."
        })
        
    except Exception as e:
        return jsonify({"error": f"분석 중 오류 발생: {str(e)}"}), 500

@app.route("/analyze_part", methods=["POST"])
def analyze_part():
    """개별 부위 분석 (인터랙티브 UI용)"""
    try:
        f = request.files.get("file")
        dominant = request.form.get("dominant", "오른손")
        part_type = request.form.get("part_type")  # 'line' or 'mount'
        part_name = request.form.get("part_name")  # '감정선', '목성언덕' 등
        
        if not f:
            return jsonify({"error": "파일이 없습니다"}), 400
            
        if not part_type or not part_name:
            return jsonify({"error": "부위 정보가 없습니다"}), 400

        # 이미지 디코딩
        file_bytes = np.frombuffer(f.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "이미지 디코딩에 실패했습니다"}), 400

        # 개별 부위 분석
        result = analyze_palm_part(img, part_type, part_name, dominant)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"분석 중 오류 발생: {str(e)}"}), 500

@app.route("/get_palm_parts", methods=["GET"])
def get_palm_parts():
    """사용 가능한 손금 부위 목록 반환"""
    try:
        analyzer = PalmAnalyzer()
        
        lines = []
        for name, data in analyzer.palm_data['lines'].items():
            lines.append({
                'name': name,
                'icon': data['icon'],
                'title': data['title']
            })
        
        mounts = []
        for name, data in analyzer.palm_data['mounts'].items():
            mounts.append({
                'name': name,
                'icon': data['icon'],
                'title': data['title']
            })
        
        return jsonify({
            "success": True,
            "lines": lines,
            "mounts": mounts,
            "total_parts": len(lines) + len(mounts)
        })
        
    except Exception as e:
        return jsonify({"error": f"오류 발생: {str(e)}"}), 500

@app.route("/analyze_report", methods=["POST"])
def analyze_report():
    """기존 전체 분석 API (하위 호환성 유지)"""
    try:
        f = request.files.get("file")
        dominant = request.form.get("dominant", "오른손")
        
        if not f:
            return jsonify({"error": "파일이 없습니다"}), 400

        # 이미지 디코딩
        file_bytes = np.frombuffer(f.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "이미지 디코딩에 실패했습니다"}), 400

        # 기존 분석 방식
        features, scores = analyze_image(img, dominant_hand=dominant)
        
        # HTML 생성 (간단한 버전)
        report_html = f"""
        <div style="color:#ddd;font-family:sans-serif">
            <h2>🖐️ {dominant} 손금 분석 결과</h2>
            <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin:20px 0;">
                <div style="background:#1a1f2e;padding:20px;border-radius:10px;text-align:center;">
                    <h3 style="color:#4a9eff;">인간관계운</h3>
                    <div style="font-size:2em;color:#4a9eff;">{scores.get('relationships', 75)}</div>
                </div>
                <div style="background:#1a1f2e;padding:20px;border-radius:10px;text-align:center;">
                    <h3 style="color:#4a9eff;">창의력</h3>
                    <div style="font-size:2em;color:#4a9eff;">{scores.get('creativity', 78)}</div>
                </div>
                <div style="background:#1a1f2e;padding:20px;border-radius:10px;text-align:center;">
                    <h3 style="color:#4a9eff;">건강운</h3>
                    <div style="font-size:2em;color:#4a9eff;">{scores.get('health', 82)}</div>
                </div>
                <div style="background:#1a1f2e;padding:20px;border-radius:10px;text-align:center;">
                    <h3 style="color:#4a9eff;">성공운</h3>
                    <div style="font-size:2em;color:#4a9eff;">{scores.get('success', 79)}</div>
                </div>
            </div>
            <p style="margin-top:20px;color:#8ea1b3;">
                더 자세한 분석을 원하시면 개별 부위를 선택해서 확인해보세요!
            </p>
        </div>
        """
        
        return jsonify({
            "report_html": report_html,
            "detail_html": report_html,
            "scores": scores,
            "features": features
        })
        
    except Exception as e:
        return jsonify({"error": f"분석 중 오류 발생: {str(e)}"}), 500

if __name__ == "__main__":
    # 개발 서버 실행
    print("🖐️ 인터랙티브 손금 분석 서버 시작!")
    print("📍 http://localhost:5000 에서 접속 가능")
    print("📱 모바일에서는 http://[내IP]:5000 으로 접속")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
