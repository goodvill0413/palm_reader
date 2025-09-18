from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# 루트 페이지
@app.route('/')
def index():
    return render_template('palm_reading.html')

# 테스트용 간단한 엔드포인트
@app.route('/analyze_scores', methods=['POST'])
def analyze_scores():
    try:
        # analyzer import 시도
        from analyzer import analyze_image, analyze_palm_part
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'}), 400
        
        file = request.files['file']
        dominant_hand = request.form.get('dominant', '오른손')
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # 파일을 numpy 배열로 변환
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'success': False, 'message': 'Invalid image file'}), 400
        
        # 분석 실행
        features, scores = analyze_image(img, dominant_hand)
        
        return jsonify({
            'success': True,
            'dominant_hand': dominant_hand,
            'scores': scores,
            'features': features
        })
        
    except ImportError as e:
        return jsonify({'success': False, 'message': f'Import error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'Analysis error: {str(e)}'}), 500

# 개별 부위 분석 엔드포인트
@app.route('/analyze_part', methods=['POST'])
def analyze_part():
    try:
        from analyzer import analyze_palm_part
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        dominant_hand = request.form.get('dominant', '오른손')
        part_type = request.form.get('part_type')
        part_name = request.form.get('part_name')
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not part_type or not part_name:
            return jsonify({'success': False, 'error': 'Missing part information'}), 400
        
        # 파일을 numpy 배열로 변환
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'success': False, 'error': 'Invalid image file'}), 400
        
        # 개별 부위 분석 실행
        result = analyze_palm_part(img, part_type, part_name, dominant_hand)
        
        return jsonify(result)
        
    except ImportError as e:
        return jsonify({'success': False, 'error': f'Import error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'Analysis error: {str(e)}'}), 500

# Render 환경 포트 반영
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
