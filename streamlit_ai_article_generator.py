#!/usr/bin/env python3
"""
AI 기사 생성 파이프라인 Streamlit 페이지
이벤트 감지 → 데이터 분석 → 기사 작성 → 이미지 생성 → 검수 → 광고 추천
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime
import time
import json
import base64
from PIL import Image
import io
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import weasyprint
import requests

# 자동 새로고침을 위한 import (없으면 설치 필요)
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

# 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Agents import
from simple_ai_article_generator import SimpleAIArticleGenerator
from data_monitoring.auto_article_event_system import AutoArticleEventSystem

# Strands Agent import
try:
    from agents.orchestrator_strand import OrchestratorStrand
    from agents.strands_framework import StrandContext
    AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Agents import 실패: {e}")
    AGENTS_AVAILABLE = False

class StreamlitProgressTracker:
    """Streamlit용 진행률 추적기"""
    
    def __init__(self, progress_bar, status_text, log_container):
        self.progress_bar = progress_bar
        self.status_text = status_text
        self.log_container = log_container
        self.logs = []
        self.start_time = time.time()
        self.current_step = 0
        self.total_steps = 6  # 이벤트감지, 데이터분석, 기사작성, 이미지생성, 검수, 광고추천
    
    def update_step(self, step_name: str, message: str = ""):
        """단계 업데이트"""
        self.current_step += 1
        progress = min(self.current_step / self.total_steps, 1.0)
        
        try:
            self.progress_bar.progress(progress)
        except:
            pass
        
        elapsed = time.time() - self.start_time
        status_msg = f"단계: {self.current_step}/{self.total_steps} ({progress*100:.1f}%) - 경과시간: {elapsed:.1f}초"
        status_msg += f"\n🔄 현재 작업: {step_name}"
        if message:
            status_msg += f" - {message}"
        
        try:
            self.status_text.text(status_msg)
        except:
            pass
    
    def add_log(self, message: str, level: str = "INFO"):
        """로그 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(level, "📝")
        log_entry = f"{emoji} [{timestamp}] {message}"
        self.logs.append(log_entry)
        
        try:
            # 최근 15개 로그만 표시
            recent_logs = self.logs[-15:]
            self.log_container.text("\n".join(recent_logs))
        except:
            pass

def collect_event_data_with_progress(tracker):
    """이벤트 데이터 수집"""
    tracker.update_step("이벤트 감지", "경제 이벤트 스캔 중...")
    tracker.add_log("🔍 경제 이벤트 감지 시작", "INFO")
    
    try:
        event_system = AutoArticleEventSystem()
        
        # 이벤트 감지 실행
        tracker.add_log("📊 시장 데이터 분석 중...", "INFO")
        events = event_system.detect_events()
        
        # 시장 컨텍스트 추가
        market_context = event_system.get_market_context()
        
        if events and len(events) > 0:
            tracker.add_log(f"✅ {len(events)}개 이벤트 감지 완료", "SUCCESS")
            
            # 이벤트 상세 로그
            for i, event in enumerate(events, 1):
                tracker.add_log(f"  이벤트 {i}: {event['description']}", "INFO")
            
            # 시장 컨텍스트 정보 추가
            for event in events:
                event['market_context'] = market_context
            
            return events
        else:
            tracker.add_log("⚠️ 감지된 이벤트가 없습니다", "WARNING")
            return []
    
    except Exception as e:
        tracker.add_log(f"❌ 이벤트 감지 실패: {str(e)}", "ERROR")
        # 실패 시에도 기본 이벤트 반환
        tracker.add_log("🔄 기본 이벤트 생성 중...", "INFO")
        return [{
            'type': 'fallback_analysis',
            'symbol': 'MARKET',
            'description': '정기 시장 분석 및 동향 리포트',
            'severity': 0.5,
            'sentiment': 'neutral',
            'timestamp': datetime.now().isoformat(),
            'source': 'fallback'
        }]

def create_wordcloud_image(keywords, title="키워드 워드클라우드"):
    """키워드로부터 워드클라우드 이미지 생성 (한글 지원)"""
    try:
        if not keywords:
            return None
            
        # 키워드 정제 및 가중치 부여
        keyword_freq = {}
        for keyword in keywords:
            if len(keyword) > 1:  # 1글자 키워드 제외
                keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        
        if not keyword_freq:
            return None
            
        # 한글 폰트 경로 찾기
        font_path = None
        possible_fonts = [
            '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Medium.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc',
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            '/System/Library/Fonts/AppleGothic.ttf',  # macOS
            'C:/Windows/Fonts/malgun.ttf'  # Windows
        ]
        
        for font in possible_fonts:
            if os.path.exists(font):
                font_path = font
                break
        
        # 워드클라우드 생성
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color='white',
            font_path=font_path,  # 한글 폰트 사용
            max_words=25,
            colormap='viridis',
            prefer_horizontal=0.6,
            min_font_size=12,
            max_font_size=60,
            relative_scaling=0.5,
            collocations=False  # 단어 조합 방지
        ).generate_from_frequencies(keyword_freq)
        
        # matplotlib figure 생성
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        
        # 제목은 영어로 설정 (한글 폰트 문제 회피)
        english_title = "Article Keywords Wordcloud"
        ax.set_title(english_title, fontsize=16, pad=20)
        
        # 이미지를 바이트로 변환
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer
        
    except Exception as e:
        print(f"워드클라우드 생성 오류: {e}")
        return None

def create_market_trend_chart(events):
    """시장 동향 차트 생성"""
    try:
        # 이벤트에서 가격 변화 데이터 추출
        symbols = []
        changes = []
        
        for event in events:
            if 'symbol' in event and 'description' in event:
                symbols.append(event['symbol'])
                # 설명에서 퍼센트 변화 추출 시도
                desc = event['description']
                if '%' in desc:
                    try:
                        # 간단한 퍼센트 추출
                        import re
                        percent_match = re.search(r'([-+]?\d+\.?\d*)%', desc)
                        if percent_match:
                            changes.append(float(percent_match.group(1)))
                        else:
                            changes.append(0)
                    except:
                        changes.append(0)
                else:
                    changes.append(0)
        
        if symbols and changes:
            fig = px.bar(
                x=symbols,
                y=changes,
                title="주요 종목 가격 변화",
                labels={'x': '종목', 'y': '변화율 (%)'},
                color=changes,
                color_continuous_scale=['red', 'yellow', 'green']
            )
            fig.update_layout(
                showlegend=False,
                height=400
            )
            return fig
        
        return None
        
    except Exception as e:
        print(f"시장 동향 차트 생성 오류: {e}")
        return None

def create_real_stock_chart(symbols):
    """실제 주식 데이터를 사용한 차트 생성"""
    try:
        import yfinance as yf
        from datetime import datetime, timedelta
        
        if not symbols:
            return None
            
        # 최근 5일간의 데이터 가져오기
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)
        
        stock_data = {}
        for symbol in symbols[:5]:  # 최대 5개 종목
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty:
                    stock_data[symbol] = hist['Close'].tolist()
            except:
                continue
        
        if stock_data:
            fig = go.Figure()
            
            for symbol, prices in stock_data.items():
                dates = [start_date + timedelta(days=i) for i in range(len(prices))]
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=prices,
                    mode='lines+markers',
                    name=symbol,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title="주요 종목 최근 5일 가격 추이",
                xaxis_title="날짜",
                yaxis_title="주가 ($)",
                height=400,
                showlegend=True
            )
            
            return fig
        
        return None
        
    except Exception as e:
        print(f"실제 주식 차트 생성 오류: {e}")
        return None

def generate_article_illustration(article_content, bedrock_client):
    """멀티모달 LLM을 활용한 기사 일러스트레이션 생성 (텍스트 설명 + 실제 이미지)"""
    try:
        if not bedrock_client:
            return None
            
        # 기사 내용 요약
        title = article_content.get('title', '')
        content = article_content.get('content', '')
        
        # 1. 텍스트 설명 생성 (기존 기능)
        illustration_prompt = f"""
다음 경제 기사의 내용을 바탕으로 적절한 일러스트레이션을 설명해주세요:

제목: {title}
내용 요약: {content[:500]}...

일러스트레이션 요구사항:
1. 경제/금융 테마에 적합한 이미지
2. 기사 내용을 시각적으로 표현
3. 전문적이고 신뢰할 수 있는 느낌
4. 색상: 파란색, 녹색, 회색 계열 사용

다음 형식으로 응답해주세요:
- 이미지 설명: [상세한 이미지 설명]
- 주요 요소: [포함되어야 할 주요 시각적 요소들]
- 색상 팔레트: [추천 색상들]
- 스타일: [이미지 스타일 설명]
"""

        # Claude에게 일러스트레이션 설명 요청
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": illustration_prompt
                }
            ]
        }
        
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        illustration_description = response_body['content'][0]['text']
        
        # 2. 실제 이미지 생성
        image_result = generate_ai_illustration_image(article_content, bedrock_client)
        
        return {
            'description': illustration_description,
            'prompt_used': illustration_prompt,
            'generated_at': datetime.now().isoformat(),
            'image_file': image_result  # 실제 이미지 파일 정보 추가
        }
        
    except Exception as e:
        print(f"일러스트레이션 생성 오류: {e}")
        # 오류 시에도 플레이스홀더 이미지 생성 시도
        try:
            image_result = generate_placeholder_image(title, "output/images")
            return {
                'description': f"기사 '{title}'에 대한 일러스트레이션을 생성했습니다.",
                'prompt_used': illustration_prompt if 'illustration_prompt' in locals() else '',
                'generated_at': datetime.now().isoformat(),
                'image_file': image_result,
                'error': str(e)
            }
        except:
            return None

def should_generate_wordcloud(article_content, analysis_data):
    """워드클라우드 생성 필요성을 AI가 판단"""
    try:
        # 기사 길이와 키워드 다양성 확인
        content = article_content.get('content', '')
        title = article_content.get('title', '')
        
        # 조건을 더 관대하게 수정
        if len(content) > 500 and len(title.split()) > 2:  # 500자 이상, 제목 2단어 이상
            # 분석 데이터에서 키워드 다양성 확인
            key_symbols = analysis_data.get('key_symbols', [])
            if len(set(key_symbols)) >= 2:  # 2개 이상의 서로 다른 심볼
                return True
        
        # 이벤트가 3개 이상이면 무조건 생성
        total_events = analysis_data.get('total_events', 0)
        if total_events >= 3:
            return True
            
        return False
        
    except Exception as e:
        print(f"워드클라우드 필요성 판단 오류: {e}")
def generate_ai_illustration_image(article_content, bedrock_client, output_dir="output/images"):
    """AWS Bedrock을 사용하여 실제 AI 일러스트레이션 이미지 생성"""
    try:
        if not bedrock_client:
            return None
            
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 기사 내용 요약
        title = article_content.get('title', '')
        content = article_content.get('content', '')
        
        # 이미지 생성을 위한 간단하고 명확한 프롬프트
        image_prompt = f"""
A professional financial illustration showing:
- Stock market charts with upward trending arrows
- Modern financial dashboard with blue and green colors
- Clean, minimalist business style
- Corporate finance theme
- High quality, professional look
- No text or numbers in the image
- Focus on: {title[:50]}
"""
        
        # Stability AI 모델을 사용한 이미지 생성
        request_body = {
            "text_prompts": [
                {
                    "text": image_prompt,
                    "weight": 1.0
                }
            ],
            "cfg_scale": 10,
            "seed": 0,
            "steps": 50,
            "width": 512,
            "height": 512
        }
        
        try:
            # Amazon Titan Image Generator 모델 시도
            request_body = {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": image_prompt,
                    "negativeText": "low quality, blurry, distorted, text, numbers, watermark"
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "height": 512,
                    "width": 512,
                    "cfgScale": 8.0,
                    "seed": 0
                }
            }
            
            response = bedrock_client.invoke_model(
                modelId="amazon.titan-image-generator-v1",
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            
            # Base64 이미지 데이터 추출
            if 'images' in response_body and len(response_body['images']) > 0:
                image_data = response_body['images'][0]
                
                # 이미지 파일로 저장
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"ai_illustration_{timestamp}.png"
                image_path = os.path.join(output_dir, image_filename)
                
                # Base64 디코딩 후 파일 저장
                import base64
                image_bytes = base64.b64decode(image_data)
                
                with open(image_path, 'wb') as f:
                    f.write(image_bytes)
                
                return {
                    'image_path': image_path,
                    'filename': image_filename,
                    'prompt_used': image_prompt,
                    'generated_at': datetime.now().isoformat(),
                    'model_used': 'amazon.titan-image-generator-v1'
                }
            else:
                print("Titan 이미지 생성 응답에 images가 없습니다")
                return generate_placeholder_image(title, output_dir)
                
        except Exception as titan_error:
            print(f"Amazon Titan 모델 오류: {titan_error}")
            
            # Stability AI 모델 시도
            try:
                request_body = {
                    "text_prompts": [
                        {
                            "text": image_prompt,
                            "weight": 1.0
                        }
                    ],
                    "cfg_scale": 10,
                    "seed": 0,
                    "steps": 50,
                    "width": 512,
                    "height": 512
                }
                
                response = bedrock_client.invoke_model(
                    modelId="stability.stable-diffusion-xl-base-v1-0",
                    body=json.dumps(request_body)
                )
                
                response_body = json.loads(response['body'].read())
                
                # Base64 이미지 데이터 추출
                if 'artifacts' in response_body and len(response_body['artifacts']) > 0:
                    image_data = response_body['artifacts'][0]['base64']
                    
                    # 이미지 파일로 저장
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    image_filename = f"ai_illustration_{timestamp}.png"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    # Base64 디코딩 후 파일 저장
                    import base64
                    image_bytes = base64.b64decode(image_data)
                    
                    with open(image_path, 'wb') as f:
                        f.write(image_bytes)
                    
                    return {
                        'image_path': image_path,
                        'filename': image_filename,
                        'prompt_used': image_prompt,
                        'generated_at': datetime.now().isoformat(),
                        'model_used': 'stability.stable-diffusion-xl-base-v1-0'
                    }
                else:
                    print("이미지 생성 응답에 artifacts가 없습니다")
                    return generate_placeholder_image(title, output_dir)
                    
            except Exception as stability_error:
                print(f"Stability AI 모델 오류: {stability_error}")
                # 대체 방법: 간단한 플레이스홀더 이미지 생성
                return generate_placeholder_image(title, output_dir)
        
    except Exception as e:
        print(f"AI 이미지 생성 오류: {e}")
        return None

def generate_placeholder_image(title, output_dir):
    """플레이스홀더 이미지 생성 (Bedrock 이미지 생성 실패 시 대체)"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
        
        # 이미지 생성
        width, height = 512, 512
        img = Image.new('RGB', (width, height), color='#f8f9fa')
        draw = ImageDraw.Draw(img)
        
        # 배경 그라데이션 효과
        for y in range(height):
            color_value = int(248 - (y / height) * 20)  # 248에서 228로 그라데이션
            color = (color_value, color_value + 2, color_value + 5)
            draw.line([(0, y), (width, y)], fill=color)
        
        # 제목 텍스트 추가
        try:
            # 기본 폰트 사용
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        except:
            font_large = None
            font_small = None
        
        # 제목 래핑
        wrapped_title = textwrap.fill(title[:50], width=25)
        
        # 텍스트 위치 계산
        text_y = height // 2 - 50
        
        # 제목 그리기
        draw.text((width//2, text_y), "📊 AI 경제 기사", 
                 fill='#2c3e50', anchor='mm', font=font_large)
        
        draw.text((width//2, text_y + 40), wrapped_title, 
                 fill='#34495e', anchor='mm', font=font_small)
        
        # 장식 요소 추가
        # 상승 화살표
        arrow_points = [(width//2 - 30, height//2 + 80), 
                       (width//2, height//2 + 50), 
                       (width//2 + 30, height//2 + 80)]
        draw.polygon(arrow_points, fill='#27ae60')
        
        # 차트 라인 시뮬레이션
        import random
        points = []
        for i in range(0, width, 20):
            y = height//2 + 100 + random.randint(-20, 20)
            points.append((i, y))
        
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill='#3498db', width=3)
        
        # 파일 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filename = f"placeholder_illustration_{timestamp}.png"
        image_path = os.path.join(output_dir, image_filename)
        
        img.save(image_path)
        
        return {
            'image_path': image_path,
            'filename': image_filename,
            'prompt_used': f"Placeholder image for: {title}",
            'generated_at': datetime.now().isoformat(),
            'model_used': 'PIL_placeholder'
        }
        
    except Exception as e:
        print(f"플레이스홀더 이미지 생성 오류: {e}")
        return None
    """HTML 콘텐츠를 PDF로 변환"""
    try:
        # CSS 스타일 추가
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Noto Sans CJK KR', Arial, sans-serif;
                    line-height: 1.6;
                    margin: 40px;
                    color: #333;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                }}
                .meta-info {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-left: 4px solid #3498db;
                    margin: 20px 0;
                }}
                .content {{
                    text-align: justify;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            {html_content}
            <div class="footer">
                <p>Generated by AI Economic News System | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
        
        # PDF 생성
        weasyprint.HTML(string=styled_html).write_pdf(output_path)
        return True
        
    except Exception as e:
        print(f"PDF 변환 오류: {e}")
        return False

def send_pdf_to_slack(pdf_path, webhook_url, title="AI 생성 경제 기사"):
    """PDF 파일을 Slack으로 전송"""
    try:
        # Slack 웹훅이 파일 업로드를 직접 지원하지 않으므로
        # 파일 정보와 함께 메시지만 전송
        message = {
            "text": f"📰 {title}",
            "attachments": [
                {
                    "color": "good",
                    "fields": [
                        {
                            "title": "📄 PDF 파일 생성 완료",
                            "value": f"파일 경로: {pdf_path}\\n파일 크기: {os.path.getsize(pdf_path)} bytes",
                            "short": False
                        },
                        {
                            "title": "🕒 생성 시간",
                            "value": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "short": True
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(webhook_url, json=message)
        return response.status_code == 200
        
    except Exception as e:
        print(f"Slack 전송 오류: {e}")
        return False

def create_html_article(result):
    """결과 데이터를 HTML 기사로 변환"""
    try:
        article = result.get('article', {})
        analysis = result.get('analysis', {})
        review = result.get('review', {})
        
        title = article.get('title', '제목 없음')
        content = article.get('content', '내용 없음')
        
        # HTML 구조 생성
        html_content = f"""
        <h1>{title}</h1>
        
        <div class="meta-info">
            <strong>📊 기사 정보</strong><br>
            생성 시간: {result.get('timestamp', '')}<br>
            감지된 이벤트: {analysis.get('total_events', 0)}개<br>
            시장 감정: {analysis.get('market_sentiment', 'neutral')}<br>
            품질 점수: {review.get('quality_score', 0)}/10
        </div>
        
        <div class="content">
            {content.replace(chr(10), '<br>').replace(chr(10)+chr(10), '</p><p>')}
        </div>
        
        <h2>📈 주요 종목</h2>
        <ul>
        """
        
        # 주요 종목 추가
        key_symbols = analysis.get('key_symbols', [])
        for symbol in key_symbols[:5]:
            html_content += f"<li>{symbol}</li>"
        
        html_content += "</ul>"
        
        # AI 일러스트레이션 추가
        images = result.get('images', {})
        ai_illustration = images.get('ai_illustration')
        if ai_illustration and isinstance(ai_illustration, dict):
            description = ai_illustration.get('description', '')
            if description:
                html_content += f"""
                <h2>🎨 AI 생성 일러스트레이션 가이드</h2>
                <div class="meta-info">
                    {description.replace(chr(10), '<br>')}
                </div>
                """
        
        # 검수 결과 추가
        if review:
            html_content += f"""
            <h2>🔍 검수 결과</h2>
            <div class="meta-info">
                <strong>품질 평가:</strong> {review.get('quality_score', 0)}/10<br>
                <strong>개선 제안:</strong><br>
                <ul>
            """
            
            suggestions = review.get('suggestions', [])
            for suggestion in suggestions:
                html_content += f"<li>{suggestion}</li>"
            
            html_content += "</ul></div>"
        
        return html_content
        
    except Exception as e:
        print(f"HTML 생성 오류: {e}")
        return f"<h1>오류 발생</h1><p>HTML 생성 중 오류가 발생했습니다: {str(e)}</p>"
        
    except Exception as e:
        print(f"워드클라우드 필요성 판단 오류: {e}")
        return True  # 오류 시 생성

def generate_article_with_agents(events, tracker):
    """에이전트를 사용한 기사 생성"""
    
    try:
        # Agents 사용 가능 여부 체크
        if not AGENTS_AVAILABLE:
            tracker.add_log("❌ Agents 시스템을 사용할 수 없습니다. 대체 시스템을 사용합니다.", "ERROR")
            return generate_article_fallback(events, tracker)
        
        # 오케스트레이터 초기화
        tracker.update_step("시스템 초기화", "AI 에이전트 준비 중...")
        tracker.add_log("🤖 AI 에이전트 시스템 초기화", "INFO")
        
        try:
            orchestrator = OrchestratorStrand()
            tracker.add_log("✅ OrchestratorStrand 초기화 성공", "SUCCESS")
        except Exception as init_error:
            tracker.add_log(f"❌ OrchestratorStrand 초기화 실패: {str(init_error)}", "ERROR")
            tracker.add_log("🔄 대체 시스템으로 전환합니다", "INFO")
            return generate_article_fallback(events, tracker)
        
        # 컨텍스트 생성
        context = StrandContext(
            strand_id=f"streamlit_article_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            input_data={
                "events": events,
                "request_type": "comprehensive_article"
            }
        )
        
        # 1. 데이터 분석
        tracker.update_step("데이터 분석", "경제 데이터 심층 분석 중...")
        tracker.add_log("📊 데이터 분석 에이전트 실행", "INFO")
        
        try:
            analysis_result = orchestrator.execute_data_analysis(context)
            if analysis_result:
                tracker.add_log("✅ 데이터 분석 완료", "SUCCESS")
                context.add_data("analysis", analysis_result)
            else:
                tracker.add_log("⚠️ 데이터 분석 결과가 비어있음", "WARNING")
        except Exception as analysis_error:
            tracker.add_log(f"❌ 데이터 분석 오류: {str(analysis_error)}", "ERROR")
            tracker.add_log("🔄 대체 시스템으로 전환합니다", "INFO")
            return generate_article_fallback(events, tracker)
        
        time.sleep(1)  # UI 업데이트 시간
        
        # 2. 기사 작성
        tracker.update_step("기사 작성", "AI 기사 작성 중...")
        tracker.add_log("✍️ 기사 작성 에이전트 실행", "INFO")
        
        try:
            article_result = orchestrator.execute_article_writing(context)
            if article_result:
                tracker.add_log("✅ 기사 작성 완료", "SUCCESS")
                context.add_data("article", article_result)
            else:
                tracker.add_log("❌ 기사 작성 결과가 비어있음", "ERROR")
                tracker.add_log("🔄 대체 시스템으로 전환합니다", "INFO")
                return generate_article_fallback(events, tracker)
        except Exception as writing_error:
            tracker.add_log(f"❌ 기사 작성 오류: {str(writing_error)}", "ERROR")
            tracker.add_log("🔄 대체 시스템으로 전환합니다", "INFO")
            return generate_article_fallback(events, tracker)
        
        time.sleep(1)
        
        # 3. 이미지 생성
        tracker.update_step("이미지 생성", "관련 이미지 및 차트 생성 중...")
        tracker.add_log("🎨 이미지 생성 에이전트 실행", "INFO")
        
        image_result = orchestrator.execute_image_generation(context)
        if image_result:
            tracker.add_log("✅ 이미지 생성 완료", "SUCCESS")
            context.add_data("images", image_result)
        else:
            tracker.add_log("⚠️ 이미지 생성 부분 실패", "WARNING")
        
        time.sleep(1)
        
        # 4. 기사 검수
        tracker.update_step("기사 검수", "품질 검수 및 개선 중...")
        tracker.add_log("🔍 검수 에이전트 실행", "INFO")
        
        review_result = orchestrator.execute_review(context)
        if review_result:
            tracker.add_log("✅ 기사 검수 완료", "SUCCESS")
            context.add_data("review", review_result)
        else:
            tracker.add_log("⚠️ 검수 부분 실패", "WARNING")
        
        time.sleep(1)
        
        # 5. 광고 추천
        tracker.update_step("광고 추천", "맞춤 광고 추천 중...")
        tracker.add_log("📢 광고 추천 에이전트 실행", "INFO")
        
        ad_result = orchestrator.execute_ad_recommendation(context)
        if ad_result:
            tracker.add_log("✅ 광고 추천 완료", "SUCCESS")
            context.add_data("ads", ad_result)
        else:
            tracker.add_log("⚠️ 광고 추천 부분 실패", "WARNING")
        
        # 최종 결과 컴파일
        tracker.add_log("🎉 전체 파이프라인 완료!", "SUCCESS")
        
        return {
            'events': events,
            'analysis': analysis_result,
            'article': article_result,
            'images': image_result,
            'review': review_result,
            'ads': ad_result,
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        tracker.add_log(f"💥 파이프라인 실행 중 오류: {str(e)}", "ERROR")
        return None

def generate_article_fallback(events, tracker):
    """대체 기사 생성 시스템 (Agents 없이)"""
    
    try:
        tracker.update_step("대체 시스템 초기화", "SimpleAI 시스템 준비 중...")
        tracker.add_log("🔄 대체 기사 생성 시스템 사용", "INFO")
        
        # SimpleAIArticleGenerator 사용
        generator = SimpleAIArticleGenerator()
        
        # 1. 데이터 분석
        tracker.update_step("데이터 분석", "기본 데이터 분석 중...")
        tracker.add_log("📊 기본 데이터 분석 실행", "INFO")
        
        analysis_data = generator.analyze_events(events)
        tracker.add_log("✅ 데이터 분석 완료", "SUCCESS")
        
        time.sleep(1)
        
        # 2. 기사 작성
        tracker.update_step("기사 작성", "AI 기사 작성 중...")
        tracker.add_log("✍️ Claude 기사 작성 실행", "INFO")
        
        # Claude를 사용한 기사 생성
        article_content = generator.generate_article_with_claude(events, analysis_data)
        
        if not article_content:
            tracker.add_log("❌ 기사 생성 실패", "ERROR")
            return None
            
        tracker.add_log("✅ 기사 작성 완료", "SUCCESS")
        time.sleep(1)
        
        # 3. 이미지/차트 생성
        tracker.update_step("이미지 생성", "차트 및 이미지 생성 중...")
        tracker.add_log("🖼️ 차트 생성", "INFO")
        
        charts = generator.create_simple_charts(events, analysis_data)
        
        # 추가 시장 동향 차트 생성
        market_trend_chart = create_market_trend_chart(events)
        if market_trend_chart:
            charts.append({
                'type': 'market_trend',
                'title': '시장 동향 분석',
                'figure': market_trend_chart,
                'description': '주요 종목들의 가격 변화를 보여줍니다.'
            })
        
        # 실제 주식 데이터 차트 생성
        symbols = [event.get('symbol') for event in events if event.get('symbol')]
        real_stock_chart = create_real_stock_chart(symbols)
        if real_stock_chart:
            charts.append({
                'type': 'real_stock_trend',
                'title': '실제 주식 가격 추이',
                'figure': real_stock_chart,
                'description': '최근 5일간 실제 주식 가격 변화를 보여줍니다.'
            })
        
        # 멀티모달 LLM을 활용한 일러스트레이션 생성
        tracker.add_log("🎨 AI 일러스트레이션 생성", "INFO")
        illustration = generate_article_illustration(article_content, generator.bedrock_client)
        
        # 기사 관련 이미지 정보 생성
        article_title = article_content.get('title', '경제 뉴스')
        illustrations = []
        
        if illustration:
            illustrations.append({
                'type': 'ai_generated',
                'description': illustration['description'],
                'generated_at': illustration['generated_at']
            })
        
        # 기본 일러스트레이션 정보 추가
        illustrations.extend([
            {
                'type': 'market_trend',
                'description': f'{article_title}와 관련된 시장 동향 일러스트레이션',
                'keywords': ['시장', '경제', '투자', '주식']
            },
            {
                'type': 'data_visualization', 
                'description': '주요 경제 지표 및 데이터 시각화',
                'keywords': ['데이터', '차트', '분석', '지표']
            }
        ])
        
        # 워드클라우드 생성 여부를 AI가 판단
        should_create_wordcloud = should_generate_wordcloud(article_content, analysis_data)
        wordcloud_image = None
        wordcloud_keywords = []
        
        if should_create_wordcloud:
            tracker.add_log("🔤 워드클라우드 생성 중", "INFO")
            
            # 더 의미있는 키워드 추출
            wordcloud_keywords = []
            
            # 1. 주식 심볼 (가중치 높음)
            for event in events:
                if 'symbol' in event:
                    symbol = event['symbol']
                    wordcloud_keywords.extend([symbol] * 3)  # 3번 추가로 가중치 부여
            
            # 2. 기사 제목에서 의미있는 단어 추출
            if article_title:
                import re
                # 한글, 영문, 숫자만 추출
                title_words = re.findall(r'[가-힣a-zA-Z0-9]+', article_title)
                meaningful_words = [w for w in title_words if len(w) > 1 and w not in ['주가', '기업', '회사', '시장']]
                wordcloud_keywords.extend(meaningful_words * 2)  # 2번 추가
            
            # 3. 기사 내용에서 핵심 키워드 추출
            content = article_content.get('content', '')
            if content:
                # 경제/금융 관련 핵심 키워드 추출
                economic_terms = ['투자', '수익', '성장', '전망', '분석', '실적', '매출', '이익', '손실', 
                                '상승', '하락', '급등', '급락', '변동', '거래', '시가총액', '배당']
                for term in economic_terms:
                    if term in content:
                        wordcloud_keywords.extend([term] * 2)
            
            # 4. 이벤트 설명에서 키워드 추출
            for event in events:
                if 'description' in event:
                    desc = event['description']
                    # 퍼센트, 숫자 관련 키워드
                    if '%' in desc:
                        if '상승' in desc or '급등' in desc:
                            wordcloud_keywords.extend(['상승', '급등'])
                        elif '하락' in desc or '급락' in desc:
                            wordcloud_keywords.extend(['하락', '급락'])
            
            # 5. 감정 기반 키워드
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            for event in events:
                sentiment = event.get('sentiment', 'neutral')
                sentiment_counts[sentiment] += 1
            
            if sentiment_counts['positive'] > sentiment_counts['negative']:
                wordcloud_keywords.extend(['긍정적', '상승세', '호재'] * 2)
            elif sentiment_counts['negative'] > sentiment_counts['positive']:
                wordcloud_keywords.extend(['부정적', '하락세', '악재'] * 2)
            else:
                wordcloud_keywords.extend(['중립적', '혼조세', '관망'] * 2)
            
            # 6. 기본 경제 키워드 (가중치 낮음)
            basic_keywords = ['경제', '금융', '증권', '투자자', '애널리스트', '전문가', '시황']
            wordcloud_keywords.extend(basic_keywords)
            
            # 워드클라우드 이미지 생성
            wordcloud_image = create_wordcloud_image(wordcloud_keywords, "기사 핵심 키워드")
            tracker.add_log("✅ 워드클라우드 생성 완료", "SUCCESS")
        else:
            tracker.add_log("ℹ️ 워드클라우드 생성 불필요로 판단", "INFO")
        
        tracker.add_log("✅ 차트 및 이미지 정보 생성 완료", "SUCCESS")
        
        time.sleep(1)
        
        # 4. 검수
        tracker.update_step("검수", "기사 품질 검수 중...")
        tracker.add_log("🔍 기사 품질 검수", "INFO")
        
        review_result = generator.generate_simple_review(article_content)
        tracker.add_log("✅ 품질 검수 완료", "SUCCESS")
        
        time.sleep(1)
        
        # 5. 광고 추천
        tracker.update_step("광고 추천", "관련 광고 추천 중...")
        tracker.add_log("📢 광고 추천", "INFO")
        
        ads_result = generator.generate_simple_ads(article_content)
        tracker.add_log("✅ 광고 추천 완료", "SUCCESS")
        
        tracker.add_log("✅ 대체 시스템으로 기사 생성 완료", "SUCCESS")
        
        return {
            'article': article_content,
            'analysis': analysis_data,
            'images': {
                'charts': charts,
                'illustrations': illustrations,
                'wordcloud': {
                    'keywords': wordcloud_keywords,
                    'description': '기사 주요 키워드 워드클라우드',
                    'image': wordcloud_image,
                    'generated': should_create_wordcloud
                } if should_create_wordcloud else None,
                'ai_illustration': illustration,
                'chart_image': '데이터 분석 결과 차트 이미지'
            },
            'review': review_result,
            'ads': ads_result,
            'timestamp': datetime.now().isoformat(),
            'system_used': 'fallback_simple_ai'
        }
        
    except Exception as e:
        tracker.add_log(f"💥 대체 시스템 오류: {str(e)}", "ERROR")
        return None

def display_article_content(result):
    """생성된 기사 내용 표시"""
    
    if not result:
        st.error("❌ 생성된 기사가 없습니다.")
        return
    
    st.markdown("---")
    st.header("📰 생성된 AI 기사")
    
    # 기사 메타데이터
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("생성 시간", datetime.fromisoformat(result['timestamp']).strftime('%H:%M:%S'))
    with col2:
        st.metric("감지된 이벤트", len(result.get('events', [])))
    with col3:
        quality_score = result.get('review', {}).get('quality_score', 0)
        st.metric("품질 점수", f"{quality_score:.1f}/10")
    
    # 기사 제목과 본문
    article = result.get('article', {})
    if article:
        st.subheader("📝 기사 제목")
        st.markdown(f"## {article.get('title', '제목 없음')}")
        
        st.subheader("📄 기사 본문")
        content = article.get('content', '내용 없음')
        st.markdown(content)
        
        # 기사 태그
        tags = article.get('tags', [])
        if tags:
            st.subheader("🏷️ 관련 태그")
            tag_cols = st.columns(min(len(tags), 5))
            for i, tag in enumerate(tags[:5]):
                with tag_cols[i]:
                    st.badge(tag)
    
    # 데이터 분석 차트
    images = result.get('images', {})
    charts = images.get('charts', [])
    
    if charts:
        st.subheader("📊 데이터 분석 차트")
        
        for i, chart_data in enumerate(charts):
            # Plotly figure 객체가 있는 경우
            if 'figure' in chart_data:
                st.plotly_chart(chart_data['figure'], use_container_width=True)
                if 'description' in chart_data:
                    st.caption(chart_data['description'])
            # 기존 형식 지원
            elif chart_data.get('type') == 'line':
                fig = px.line(
                    x=chart_data.get('x', []),
                    y=chart_data.get('y', []),
                    title=chart_data.get('title', f'차트 {i+1}')
                )
                st.plotly_chart(fig, use_container_width=True)
            elif chart_data.get('type') == 'bar':
                fig = px.bar(
                    x=chart_data.get('x', []),
                    y=chart_data.get('y', []),
                    title=chart_data.get('title', f'차트 {i+1}')
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # 분석 데이터도 별도로 표시
    analysis = result.get('analysis', {})
    if analysis and not charts:  # 차트가 없을 때만 분석 데이터 표시
        st.subheader("📈 분석 데이터")
        
        # 주요 지표들 표시
        if 'price_changes' in analysis:
            price_changes = analysis['price_changes']
            if price_changes:
                st.write("**주요 종목 변화율:**")
                for item in price_changes[:5]:  # 상위 5개만 표시
                    symbol = item.get('symbol', 'Unknown')
                    change = item.get('change', 0)
                    color = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                    st.write(f"{color} {symbol}: {change:+.2f}%")
        
        # 시장 감정 표시
        if 'market_sentiment' in analysis:
            sentiment = analysis['market_sentiment']
            sentiment_emoji = {"bullish": "🐂", "bearish": "🐻", "neutral": "⚖️"}
            st.write(f"**시장 감정:** {sentiment_emoji.get(sentiment, '⚖️')} {sentiment.upper()}")
    
    # 생성된 이미지 (기사 관련 그림)
    if images and 'illustrations' in images:
        st.subheader("🖼️ 기사 관련 이미지")
        
        illustrations = images.get('illustrations', [])
        if illustrations:
            for i, illustration in enumerate(illustrations):
                if isinstance(illustration, dict):
                    if illustration.get('type') == 'ai_generated':
                        st.markdown("### 🤖 AI 생성 일러스트레이션")
                        st.info("**AI가 기사 내용을 분석하여 생성한 일러스트레이션 설명:**")
                        st.markdown(illustration.get('description', '설명 없음'))
                        st.caption(f"생성 시간: {illustration.get('generated_at', '')}")
                    else:
                        st.write(f"**이미지 {i+1}**: {illustration.get('description', '이미지 설명')}")
                        # 실제 이미지 파일이 있다면 표시
                        if 'path' in illustration:
                            try:
                                st.image(illustration['path'], caption=illustration.get('description', ''))
                            except:
                                st.write("이미지 로드 실패")
                else:
                    st.info(f"**이미지 {i+1}**: {illustration}")
    
    # AI 일러스트레이션 표시 (실제 이미지 파일 포함)
    st.subheader("🎨 AI 생성 일러스트레이션")
    
    try:
        # 데이터 존재 여부 확인
        has_images = bool(images)
        has_ai_illustration = has_images and 'ai_illustration' in images
        ai_illustration_data = images.get('ai_illustration') if has_ai_illustration else None
        has_description = bool(ai_illustration_data and isinstance(ai_illustration_data, dict) and ai_illustration_data.get('description'))
        
        if has_description:
            st.success("🎉 AI 일러스트레이션이 성공적으로 생성되었습니다!")
            
            # 실제 이미지 파일 표시
            image_file_info = ai_illustration_data.get('image_file')
            if image_file_info and isinstance(image_file_info, dict):
                image_path = image_file_info.get('image_path')
                
                if image_path and os.path.exists(image_path):
                    st.markdown("### 🖼️ 생성된 일러스트레이션 이미지")
                    
                    # PIL을 사용하여 이미지 로드 및 표시
                    from PIL import Image
                    try:
                        img = Image.open(image_path)
                        
                        # 두 가지 방식으로 이미지 표시
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**기본 크기:**")
                            st.image(img, caption=f"AI 생성 일러스트레이션")
                        
                        with col2:
                            st.markdown("**전체 너비:**")
                            st.image(img, caption=f"AI 생성 일러스트레이션", use_container_width=True)
                        
                        # 이미지 정보 표시
                        st.info(f"""
                        **이미지 정보:**
                        - 파일명: {image_file_info.get('filename', 'Unknown')}
                        - 모델: {image_file_info.get('model_used', 'Unknown')}
                        - 생성 시간: {image_file_info.get('generated_at', 'Unknown')}
                        - 파일 크기: {os.path.getsize(image_path)} bytes
                        """)
                        
                    except Exception as img_error:
                        st.error(f"이미지 로드 오류: {img_error}")
                        st.write(f"이미지 경로: {image_path}")
                else:
                    st.warning("⚠️ 이미지 파일을 찾을 수 없습니다.")
                    if image_file_info:
                        st.write("이미지 파일 정보:", image_file_info)
            else:
                st.info("📝 텍스트 설명만 생성되었습니다 (이미지 파일 없음)")
            
            # 텍스트 설명 표시
            st.markdown("### 📝 AI 생성 설명")
            description = ai_illustration_data.get('description', '')
            formatted_description = description.replace('\\n\\n', '\n\n').replace('\\n', '\n')
            
            st.text_area(
                "일러스트레이션 설명",
                value=formatted_description,
                height=200,
                disabled=True
            )
            
            # 생성 시간 표시
            generated_at = ai_illustration_data.get('generated_at', '')
            if generated_at:
                st.caption(f"🕒 생성 시간: {generated_at}")
                
        else:
            st.warning("⚠️ AI 일러스트레이션을 생성하지 못했습니다.")
            
            # 수동으로 플레이스홀더 이미지 생성 버튼
            if st.button("🔄 플레이스홀더 이미지 생성", key="generate_placeholder"):
                with st.spinner("플레이스홀더 이미지 생성 중..."):
                    try:
                        article = result.get('article', {})
                        title = article.get('title', 'AI 경제 기사')
                        
                        placeholder_result = generate_placeholder_image(title, "output/images")
                        if placeholder_result:
                            st.success("✅ 플레이스홀더 이미지 생성 완료!")
                            
                            # 생성된 이미지 표시
                            img_path = placeholder_result['image_path']
                            if os.path.exists(img_path):
                                from PIL import Image
                                img = Image.open(img_path)
                                st.image(img, caption="플레이스홀더 일러스트레이션", use_container_width=True)
                        else:
                            st.error("❌ 플레이스홀더 이미지 생성 실패")
                    except Exception as e:
                        st.error(f"💥 오류: {str(e)}")
            
    except Exception as e:
        st.error(f"💥 AI 일러스트레이션 표시 중 오류: {str(e)}")
        st.write("**디버깅 정보:**")
        st.write(f"- images 타입: {type(images)}")
        if images:
            st.write(f"- images 키들: {list(images.keys())}")
            if 'ai_illustration' in images:
                st.write(f"- ai_illustration 내용: {images['ai_illustration']}")
    
    # 워드클라우드나 기타 이미지 정보
    if images and 'wordcloud' in images and images['wordcloud']:
        wordcloud_data = images['wordcloud']
        if wordcloud_data.get('generated', False):  # AI가 필요하다고 판단한 경우만
            st.subheader("📸 추가 시각화")
            st.write("🔤 **워드클라우드**: 기사의 주요 키워드를 시각화")
            
            # 실제 워드클라우드 이미지가 있으면 표시
            if 'image' in wordcloud_data and wordcloud_data['image']:
                try:
                    st.image(wordcloud_data['image'], caption="기사 핵심 키워드", use_container_width=True)
                except Exception as e:
                    st.write(f"워드클라우드 표시 오류: {e}")
                    # 키워드 목록으로 대체
                    keywords = wordcloud_data.get('keywords', [])
                    if keywords:
                        st.write("**주요 키워드:**", ", ".join(list(set(keywords))[:15]))
            else:
                # 키워드 목록 표시
                keywords = wordcloud_data.get('keywords', [])
                if keywords:
                    unique_keywords = list(set(keywords))[:15]  # 중복 제거 후 15개
                    st.write("**주요 키워드:**", ", ".join(unique_keywords))
    
    # 기타 이미지 정보
    if images and any(key in images for key in ['illustration', 'chart_image']):
        if not (images.get('wordcloud', {}).get('generated', False)):  # 워드클라우드가 표시되지 않은 경우만
            st.subheader("📸 추가 시각화")
        
        if 'illustration' in images:
            st.write("🎨 **일러스트레이션**: 기사 내용을 표현하는 이미지")
        if 'chart_image' in images:
            st.write("📊 **차트 이미지**: 데이터 분석 결과 시각화")
    
    # 검수 결과
    review = result.get('review', {})
    if review:
        st.subheader("🔍 검수 결과")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**품질 평가**")
            quality_items = review.get('quality_assessment', {})
            for key, value in quality_items.items():
                st.write(f"• {key}: {value}")
        
        with col2:
            st.markdown("**개선 제안**")
            suggestions = review.get('suggestions', [])
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
    
    # 추천 광고
    ads = result.get('ads', {})
    if ads:
        st.subheader("📢 추천 광고")
        
        recommended_ads = ads.get('recommendations', [])
        if recommended_ads:
            ad_cols = st.columns(min(len(recommended_ads), 2))
            for i, ad in enumerate(recommended_ads[:2]):
                with ad_cols[i]:
                    st.container()
                    st.markdown(f"**{ad.get('title', '광고 제목')}**")
                    st.write(ad.get('description', '광고 설명'))
                    st.caption(f"관련도: {ad.get('relevance_score', 0):.1f}/10")

def show_ai_article_generator():
    """AI 기사 생성기 메인 페이지"""
    
    st.title("🤖 AI 기사 생성 파이프라인")
    st.markdown("**이벤트 감지부터 기사 작성, 이미지 생성, 검수, 광고 추천까지 완전 자동화**")
    st.markdown("---")
    
    # 자동 새로고침 설정
    with st.sidebar:
        st.header("⚙️ 생성 옵션")
        
        # 자동 새로고침 옵션
        auto_refresh = st.checkbox("🔄 5분 자동 새로고침", value=False, key="auto_refresh_check")
        
        if auto_refresh:
            st.info("✅ 5분마다 자동으로 새 기사를 생성합니다")
            # streamlit-autorefresh가 있으면 사용, 없으면 수동 체크
            if st_autorefresh:
                st_autorefresh(interval=300000, key="auto_article_refresh")
            else:
                st.caption("⚠️ 자동 새로고침을 위해서는 페이지를 수동으로 새로고침하세요")
        
        article_type = st.selectbox(
            "기사 유형",
            ["시장 분석", "개별 종목", "경제 전망", "섹터 분석"],
            key="article_type_select"
        )
        
        analysis_depth = st.selectbox(
            "분석 깊이",
            ["기본", "상세", "전문가"],
            key="analysis_depth_select"
        )
        
        include_images = st.checkbox("이미지 생성 포함", value=True, key="include_images_check")
        include_ads = st.checkbox("광고 추천 포함", value=True, key="include_ads_check")
        
        # 마지막 생성 시간 표시
        if 'last_ai_article_update' in st.session_state:
            last_update = st.session_state.last_ai_article_update
            time_diff = datetime.now() - last_update
            minutes_ago = int(time_diff.total_seconds() / 60)
            st.caption(f"마지막 생성: {minutes_ago}분 전")
    
    # 자동 생성 조건 확인
    should_auto_generate = False
    if auto_refresh and 'last_ai_article_update' in st.session_state:
        last_update = st.session_state.last_ai_article_update
        time_diff = datetime.now() - last_update
        # 5분(300초) 이상 경과 시 자동 생성
        if time_diff.total_seconds() >= 300:
            should_auto_generate = True
    
    # 캐시 확인 및 생성 조건
    manual_trigger = st.button("🚀 AI 기사 생성 시작", type="primary", key="ai_article_generate")
    
    if ('ai_article_data' not in st.session_state or 
        manual_trigger or 
        should_auto_generate or
        (auto_refresh and 'ai_article_data' not in st.session_state)):
        
        if should_auto_generate:
            st.info("🔄 5분이 경과하여 자동으로 새 기사를 생성합니다...")
        
        # 진행률 표시 컨테이너
        st.subheader("🔄 AI 기사 생성 진행 상황")
        
        # 진행률 바
        progress_bar = st.progress(0)
        
        # 상태 텍스트
        status_text = st.empty()
        
        # 단계별 상태
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            event_status = st.empty()
        with col2:
            analysis_status = st.empty()
        with col3:
            writing_status = st.empty()
        with col4:
            image_status = st.empty()
        with col5:
            review_status = st.empty()
        with col6:
            ad_status = st.empty()
        
        # 로그 컨테이너
        st.markdown("#### 📝 실시간 로그")
        log_container = st.empty()
        
        # 진행률 추적기 초기화
        tracker = StreamlitProgressTracker(progress_bar, status_text, log_container)
        
        try:
            # 1. 이벤트 감지
            event_status.metric("이벤트 감지", "진행 중...", "🔄")
            events = collect_event_data_with_progress(tracker)
            
            if events:
                event_status.metric("이벤트 감지", f"{len(events)}개", "✅")
            else:
                event_status.metric("이벤트 감지", "실패", "❌")
                st.error("❌ 이벤트 감지에 실패했습니다.")
                return
            
            # 2. AI 에이전트 파이프라인 실행
            analysis_status.metric("데이터 분석", "대기 중...", "⏳")
            writing_status.metric("기사 작성", "대기 중...", "⏳")
            image_status.metric("이미지 생성", "대기 중...", "⏳")
            review_status.metric("기사 검수", "대기 중...", "⏳")
            ad_status.metric("광고 추천", "대기 중...", "⏳")
            
            result = generate_article_with_agents(events, tracker)
            
            if result:
                # 각 단계별 상태 업데이트
                analysis_status.metric("데이터 분석", "완료", "✅")
                writing_status.metric("기사 작성", "완료", "✅")
                
                if include_images:
                    image_status.metric("이미지 생성", "완료", "✅")
                else:
                    image_status.metric("이미지 생성", "건너뜀", "⏭️")
                
                review_status.metric("기사 검수", "완료", "✅")
                
                if include_ads:
                    ad_status.metric("광고 추천", "완료", "✅")
                else:
                    ad_status.metric("광고 추천", "건너뜀", "⏭️")
                
                # 완료
                progress_bar.progress(1.0)
                status_text.success("✅ AI 기사 생성이 완료되었습니다!")
                
                # 세션 상태에 저장
                st.session_state.ai_article_data = result
                st.session_state.last_ai_article_update = datetime.now()
                
                # 성공 메시지
                if should_auto_generate:
                    st.success("🎉 자동 AI 기사 생성이 완료되었습니다!")
                else:
                    st.success("🎉 AI 기사 생성이 완료되었습니다!")
                time.sleep(2)
                st.rerun()
            
            else:
                st.error("❌ AI 기사 생성에 실패했습니다.")
                return
        
        except Exception as e:
            tracker.add_log(f"💥 시스템 오류: {str(e)}", "ERROR")
            st.error(f"❌ 시스템 오류: {str(e)}")
            return
    
    # 캐시된 데이터 사용
    if 'ai_article_data' in st.session_state:
        result = st.session_state.ai_article_data
        last_update = st.session_state.get('last_ai_article_update', datetime.now())
        
        # 업데이트 시간 표시
        st.info(f"📅 마지막 생성: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 생성된 기사 표시
        display_article_content(result)
        
        # 다운로드 옵션
        st.markdown("---")
        st.subheader("💾 다운로드 및 공유 옵션")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📄 기사 텍스트 다운로드", key="download_text"):
                article = result.get('article', {})
                content = f"# {article.get('title', '제목 없음')}\n\n{article.get('content', '내용 없음')}"
                st.download_button(
                    label="다운로드",
                    data=content,
                    file_name=f"ai_article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
        
        with col2:
            if st.button("📊 분석 데이터 다운로드", key="download_analysis"):
                analysis_data = json.dumps(result.get('analysis', {}), indent=2, ensure_ascii=False)
                st.download_button(
                    label="다운로드",
                    data=analysis_data,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("📋 전체 결과 다운로드", key="download_full"):
                # 민감한 정보 제거 후 다운로드
                download_data = {
                    'article': result.get('article', {}),
                    'analysis_summary': result.get('analysis', {}).get('summary', ''),
                    'review': result.get('review', {}),
                    'ads': result.get('ads', {}),
                    'timestamp': result.get('timestamp', '')
                }
                full_data = json.dumps(download_data, indent=2, ensure_ascii=False)
                st.download_button(
                    label="다운로드",
                    data=full_data,
                    file_name=f"ai_article_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col4:
            if st.button("📄 PDF 생성", key="generate_pdf"):
                with st.spinner("PDF 생성 중..."):
                    try:
                        # HTML 콘텐츠 생성
                        html_content = create_html_article(result)
                        
                        # PDF 파일 경로
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        pdf_filename = f"ai_article_{timestamp}.pdf"
                        pdf_path = os.path.join("output", pdf_filename)
                        
                        # output 디렉토리 생성
                        os.makedirs("output", exist_ok=True)
                        
                        # PDF 변환
                        if convert_html_to_pdf(html_content, pdf_path):
                            st.success(f"✅ PDF 생성 완료: {pdf_filename}")
                            
                            # PDF 다운로드 버튼
                            with open(pdf_path, "rb") as pdf_file:
                                st.download_button(
                                    label="📥 PDF 다운로드",
                                    data=pdf_file.read(),
                                    file_name=pdf_filename,
                                    mime="application/pdf"
                                )
                        else:
                            st.error("❌ PDF 생성 실패")
                            
                    except Exception as e:
                        st.error(f"💥 PDF 생성 오류: {str(e)}")
        
        # Slack 전송 섹션
        st.markdown("---")
        st.subheader("📤 Slack 전송")
        
        col1, col2 = st.columns(2)
        
        with col1:
            slack_webhook = st.text_input(
                "Slack 웹훅 URL",
                placeholder="https://hooks.slack.com/services/...",
                type="password",
                help="Slack 앱에서 생성한 웹훅 URL을 입력하세요"
            )
        
        with col2:
            if st.button("📤 Slack으로 전송", key="send_slack"):
                if not slack_webhook:
                    st.error("❌ Slack 웹훅 URL을 입력해주세요")
                else:
                    with st.spinner("Slack 전송 중..."):
                        try:
                            # HTML 콘텐츠 생성
                            html_content = create_html_article(result)
                            
                            # PDF 생성
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            pdf_filename = f"ai_article_{timestamp}.pdf"
                            pdf_path = os.path.join("output", pdf_filename)
                            
                            os.makedirs("output", exist_ok=True)
                            
                            if convert_html_to_pdf(html_content, pdf_path):
                                # Slack 전송
                                article_title = result.get('article', {}).get('title', 'AI 생성 경제 기사')
                                if send_pdf_to_slack(pdf_path, slack_webhook, article_title):
                                    st.success("✅ Slack 전송 완료!")
                                    st.info(f"📄 PDF 파일도 생성되었습니다: {pdf_path}")
                                else:
                                    st.error("❌ Slack 전송 실패")
                            else:
                                st.error("❌ PDF 생성 실패로 Slack 전송 불가")
                                
                        except Exception as e:
                            st.error(f"💥 Slack 전송 오류: {str(e)}")
    
    else:
        st.info("🚀 'AI 기사 생성 시작' 버튼을 클릭하여 새로운 기사를 생성하세요.")

if __name__ == "__main__":
    show_ai_article_generator()
