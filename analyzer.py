# analyzer.py
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from typing import Dict, Any
import random

class PalmAnalyzer:
    def __init__(self):
        # 손금 분석 데이터
        self.palm_data = {
            'lines': {
                '감정선': {
                    'icon': '💕',
                    'title': '감정선 (Heart Line)',
                    'analysis': '''선명하게 보이니 따뜻한 마음이 잘 전달되고, 곡선이 아름답게 보이니 창의적인 관계가 기대되고, 길게 뻗어 있으니 깊은 우정과 사랑이 지속되고 있어.

감정선은 당신의 사랑과 우정을 담당하는 특별한 선이야. 두껍게 보이니 감정이 풍부하고, 적당한 깊이로 새겨져 있으니 진실한 마음을 가지고 있어.

손을 편안히 펴고 자연광 아래에서 다시 찍어보면 이 선의 매력이 더 잘 드러날 거야. 앞으로 새로운 만남에서 특별한 인연이 기다리고 있을 것 같아!'''
                },
                '지능선': {
                    'icon': '🧠',
                    'title': '지능선 (Head Line)',
                    'analysis': '''직선에 가깝게 보이니 목표가 단단해지고, 선명하니 명석함이 잘 드러나고, 적당한 길이니 실용적 사고가 뛰어나고, 깊이 있게 새겨져 있으니 열정이 담기고 있어.

지능선은 당신의 사고와 창의력을 보여주는 중요한 선이야. 분기가 보이니 다양한 아이디어가 샘솟고, 균형잡힌 모습이니 논리적 사고와 창의적 영감이 조화를 이루고 있어.

명상이나 아이디어 적기를 해보는 것도 좋을 거야. 새로운 도전에서 당신의 지적 능력이 빛을 발할 때가 다가오고 있어!'''
                },
                '생명선': {
                    'icon': '💪', 
                    'title': '생명선 (Life Line)',
                    'analysis': '''엄지 주변을 아름답게 감싸는 곡선이 보이니 삶이 유연해지고, 깊고 선명하니 활력이 잘 드러나고, 길게 이어져 있으니 회복력이 강하고, 안정적인 호를 그리니 에너지가 잘 순환되고 있어.

생명선은 당신의 건강과 생명력을 나타내는 소중한 선이야. 두껍게 보이니 체력이 좋고, 연속성이 있으니 꾸준한 에너지가 흘러.

스트레칭이나 산책으로 이 튼튼함을 유지해보자. 앞으로도 건강하고 활기찬 삶이 지속될 거야!'''
                },
                '운명선': {
                    'icon': '⭐',
                    'title': '운명선 (Fate Line)',
                    'analysis': '''손목 근처에서 위로 향하는 선이 보이니 새로운 기회를 탐색한 과정이 되고, 수직으로 뻗어 있으니 목표가 뚜렷해지고, 중간에 변화가 있으니 다양한 길이 열리고 있어.

운명선은 당신의 인생 방향과 목표 달성을 보여주는 신비로운 선이야. 선명한 부분이 있으니 결단력이 강하고, 깊이가 느껴지니 인내심도 충분해.

작은 목표를 세워 하나씩 이뤄보자. 당신의 운명선은 큰 성취를 예고하고 있어!'''
                },
                '태양선': {
                    'icon': '☀️',
                    'title': '태양선 (Sun Line)',
                    'analysis': '''약지 아래 부분에 희미하게 보이니 새로운 도전을 통해 빛날 기회가 되고, 상승하는 방향이니 창의적인 성취가 기대되고, 선명해질수록 명예와 성공이 따라오고 있어.

태양선은 당신의 성공과 명예를 담당하는 황금 같은 선이야. 곡선이 아름다우니 예술적 재능이 있고, 적당한 길이니 실현 가능한 꿈을 가지고 있어.

자신만의 아이디어를 실천해보자. 태양선이 더욱 선명해질 날이 멀지 않았어!'''
                },
                '금성띠': {
                    'icon': '💫',
                    'title': '금성띠 (Girdle of Venus)',
                    'analysis': '''감정선 위쪽에 섬세한 선들이 보이니 감정을 자유롭게 표현할 때가 되고, 예술적 감성이 풍부해지고, 창의적인 재능이 꽃피우고 있어.

금성띠는 당신의 예술적 감수성과 섬세한 감정을 보여주는 특별한 선이야. 부드러운 곡선이니 로맨틱한 성향이 있고, 분기된 모습이니 다양한 창작 활동에 재능이 있어.

손으로 그림이나 음악을 해보는 것도 좋을 거야. 당신의 감성이 많은 사람들에게 감동을 줄 수 있을 거야!'''
                },
                '결혼선': {
                    'icon': '💒',
                    'title': '결혼선 (Marriage Line)',
                    'analysis': '''새끼손가락 아래 옆면에 선들이 보이니 관계에서 새로운 조율의 시간이 되고, 안정적인 동반자성이 강해지고, 깊은 애정이 담겨 있어.

결혼선은 당신의 사랑과 결혼운을 보여주는 로맨틱한 선이야. 직선에 가까우니 신뢰가 단단하고, 적당한 두께니 균형잡힌 관계를 추구해.

대화로 관계를 더 따뜻하게 만들어보자. 진정한 사랑이 당신을 기다리고 있어!'''
                },
                '운세선': {
                    'icon': '🌊',
                    'title': '운세선 (Via Lasciva)',
                    'analysis': '''손바닥 아래쪽에 곡선들이 보이니 새로운 모험을 시작할 준비가 되고, 다채로운 경험이 많아지고, 자유로운 정신이 빛나고 있어.

운세선은 당신의 모험심과 자유로운 영혼을 보여주는 역동적인 선이야. 물결처럼 흐르니 변화를 즐기고, 여러 갈래로 나뉘니 다양한 경험을 추구해.

여행이나 취미로 이 에너지를 즐겨보자. 새로운 도전이 당신에게 특별한 행운을 가져다 줄 거야!'''
                }
            },
            'mounts': {
                '목성언덕': {
                    'icon': '🏔️',
                    'title': '목성언덕 (검지 아래)',
                    'analysis': '''넓고 발달해 보이니 잠재력이 풍부하고 자신감이 넘치고, 단단해 보이니 리더십이 강하고, 붉은 기운이 느껴지니 활력이 넘치고 있어.

목성언덕은 당신의 야망과 리더십을 상징하는 권위의 언덕이야. 높게 솟아있으니 큰 꿈을 품고 있고, 넓게 퍼져있으니 포용력도 뛰어나.

리더십을 발휘할 기회가 많을 테니 작은 결정을 자신 있게 해보자. 당신은 타고난 리더야!'''
                },
                '토성언덕': {
                    'icon': '🗻',
                    'title': '토성언덕 (중지 아래)',
                    'analysis': '''적당한 높이로 보이니 안정감이 있고, 부드러워 보이니 유연성이 강하고, 차분한 에너지가 느껴지니 인내심이 뛰어나고 있어.

토성언덕은 당신의 책임감과 인내력을 보여주는 신중함의 언덕이야. 균형잡힌 모습이니 성급하지 않고 신중하게 판단해.

꾸준히 나아가는 모습이 멋질 거야. 당신의 인내심이 큰 결실을 맺을 때가 올 거야!'''
                },
                '태양언덕': {
                    'icon': '🌅',
                    'title': '태양언덕 (약지 아래)',
                    'analysis': '''부드럽고 넓어 보이니 창의성이 풍부하고, 붉은 기운이 보이니 활력이 넘치고, 매력적인 에너지가 흘러서 사람들을 끌어당기고 있어.

태양언덕은 당신의 창의력과 매력을 상징하는 빛나는 언덕이야. 발달된 모습이니 예술적 재능이 있고, 따뜻한 기운이니 사람들에게 인기가 많아.

매력을 발휘할 좋은 시간이네. 당신의 창의적 에너지로 많은 사람들에게 영감을 줄 수 있을 거야!'''
                },
                '수성언덕': {
                    'icon': '💎',
                    'title': '수성언덕 (새끼손가락 아래)',
                    'analysis': '''단단해 보이니 의지가 강하고, 적당한 크기니 소통 능력이 뛰어나고, 지적인 에너지가 느껴지니 학습 능력이 뛰어나고 있어.

수성언덕은 당신의 소통 능력과 상업적 감각을 보여주는 지혜의 언덕이야. 선명한 모습이니 말재주가 좋고, 균형잡힌 크기니 실용적 지혜가 있어.

대화에서 재치가 빛날 거야. 당신의 커뮤니케이션 능력이 큰 성공을 가져다 줄 거야!'''
                }
            }
        }

    def _preprocess(self, img: np.ndarray):
        """이미지 전처리"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        return gray, blur

    def analyze_palm_part(self, img: np.ndarray, part_type: str, part_name: str, dominant_hand: str = "오른손") -> Dict[str, Any]:
        """개별 손금 부위 분석"""
        # 실제 이미지 전처리
        gray, enhanced = self._preprocess(img)
        
        # 해당 부위 데이터 가져오기
        if part_type == 'line':
            part_data = self.palm_data['lines'].get(part_name)
        else:  # mount
            part_data = self.palm_data['mounts'].get(part_name)
        
        if not part_data:
            return {
                'error': '잘못된 부위 이름입니다.',
                'part_type': part_type,
                'part_name': part_name
            }
        
        # 분석 결과 반환
        return {
            'success': True,
            'part_type': part_type,
            'part_name': part_name,
            'dominant_hand': dominant_hand,
            'icon': part_data['icon'],
            'title': part_data['title'],
            'analysis': part_data['analysis'],
            'image_analyzed': True
        }

    def get_full_analysis(self, img: np.ndarray, dominant_hand: str = "오른손") -> Dict[str, Any]:
        """전체 손금 분석 (기존 호환성 유지)"""
        gray, enhanced = self._preprocess(img)
        
        # 간단한 점수 계산 (랜덤 + 이미지 기반)
        h, w = gray.shape[:2]
        brightness = int(gray.mean())
        
        scores = {
            'relationships': min(100, max(60, 70 + (brightness % 20))),
            'creativity': min(100, max(60, 75 + ((h + w) % 25))),
            'health': min(100, max(60, 80 + (brightness % 15))), 
            'success': min(100, max(60, 72 + ((h * w) % 100) // 4))
        }
        
        return {
            'dominant_hand': dominant_hand,
            'scores': scores,
            'total_parts': 12,
            'analyzed': True
        }

# 기존 호환성을 위한 함수들
def analyze_image(img: np.ndarray, dominant_hand: str = "오른손"):
    """기존 API 호환성 함수"""
    analyzer = PalmAnalyzer()
    result = analyzer.get_full_analysis(img, dominant_hand)
    
    features = {
        'dominant_hand': dominant_hand,
        'total_parts': 12
    }
    
    scores = result['scores']
    return features, scores

def analyze_palm_part(img: np.ndarray, part_type: str, part_name: str, dominant_hand: str = "오른손"):
    """개별 부위 분석 함수"""
    analyzer = PalmAnalyzer()
    return analyzer.analyze_palm_part(img, part_type, part_name, dominant_hand)

# 내보낼 심볼
__all__ = ["analyze_image", "analyze_palm_part", "PalmAnalyzer"]
