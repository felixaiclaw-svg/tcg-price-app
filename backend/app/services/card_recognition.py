"""
卡牌識別服務 - AI 視覺版
使用 Google Gemini Vision API（免費）進行卡牌識別
準確率遠高於傳統 OCR，支援複雜場景（反光、傾斜、手拿等）

備用方案：Tesseract OCR（當 Gemini 不可用時）
"""

import io
import os
import cv2
import numpy as np
from PIL import Image
import pytesseract
from typing import Optional, Dict, List
import re
import base64


class CardRecognitionService:
    """TCG 卡牌識別服務 - AI 視覺識別 + OCR 備用"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_available = self.api_key is not None
        
        # 初始化 Gemini（如果 API key 存在）
        if self.gemini_available:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✓ Gemini Vision 已啟用（免費層：60 請求/分鐘）")
            except Exception as e:
                print(f"✗ Gemini 初始化失敗：{e}，將使用 OCR 備用方案")
                self.gemini_available = False
        else:
            print("⚠ 未設置 GEMINI_API_KEY，使用 OCR 備用方案")
            print("  申請免費 API Key: https://aistudio.google.com/app/apikey")
        
        # TCG 遊戲特徵關鍵詞
        self.tcg_keywords = {
            'PTCG': ['POKÉMON', 'Pokémon', 'pokemon', 'HP', 'LV.', 'ピカチュウ', '宝可梦', '皮卡丘'],
            'OPCG': ['ONE PIECE', 'One Piece', 'ドン!!', '海贼王', '원피스', '海賊王'],
            'YUGIOH': ['YU-GI-OH!', '遊☆戯☆王', '游戏王', '유희왕', 'Effect Monster'],
            'MTG': ['MAGIC', 'Magic: The Gathering', '万智牌', 'マジック'],
        }
        
        # 語言檢測特徵
        self.language_patterns = {
            'JP': {
                'pattern': r'[\u3040-\u309F\u30A0-\u30FF]',
                'name': '日文',
                'code': 'JP',
                'price_multiplier': 1.0
            },
            'CN_TRAD': {
                'pattern': r'[\u4E00-\u9FFF]',
                'name': '繁體中文',
                'code': 'ZH-HK',
                'price_multiplier': 1.2
            },
            'CN_SIMP': {
                'pattern': r'[\u4E00-\u9FFF].*(宝可梦 | 游戏王 | 海贼王)',
                'name': '簡體中文',
                'code': 'ZH-CN',
                'price_multiplier': 0.9
            },
            'EN': {
                'pattern': r'\b(Pokémon|ONE PIECE|Yu-Gi-Oh!|Magic)\b',
                'name': '英文',
                'code': 'EN',
                'price_multiplier': 1.5
            },
            'KR': {
                'pattern': r'[\uAC00-\uD7AF]',
                'name': '韓文',
                'code': 'KO',
                'price_multiplier': 1.1
            },
        }
        
        # 卡牌編號格式
        self.number_patterns = [
            r'(\d{1,3}/\d{1,3})',
            r'(\d{3}/\d{3})',
            r'(\d{1,3}-\d{1,3})',
        ]
    
    async def recognize_card(self, image_file) -> Optional[Dict]:
        """
        識別卡牌信息 - 優先使用 Gemini Vision，失敗則用 OCR
        """
        try:
            contents = await image_file.read()
            image = Image.open(io.BytesIO(contents))
            
            # 嘗試 Gemini Vision（高準確率）
            if self.gemini_available:
                print("\n=== 使用 Gemini Vision 識別 ===")
                card_info = await self._recognize_with_gemini(contents, image)
                if card_info and card_info.get('confidence', 0) > 0.3:
                    print(f"✓ Gemini 識別成功：{card_info}")
                    return card_info
                else:
                    print("⚠ Gemini 識別置信度低，切換到 OCR 備用方案")
            
            # 備用：傳統 OCR
            print("\n=== 使用 OCR 備用方案 ===")
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            img_processed = self._preprocess_image(img_cv)
            text = self._extract_text_multilingual(img_processed)
            card_info = self._analyze_with_ocr(text, img_cv, contents)
            print(f"OCR 識別結果：{card_info}")
            return card_info
            
        except Exception as e:
            print(f"識別錯誤：{e}")
            return None
    
    async def _recognize_with_gemini(self, image_bytes: bytes, image: Image.Image) -> Optional[Dict]:
        """
        使用 Gemini Vision 識別卡牌
        """
        try:
            import google.generativeai as genai
            
            # 構建提示詞
            prompt = """
你是一個 TCG 卡牌識別專家。請分析這張圖片中的卡牌，提取以下信息：

1. 遊戲名稱（Pokemon/One Piece/Yu-Gi-Oh/Magic 等）
2. 卡牌名稱（如果有文字）
3. 卡牌編號（格式如 153/SV-P 或 025/165）
4. 卡牌系列（如 Scarlet & Violet, Base Set 等）
5. 語言版本（英文/繁體中文/簡體中文/日文/韓文）

請以 JSON 格式返回，只返回 JSON，不要其他文字：
{
    "game": "遊戲名稱",
    "name": "卡牌名稱",
    "number": "卡牌編號",
    "set": "系列名稱",
    "language": "語言",
    "confidence": 0.0-1.0
}

如果某些信息無法識別，用 null 或 "Unknown" 表示。
卡牌編號最重要，請仔細識別。
"""
            
            # 調用 Gemini API
            response = self.model.generate_content([prompt, image])
            response_text = response.text.strip()
            
            print(f"Gemini 原始回應：{response_text[:300]}")
            
            # 解析 JSON
            import json
            # 清理可能的 markdown 標記
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            result = json.loads(response_text)
            
            # 轉換為我們的格式
            card_info = {
                'game': result.get('game', 'Unknown'),
                'name': result.get('name', 'Unknown'),
                'number': result.get('number', 'Unknown'),
                'set': result.get('set', 'Unknown'),
                'language': self._map_language(result.get('language', '英文')),
                'language_name': result.get('language', '英文'),
                'language_code': self._get_language_code(result.get('language', '英文')),
                'confidence': result.get('confidence', 0.5),
                'source': 'gemini'
            }
            
            return card_info
            
        except Exception as e:
            print(f"Gemini 識別失敗：{e}")
            return None
    
    def _map_language(self, language: str) -> str:
        """將語言名稱映射到代碼"""
        lang_lower = language.lower()
        if '繁' in lang_lower or 'hk' in lang_lower or 'tw' in lang_lower:
            return 'CN_TRAD'
        elif '簡' in lang_lower or 'cn' in lang_lower:
            return 'CN_SIMP'
        elif '日' in lang_lower or 'jp' in lang_lower:
            return 'JP'
        elif '韓' in lang_lower or 'ko' in lang_lower:
            return 'KR'
        else:
            return 'EN'
    
    def _get_language_code(self, language: str) -> str:
        """獲取語言代碼"""
        lang_lower = language.lower()
        if '繁' in lang_lower or 'hk' in lang_lower or 'tw' in lang_lower:
            return 'ZH-HK'
        elif '簡' in lang_lower or 'cn' in lang_lower:
            return 'ZH-CN'
        elif '日' in lang_lower or 'jp' in lang_lower:
            return 'JP'
        elif '韓' in lang_lower or 'ko' in lang_lower:
            return 'KO'
        else:
            return 'EN'
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """圖片預處理 - 增強 OCR 準確度"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
        binary = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        kernel = np.ones((2, 2), np.uint8)
        morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        return morphed
    
    def _extract_text_multilingual(self, image: np.ndarray) -> str:
        """多語言 OCR 文字提取"""
        custom_config = r'--oem 3 --psm 6'
        langs = ['eng', 'chi_tra', 'chi_sim', 'jpn', 'kor']
        
        try:
            langs_installed = pytesseract.get_languages(config='')
            available_langs = [l for l in langs if l in langs_installed]
        except:
            available_langs = ['eng']
        
        if not available_langs:
            available_langs = ['eng']
        
        lang_str = '+'.join(available_langs)
        text = pytesseract.image_to_string(image, lang=lang_str, config=custom_config)
        return text
    
    def _analyze_with_ocr(self, text: str, image: np.ndarray, image_bytes: bytes) -> Dict:
        """使用 OCR 文字分析卡牌信息"""
        print(f"\n=== OCR 識別結果 ===")
        print(f"識別文字：{text[:500] if text else '(無文字)'}")
        print(f"===================\n")
        
        card_info = {
            'name': 'Unknown',
            'set': 'Unknown',
            'number': 'Unknown',
            'language': 'EN',
            'language_name': '英文',
            'language_code': 'EN',
            'game': 'Unknown',
            'confidence': 0.0,
            'source': 'ocr'
        }
        
        # 1. 檢測遊戲類型
        for game, keywords in self.tcg_keywords.items():
            if any(keyword.lower() in text.lower() for keyword in keywords):
                card_info['game'] = game
                break
        
        # 2. 檢測語言版本
        detected_langs = []
        for lang_code, lang_info in self.language_patterns.items():
            if re.search(lang_info['pattern'], text):
                detected_langs.append({
                    'code': lang_code,
                    'name': lang_info['name'],
                    'confidence': len(re.findall(lang_info['pattern'], text))
                })
        
        if detected_langs:
            best_lang = max(detected_langs, key=lambda x: x['confidence'])
            card_info['language'] = best_lang['code']
            card_info['language_name'] = best_lang['name']
            card_info['language_code'] = self.language_patterns.get(
                best_lang['code'], {}
            ).get('code', best_lang['code'])
        
        # 3. 提取卡牌編號
        for pattern in self.number_patterns:
            number_match = re.search(pattern, text)
            if number_match:
                card_info['number'] = number_match.group(1)
                break
        
        # 4. 提取卡牌名稱
        lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 2]
        if lines:
            excluded = ['POKÉMON', 'ONE PIECE', 'YU-GI-OH!', 'MAGIC', 'Nintendo', ' Creatures', 'GAME FREAK']
            for line in lines:
                if not any(excl.lower() in line.lower() for excl in excluded):
                    card_info['name'] = line[:60]
                    break
        
        # 5. 計算置信度
        if card_info['number'] != 'Unknown':
            card_info['confidence'] = 0.6
        if card_info['name'] != 'Unknown':
            card_info['confidence'] += 0.3
        if card_info['game'] != 'Unknown':
            card_info['confidence'] += 0.1
        
        card_info['confidence'] = min(card_info['confidence'], 1.0)
        
        return card_info


if __name__ == "__main__":
    service = CardRecognitionService()
    print("\n卡牌識別服務已初始化")
    print(f"Gemini Vision: {'✓ 已啟用' if service.gemini_available else '✗ 未啟用'}")
