# analyzer.py
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple
import math

class PalmAnalyzer:
    def __init__(self):
        # 5가지 손금 유형별 분석 데이터
        self.line_type_analysis = {
            'thick_long': {
                '감정선': "선명하고 길게 뻗은 감정선이 풍부한 감정과 깊은 사랑의 능력을 보여줍니다. 한번 마음을 정하면 끝까지 헌신하는 타입으로, 진실하고 오래가는 관계를 추구합니다. 때로는 감정이 깊어 상처받기 쉽지만, 그만큼 타인에게 큰 위로와 사랑을 줄 수 있는 사람입니다. 마음을 열고 소통하는 것을 두려워하지 마세요.",
                
                '지능선': "굵고 긴 지능선은 강한 집중력과 지속적인 사고력을 나타냅니다. 한 가지 일에 몰두하면 놀라운 성과를 내는 타입으로, 깊이 있는 사고와 체계적인 접근을 선호합니다. 복잡한 문제도 차근차근 해결해나가는 능력이 뛰어나며, 학습 능력과 기억력이 우수합니다. 당신의 끈기와 집중력을 믿고 큰 목표에 도전해보세요.",
                
                '생명선': "뚜렷하고 긴 생명선은 강한 생명력과 회복력을 의미합니다. 체력이 좋고 스트레스에 대한 저항력이 강하며, 어려운 상황에서도 금세 회복하는 능력을 가지고 있습니다. 활동적이고 에너지가 넘치는 성격으로, 도전을 즐기고 역동적인 삶을 살아갑니다. 규칙적인 운동과 건강한 생활습관으로 이 에너지를 잘 관리하세요.",
                
                '운명선': "강하고 긴 운명선은 뚜렷한 목표 의식과 실행력을 보여줍니다. 자신만의 길을 개척하는 능력이 뛰어나며, 한번 결정한 일은 끝까지 해내는 의지력을 가지고 있습니다. 큰 성취를 이룰 가능성이 높으며, 리더십을 발휘할 기회도 많을 것입니다. 자신의 비전을 믿고 꾸준히 나아가면 훌륭한 결과를 얻을 수 있습니다.",
                
                '태양선': "선명한 태양선은 창의적 재능과 성공 가능성을 나타냅니다. 예술적 감각이 뛰어나고 남들과 다른 독창적인 아이디어를 가지고 있습니다. 사회적으로 인정받을 가능성이 높으며, 자신만의 분야에서 두각을 나타낼 것입니다. 창의력을 발휘할 수 있는 일을 찾아 도전해보세요.",
                
                '금성띠': "뚜렷한 금성띠는 풍부한 예술적 감수성과 로맨틱한 성향을 보여줍니다. 아름다운 것을 추구하고 감정 표현이 풍부하며, 창작 활동에 재능이 있습니다. 사랑에 대한 이상이 높고 감성적인 관계를 중시합니다. 예술이나 문화 활동을 통해 자신을 표현해보세요.",
                
                '결혼선': "깊고 긴 결혼선은 진지하고 안정적인 사랑을 추구함을 의미합니다. 결혼과 가정에 대한 책임감이 강하고, 파트너와의 깊은 유대감을 중시합니다. 한번 사랑하면 오래가는 관계를 만들어가며, 가족을 위해 헌신하는 타입입니다. 진실한 사랑이 당신을 기다리고 있습니다.",
                
                '운세선': "강한 운세선은 모험심과 도전 정신을 나타냅니다. 새로운 경험을 추구하고 변화를 두려워하지 않으며, 여행이나 탐험을 즐깁니다. 다양한 분야에서 경험을 쌓으며 폭넓은 시야를 가지게 될 것입니다. 새로운 도전을 통해 더 큰 성장을 이뤄보세요."
            },
            
            'thick_short': {
                '감정선': "굵고 짧은 감정선은 강렬하고 직접적인 감정 표현을 나타냅니다. 솔직하고 진실한 마음을 가지고 있으며, 가식 없는 순수한 사랑을 추구합니다. 감정의 변화가 빠르지만 그만큼 순간순간 진실합니다. 직관적이고 즉석에서 판단하는 능력이 뛰어나며, 자신의 감정에 솔직한 사람입니다.",
                
                '지능선': "굵고 짧은 지능선은 빠른 판단력과 실용적 사고를 의미합니다. 복잡한 이론보다는 실제적이고 즉시 적용 가능한 것을 선호하며, 핵심을 빠르게 파악하는 능력이 뛰어납니다. 효율성을 중시하고 불필요한 것은 과감히 제거하는 스타일입니다. 직관과 경험을 바탕으로 한 결정력이 강점입니다.",
                
                '생명선': "굵고 짧은 생명선은 강한 순간적 에너지와 집중력을 보여줍니다. 짧은 시간에 강한 힘을 발휘하며, 중요한 순간에 집중해서 큰 성과를 내는 타입입니다. 효율적으로 에너지를 사용하고, 필요할 때 폭발적인 활력을 보입니다. 적절한 휴식과 재충전으로 지속가능한 에너지를 관리하세요.",
                
                '운명선': "짧지만 굵은 운명선은 명확한 목표와 강한 실행력을 나타냅니다. 시간을 효율적으로 사용하며 핵심적인 성과를 내는 데 집중합니다. 불필요한 우회 없이 직접적으로 목표에 도달하려는 성향이 강하며, 단기간에 큰 변화를 만들어낼 수 있습니다. 집중력이 당신의 가장 큰 무기입니다.",
                
                '태양선': "짧고 굵은 태양선은 강렬한 개성과 독특함을 의미합니다. 남들과 다른 특별한 매력을 가지고 있으며, 강한 인상을 남기는 능력이 있습니다. 단기간에 주목받을 수 있는 재능을 가지고 있으며, 자신만의 독특한 방식으로 성공할 가능성이 높습니다. 개성을 살려 자신만의 길을 만들어가세요.",
                
                '금성띠': "굵고 짧은 금성띠는 강렬한 감성과 예술적 순간을 포착하는 능력을 보여줍니다. 짧지만 강한 영감과 창의적 아이디어가 번뜩이는 타입으로, 순간적인 직감이 뛰어납니다. 감정이 진솔하고 표현이 직접적이며, 진정성 있는 작품이나 관계를 만들어냅니다.",
                
                '결혼선': "짧고 굵은 결혼선은 진실하고 집중적인 사랑을 의미합니다. 연애할 때 온 마음을 다해 사랑하며, 진심어린 관계를 추구합니다. 가벼운 만남보다는 진지한 관계를 선호하고, 파트너에게 집중적인 관심과 사랑을 보여줍니다. quality over quantity의 사랑관을 가지고 있습니다.",
                
                '운세선': "굵고 짧은 운세선은 중요한 순간의 큰 변화를 나타냅니다. 인생의 터닝포인트에서 과감한 결정을 내리는 능력이 있으며, 짧은 시간에 큰 변화를 만들어내는 타입입니다. 기회를 놓치지 않는 순발력과 결단력이 뛰어나며, 인생의 중요한 순간들을 잘 활용할 것입니다."
            },
            
            'thin_long': {
                '감정선': "가늘고 긴 감정선은 섬세하고 지속적인 감정을 나타냅니다. 깊이 있는 감정을 오래 간직하며, 미묘한 감정의 변화도 민감하게 느끼는 타입입니다. 예술적 감수성이 뛰어나고 타인의 마음을 잘 이해하며, 세심한 배려와 따뜻한 마음을 가지고 있습니다. 당신의 섬세함이 많은 사람들에게 위로가 될 것입니다.",
                
                '지능선': "가늘고 긴 지능선은 세밀하고 지속적인 사고력을 의미합니다. 꼼꼼하고 치밀한 분석을 통해 문제를 해결하며, 세부사항까지 놓치지 않는 완벽주의적 성향이 있습니다. 학습 능력이 뛰어나고 기억력이 좋으며, 복잡한 정보도 체계적으로 정리하는 능력이 있습니다. 신중함과 정확성이 당신의 강점입니다.",
                
                '생명선': "가늘고 긴 생명선은 꾸준하고 지속적인 생명력을 보여줍니다. 급격한 변화보다는 안정적이고 규칙적인 생활을 통해 건강을 유지하는 타입입니다. 스트레스에 민감하지만 적절한 관리를 통해 장수할 수 있는 체질을 가지고 있습니다. 균형 잡힌 생활과 꾸준한 관리가 중요합니다.",
                
                '운명선': "가늘고 긴 운명선은 신중하고 지속적인 노력을 통한 성취를 나타냅니다. 급하게 결과를 얻으려 하지 않고 차근차근 단계를 밟아가며, 장기적인 계획을 세워 목표를 달성하는 타입입니다. 꾸준함과 인내심이 뛰어나며, 시간이 지날수록 더 큰 성과를 얻을 수 있습니다. 자신의 페이스를 유지하며 나아가세요.",
                
                '태양선': "가늘고 긴 태양선은 지속적인 창의력과 예술적 재능을 의미합니다. 세련되고 우아한 감각을 가지고 있으며, 시간이 지날수록 더욱 빛나는 재능을 발휘합니다. 꾸준한 노력을 통해 자신만의 독특한 스타일을 완성해나가며, 장기적으로 인정받을 가능성이 높습니다. 인내심을 가지고 자신의 재능을 키워나가세요.",
                
                '금성띠': "가늘고 긴 금성띠는 섬세한 예술적 감각과 로맨틱한 성향을 보여줍니다. 미적 감각이 뛰어나고 아름다운 것에 대한 안목이 있으며, 세련된 취향을 가지고 있습니다. 감정이 깊고 섬세하며, 예술이나 문화 활동을 통해 자신을 표현하는 것을 좋아합니다. 당신의 섬세한 감각을 살려보세요.",
                
                '결혼선': "가늘고 긴 결혼선은 신중하고 지속적인 사랑을 추구함을 의미합니다. 상대방을 깊이 이해하고 오래도록 함께하려는 마음이 강하며, 세심한 배려와 이해심이 뛰어납니다. 급하게 관계를 발전시키기보다는 천천히 마음을 나누며 깊은 유대감을 만들어갑니다. 진정한 사랑이 당신을 기다리고 있습니다.",
                
                '운세선': "가늘고 긴 운세선은 꾸준한 변화와 지속적인 성장을 나타냅니다. 갑작스러운 변화보다는 점진적이고 지속적인 발전을 추구하며, 새로운 경험을 통해 조금씩 성장해나갑니다. 인내심이 강하고 적응력이 뛰어나며, 시간이 지날수록 더 많은 가능성을 발견하게 될 것입니다."
            },
            
            'thin_short': {
                '감정선': "가늘고 짧은 감정선은 민감하고 순수한 감정을 나타냅니다. 마음이 여리고 감수성이 풍부하며, 작은 것에도 큰 감동을 받는 순수한 성격입니다. 변화에 민감하고 적응력이 뛰어나며, 새로운 환경에서도 빠르게 적응합니다. 당신의 순수함과 민감함이 주변 사람들에게 특별한 매력으로 다가갈 것입니다.",
                
                '지능선': "가늘고 짧은 지능선은 빠르고 유연한 사고력을 의미합니다. 직관적이고 창의적인 아이디어가 번뜩이며, 고정관념에 얽매이지 않는 자유로운 사고를 합니다. 복잡한 것보다는 simple하고 효과적인 해결책을 찾는 능력이 뛰어나며, 새로운 분야에 대한 호기심이 많습니다. 유연한 사고로 새로운 길을 개척해보세요.",
                
                '생명선': "가늘고 짧은 생명선은 민감하지만 적응력 있는 체질을 보여줍니다. 변화에 민감하지만 그만큼 환경에 잘 적응하며, 스트레스 관리와 자기 관리에 주의를 기울이면 건강하게 살 수 있습니다. 규칙적인 생활과 충분한 휴식이 중요하며, 자신만의 건강 관리법을 찾는 것이 도움이 될 것입니다.",
                
                '운명선': "가늘고 짧은 운명선은 유연하고 변화 지향적인 인생관을 나타냅니다. 하나의 길에 얽매이지 않고 다양한 가능성을 탐색하며, 변화하는 상황에 빠르게 적응하는 능력이 뛰어납니다. 여러 분야에서 경험을 쌓으며 자신만의 독특한 길을 만들어갈 것입니다. 변화를 두려워하지 말고 새로운 기회를 적극적으로 잡으세요.",
                
                '태양선': "가늘고 짧은 태양선은 순간적 영감과 독특한 창의력을 의미합니다. 번뜩이는 아이디어와 새로운 관점을 가지고 있으며, 예술적 감각이 뛰어납니다. 자유롭고 독창적인 표현을 좋아하며, 기존의 틀을 벗어난 새로운 것을 만들어내는 능력이 있습니다. 당신만의 독특한 재능을 발견해보세요.",
                
                '금성띠': "가늘고 짧은 금성띠는 섬세하고 변화하는 감성을 보여줍니다. 감정이 풍부하고 예술적 감각이 뛰어나며, 아름다운 것에 대한 순수한 감동을 느낍니다. 로맨틱하고 감성적인 성향이 있으며, 창작 활동을 통해 자신의 감정을 표현하는 것을 좋아합니다. 자유로운 감성 표현을 두려워하지 마세요.",
                
                '결혼선': "가늘고 짧은 결혼선은 순수하고 변화하는 사랑을 추구함을 의미합니다. 마음이 순수하고 로맨틱하며, 사랑에 대한 꿈과 이상이 높습니다. 상황에 따라 감정이 변할 수 있지만 그 순간순간은 진실합니다. 자유롭고 순수한 사랑을 통해 행복을 찾을 수 있을 것입니다.",
                
                '운세선': "가늘고 짧은 운세선은 빠른 변화와 새로운 기회에 대한 민감함을 나타냅니다. 새로운 환경이나 상황에 빠르게 적응하며, 변화하는 시대의 흐름을 잘 파악합니다. 다양한 경험을 통해 성장하며, 예상치 못한 기회를 통해 새로운 가능성을 발견할 것입니다. 열린 마음으로 변화를 받아들이세요."
            },
            
            'balanced': {
                '감정선': "균형 잡힌 감정선은 안정적이고 조화로운 감정을 나타냅니다. 감정의 기복이 적고 침착하게 상황을 판단하며, 타인과의 관계에서도 균형감각을 유지합니다. 너무 과하지도 부족하지도 않은 적절한 감정 표현을 하며, 주변 사람들에게 안정감을 주는 존재입니다. 당신의 균형 감각이 많은 사람들에게 도움이 될 것입니다.",
                
                '지능선': "균형 잡힌 지능선은 논리적 사고와 창의적 사고의 조화를 의미합니다. 체계적이면서도 유연한 사고를 하며, 상황에 따라 적절한 판단을 내리는 능력이 뛰어납니다. 분석력과 직감이 모두 발달되어 있어 다양한 분야에서 성과를 낼 수 있습니다. 균형 잡힌 사고로 현명한 결정을 내려나가세요.",
                
                '생명선': "균형 잡힌 생명선은 안정적인 건강과 적당한 활력을 보여줍니다. 무리하지 않으면서도 필요할 때는 에너지를 발휘할 수 있으며, 전반적으로 건강한 생활을 유지할 수 있는 체질입니다. 규칙적인 생활 습관으로 지속적인 건강을 유지할 수 있으며, 스트레스 관리도 잘 하는 편입니다.",
                
                '운명선': "균형 잡힌 운명선은 안정적이면서도 성장하는 인생을 나타냅니다. 급격한 변화보다는 꾸준한 발전을 추구하며, 계획적이고 단계적으로 목표를 달성해나갑니다. 위험을 감수하면서도 안정성을 놓치지 않는 현명함을 가지고 있으며, 장기적으로 큰 성취를 이룰 수 있습니다. 균형 잡힌 접근으로 성공을 향해 나아가세요.",
                
                '태양선': "균형 잡힌 태양선은 조화로운 창의력과 실용성을 의미합니다. 예술적 감각과 현실적 감각을 모두 가지고 있어 창의적이면서도 실현 가능한 아이디어를 만들어냅니다. 다양한 분야에서 재능을 발휘할 수 있으며, 꾸준한 노력을 통해 인정받을 수 있습니다. 당신의 조화로운 재능을 발휘해보세요.",
                
                '금성띠': "균형 잡힌 금성띠는 조화로운 감성과 예술적 감각을 보여줍니다. 아름다움을 추구하면서도 현실감각을 잃지 않으며, 품격 있고 세련된 취향을 가지고 있습니다. 감정 표현이 적절하고 품위가 있으며, 예술과 일상의 균형을 잘 맞춰나갑니다. 조화로운 아름다움을 추구해나가세요.",
                
                '결혼선': "균형 잡힌 결혼선은 안정적이고 지속적인 사랑을 추구함을 의미합니다. 감정과 이성의 균형이 잘 잡혀있어 현실적이면서도 로맨틱한 관계를 만들어갑니다. 상대방과의 조화를 중시하며, 서로를 이해하고 배려하는 성숙한 관계를 구축합니다. 균형 잡힌 사랑으로 행복한 관계를 만들어가세요.",
                
                '운세선': "균형 잡힌 운세선은 안정적인 변화와 지속적인 성장을 나타냅니다. 급격한 변화보다는 점진적이고 계획적인 발전을 추구하며, 새로운 기회와 안정성의 균형을 잘 맞춰나갑니다. 모험심과 신중함을 모두 가지고 있어 적절한 때에 적절한 결정을 내릴 수 있습니다. 균형 잡힌 접근으로 더 나은 미래를 만들어가세요."
            }
        }
        
        # 언덕 부위 분석 (간단한 버전)
        self.mount_analysis = {
            '목성언덕': "검지 아래 목성언덕의 발달 정도가 당신의 리더십과 야망을 보여줍니다. 적당히 발달된 목성언덕은 자신감과 포용력, 그리고 큰 꿈을 품을 수 있는 능력을 의미합니다. 리더십을 발휘할 기회가 많을 것이며, 자신의 목표를 향해 당당하게 나아갈 수 있는 힘을 가지고 있습니다.",
            
            '토성언덕': "중지 아래 토성언덕은 당신의 책임감과 인내력을 나타냅니다. 균형 잡힌 토성언덕은 신중하고 성실한 성격을 보여주며, 어려운 일도 끝까지 해내는 끈기를 가지고 있습니다. 시간이 지날수록 더 큰 성과를 얻을 수 있으며, 꾸준함이 당신의 가장 큰 무기입니다.",
            
            '태양언덕': "약지 아래 태양언덕은 창의력과 매력을 상징합니다. 발달된 태양언덕은 예술적 재능과 사회적 매력을 의미하며, 사람들에게 긍정적인 에너지를 전달하는 능력을 가지고 있습니다. 창의적인 분야에서 두각을 나타낼 가능성이 높으며, 당신만의 독특한 매력으로 많은 사람들을 이끌 수 있습니다.",
            
            '수성언덕': "새끼손가락 아래 수성언덕은 소통 능력과 지적 호기심을 보여줍니다. 잘 발달된 수성언덕은 뛰어난 언어 능력과 학습 능력을 의미하며, 사람들과의 소통에서 재치와 유머를 발휘할 수 있습니다. 상업적 감각도 뛰어나며, 커뮤니케이션을 통한 성공 가능성이 높습니다."
        }

    def _preprocess_image(self, img: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """이미지 전처리 - 손금선 검출을 위한 최적화"""
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()
        
        # 노이즈 제거
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # 대비 향상
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        return enhanced, enhanced

    def _detect_hand_region(self, img: np.ndarray) -> np.ndarray:
        """손 영역 검출 (간단 버전)"""
        try:
            # HSV 색공간으로 피부색 검출
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # 모폴로지 연산
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            return mask
        except:
            # 실패시 전체 영역 반환
            return np.ones(img.shape[:2], dtype=np.uint8) * 255

    def _detect_palm_lines(self, img: np.ndarray, hand_mask: np.ndarray) -> List[np.ndarray]:
        """손금선 검출"""
        try:
            enhanced, _ = self._preprocess_image(img)
            masked = cv2.bitwise_and(enhanced, enhanced, mask=hand_mask)
            
            # Canny 에지 검출
            edges = cv2.Canny(masked, 30, 100, apertureSize=3)
            
            # HoughLinesP로 선 검출
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                                   minLineLength=20, maxLineGap=8)
            
            return lines if lines is not None else []
        except:
            return []

    def _analyze_line_features(self, lines: List[np.ndarray], img_shape: Tuple) -> Dict:
        """선의 특징 분석"""
        if not len(lines):
            return {
                'line_count': 0,
                'avg_length': 0,
                'density': 0
            }
        
        h, w = img_shape[:2]
        lengths = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            lengths.append(length)
        
        return {
            'line_count': len(lines),
            'avg_length': np.mean(lengths) if lengths else 0,
            'density': len(lines) / (w * h) * 10000  # 정규화된 밀도
        }

    def _classify_line_type(self, features: Dict) -> str:
        """손금 유형 분류 (5가지)"""
        line_count = features.get('line_count', 0)
        avg_length = features.get('avg_length', 0)
        density = features.get('density', 0)
        
        # 검출 실패시 균형형으로 분류
        if line_count < 3:
            return 'balanced'
        
        # 길이 기준: 50 이상=길다, 미만=짧다
        # 밀도 기준: 3 이상=굵다, 미만=가늘다
        is_long = avg_length >= 50
        is_thick = density >= 3
        
        if is_thick and is_long:
            return 'thick_long'
        elif is_thick and not is_long:
            return 'thick_short'
        elif not is_thick and is_long:
            return 'thin_long'
        elif not is_thick and not is_long:
            return 'thin_short'
        else:
            return 'balanced'

    def _check_detection_quality(self, features: Dict) -> str:
        """검출 품질 확인"""
        line_count = features.get('line_count', 0)
        avg_length = features.get('avg_length', 0)
        
        if line_count == 0:
            return "손금선이 검출되지 않았습니다. 밝은 조명에서 손바닥을 펼친 상태로 명확하게 촬영해주세요."
        
        if line_count < 3:
            return "검출된 손금선이 너무 적습니다. 손바닥 전체가 잘 보이도록 다시 촬영하시거나, 더 밝은 조명에서 시도해보세요."
        
        if line_count > 80:
            return "검출된 선이 너무 많아 정확한 분석이 어렵습니다. 그림자나 반사광을 피하고 자연광에서 다시 촬영해주세요."
        
        if avg_length < 15:
            return "손금선이 명확하게 보이지 않습니다. 카메라와의 거리를 조정하고 초점을 맞춰서 다시 촬영해주세요."
        
        return None

    def analyze_palm_part(self, img: np.ndarray, part_type: str, part_name: str, dominant_hand: str = "오른손") -> Dict[str, Any]:
        """개별 손금 부위 분석"""
        try:
            if part_type == 'mount':
                # 언덕 부위는 간단한 분석
                analysis_text = self.mount_analysis.get(part_name, "이 부위의 특징이 당신의 성격과 능력을 보여줍니다.")
            else:
                # 선 부위는 5가지 유형 분류 기반 분석
                hand_mask = self._detect_hand_region(img)
                lines = self._detect_palm_lines(img, hand_mask)
                features = self._analyze_line_features(lines, img.shape)
                
                # 검출 품질 확인
                quality_issue = self._check_detection_quality(features)
                if quality_issue:
                    analysis_text = f"📷 {quality_issue}\n\n참고로, 현재 보이는 패턴을 바탕으로 간단한 분석을 제공해드립니다:\n\n손바닥의 전반적인 형태가 균형잡힌 성격과 차분한 기질을 보여줍니다. 더 정확한 분석을 위해 조명과 촬영 각도를 개선해보세요."
                else:
                    # 유형 분류 후 해당 분석 제공
                    line_type = self._classify_line_type(features)
                    analysis_text = self.line_type_analysis[line_type].get(part_name, "이 선의 특징이 당신의 성격을 잘 보여줍니다.")
            
            # 아이콘과 제목 설정
            icons = {
                '감정선': '💕', '지능선': '🧠', '생명선': '💪', '운명선': '⭐',
                '태양선': '☀️', '금성띠': '💫', '결혼선': '💒', '운세선': '🌊',
                '목성언덕': '🏔️', '토성언덕': '🗻', '태양언덕': '🌅', '수성언덕': '💎'
            }
            
            titles = {
                '감정선': '감정선 (Heart Line)', '지능선': '지능선 (Head Line)', 
                '생명선': '생명선 (Life Line)', '운명선': '운명선 (Fate Line)',
                '태양선': '태양선 (Sun Line)', '금성띠': '금성띠 (Girdle of Venus)', 
                '결혼선': '결혼선 (Marriage Line)', '운세선': '운세선 (Via Lasciva)',
                '목성언덕': '목성언덕 (검지 아래)', '토성언덕': '토성언덕 (중지 아래)', 
                '태양언덕': '태양언덕 (약지 아래)', '수성언덕': '수성언덕 (새끼손가락 아래)'
            }
            
            return {
                'success': True,
                'part_type': part_type,
                'part_name': part_name,
                'dominant_hand': dominant_hand,
                'icon': icons.get(part_name, '🔮'),
                'title': titles.get(part_name, part_name),
                'analysis': analysis_text,
                'image_analyzed': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'분석 중 오류 발생: {str(e)}',
                'part_type': part_type,
                'part_name': part_name
            }

    def get_full_analysis(self, img: np.ndarray, dominant_hand: str = "오른손") -> Dict[str, Any]:
        """전체 손금 분석"""
        try:
            hand_mask = self._detect_hand_region(img)
            lines = self._detect_palm_lines(img, hand_mask)
            features = self._analyze_line_features(lines, img.shape)
            
            # 검출 품질 확인
            quality_issue = self._check_detection_quality(features)
            
            if quality_issue:
                # 품질 문제시 기본 점수
                scores = {
                    'relationships': 75,
                    'creativity': 75,
                    'health': 75,
                    'success': 75
                }
                score_explanation = "손금선이 명확하게 보이지 않아 정확한 분석이 어려워 보수적인 점수로 계산되었습니다."
            else:
                # 특징 기반 점수 계산
                scores = self._calculate_scores(features)
                score_explanation = "손금선이 잘 검출되어 실제 특징을 바탕으로 점수가 계산되었습니다."
            
            return {
                'dominant_hand': dominant_hand,
                'scores': scores,
                'score_explanation': score_explanation,
                'quality_message': quality_issue,
                'total_parts': 12,
                'analyzed': True
            }
            
        except Exception as e:
            return {
                'dominant_hand': dominant_hand,
                'scores': {
                    'relationships': 75,
                    'creativity': 75,
                    'health': 75,
                    'success': 75
                },
                'score_explanation': "이미지 분석이 어려워 기본 점수로 계산되었습니다.",
                'quality_message': "이미지 처리 중 오류가 발생했습니다.",
                'total_parts': 12,
                'analyzed': False
            }

    def _calculate_scores(self, features: Dict) -> Dict[str, int]:
        """특징 기반 점수 계산"""
        line_count = features.get('line_count', 0)
        avg_length = features.get('avg_length', 0)
        density = features.get('density', 0)
        
        # 기본 점수
        base = 70
        
        # 관계운 (선의 개수와 밀도 기반)
        relationships = base
        if line_count > 20:
            relationships += 20
        elif line_count > 10:
            relationships += 15
        else:
            relationships += 8
        
        if density > 4:
            relationships += 10
        
        # 창의력 (복잡성 기반)
        creativity = base
        if line_count > 15 and avg_length > 40:
            creativity += 25
        elif line_count > 8:
            creativity += 15
        else:
            creativity += 10
        
        # 건강운 (선의 품질 기반)
        health = base
        if avg_length > 60:
            health += 20
        elif avg_length > 30:
            health += 15
        else:
            health += 8
        
        # 성공운 (전체적 조화)
        success = base
        if line_count > 12 and avg_length > 50:
            success += 25
        elif line_count > 6 and avg_length > 30:
            success += 18
        else:
            success += 10
        
        return {
            'relationships': min(100, max(60, relationships)),
            'creativity': min(100, max(60, creativity)),
            'health': min(100, max(60, health)),
            'success': min(100, max(60, success))
        }

# 기존 호환성 함수들
def analyze_image(img: np.ndarray, dominant_hand: str = "오른손"):
    analyzer = PalmAnalyzer()
    result = analyzer.get_full_analysis(img, dominant_hand)
    
    features = {
        'dominant_hand': dominant_hand,
        'total_parts': 12
    }
    
    scores = result['scores']
    return features, scores

def analyze_palm_part(img: np.ndarray, part_type: str, part_name: str, dominant_hand: str = "오른손"):
    analyzer = PalmAnalyzer()
    return analyzer.analyze_palm_part(img, part_type, part_name, dominant_hand)

__all__ = ["analyze_image", "analyze_palm_part", "PalmAnalyzer"]
