"""
TCG Price Scanner - Backend API
卡牌價格查詢後端服務
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import os
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

from app.services.card_recognition import CardRecognitionService
from app.services.price_scraper import PriceScraperService
from app.services.currency_converter import CurrencyConverterService

app = FastAPI(
    title="TCG Price Scanner API",
    description="TCG 卡牌價格查詢 API - 支援多平台價格比較",
    version="1.0.0"
)

# CORS 設置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應限制具體域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 服務初始化
card_service = CardRecognitionService()
price_service = PriceScraperService()
currency_service = CurrencyConverterService()


class PriceInfo(BaseModel):
    website: str
    price: float
    currency: str
    url: str
    last_updated: str


class CardPriceResponse(BaseModel):
    card_name: str
    card_set: str
    card_number: str
    language: str
    prices: List[PriceInfo]
    converted_prices: Dict[str, float]  # MOP, HKD, RMB


class CurrencyConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currencies: List[str]


class ManualCardInput(BaseModel):
    """手動輸入卡牌信息"""
    card_name: str
    card_number: Optional[str] = None
    card_set: Optional[str] = None
    game: Optional[str] = "PTCG"
    language: Optional[str] = "ZH-HK"


@app.get("/")
async def root():
    return {
        "message": "TCG Price Scanner API",
        "version": "1.0.0",
        "endpoints": {
            "scan_card": "POST /api/v1/card/scan",
            "get_prices": "GET /api/v1/card/prices",
            "convert_currency": "POST /api/v1/currency/convert",
            "supported_currencies": "GET /api/v1/currencies"
        }
    }


@app.post("/api/v1/card/scan", response_model=CardPriceResponse)
async def scan_card(
    image: UploadFile = File(..., description="卡牌圖片"),
    target_currency: str = Query(default="MOP", description="目標貨幣：MOP/HKD/RMB")
):
    """
    上傳卡牌圖片，自動識別並返回價格信息
    
    - **image**: 卡牌圖片文件
    - **target_currency**: 目標顯示貨幣
    """
    try:
        # 1. 識別卡牌信息
        card_info = await card_service.recognize_card(image)
        
        if not card_info:
            raise HTTPException(status_code=400, detail="無法識別卡牌，請嘗試更清晰的圖片")
        
        # 降低置信度要求，只要有卡牌編號就接受
        if card_info.get('confidence', 0) < 0.3 and card_info.get('number') == 'Unknown':
            raise HTTPException(status_code=400, detail=f"識別置信度較低 ({card_info.get('confidence', 0):.0%})，請嘗試更清晰的圖片。已識別：{card_info.get('game', 'Unknown')} - {card_info.get('language_name', 'Unknown')}")
        
        # 2. 抓取各網站價格
        prices = await price_service.get_prices(card_info)
        
        if not prices:
            raise HTTPException(status_code=404, detail="未找到該卡牌的價格信息")
        
        # 3. 貨幣轉換
        converted = await currency_service.convert_to_currencies(
            prices, 
            ["MOP", "HKD", "RMB"]
        )
        
        return CardPriceResponse(
            card_name=card_info.get("name", "Unknown"),
            card_set=card_info.get("set", "Unknown"),
            card_number=card_info.get("number", "Unknown"),
            language=card_info.get("language", "Unknown"),
            prices=prices,
            converted_prices=converted
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"處理失敗：{str(e)}")


@app.get("/api/v1/card/prices")
async def get_card_prices(
    card_name: str = Query(..., description="卡牌名稱"),
    card_set: Optional[str] = Query(default=None, description="卡牌系列")
):
    """
    根據卡牌名稱查詢價格
    """
    card_info = {"name": card_name, "set": card_set}
    prices = await price_service.get_prices(card_info)
    
    if not prices:
        raise HTTPException(status_code=404, detail="未找到價格信息")
    
    converted = await currency_service.convert_to_currencies(prices, ["MOP", "HKD", "RMB"])
    
    return {
        "card_name": card_name,
        "prices": prices,
        "converted_prices": converted
    }


@app.post("/api/v1/currency/convert")
async def convert_currency(request: CurrencyConvertRequest):
    """
    貨幣轉換
    """
    rates = await currency_service.get_rates(request.from_currency)
    
    result = {
        "amount": request.amount,
        "from": request.from_currency,
        "conversions": {}
    }
    
    for to_currency in request.to_currencies:
        if to_currency in rates:
            result["conversions"][to_currency] = request.amount * rates[to_currency]
    
    return result


@app.get("/api/v1/currencies")
async def get_supported_currencies():
    """
    獲取支援的貨幣列表
    """
    return {
        "currencies": [
            {"code": "MOP", "name": "澳門元", "symbol": "MOP$"},
            {"code": "HKD", "name": "港幣", "symbol": "HK$"},
            {"code": "RMB", "name": "人民幣", "symbol": "¥"},
            {"code": "USD", "name": "美元", "symbol": "$"},
            {"code": "JPY", "name": "日圓", "symbol": "¥"},
            {"code": "CNY", "name": "人民幣", "symbol": "¥"}
        ],
        "default": "MOP"
    }


@app.get("/api/v1/health")
async def health_check():
    """
    健康檢查
    """
    return {
        "status": "healthy",
        "services": {
            "card_recognition": "ok",
            "price_scraper": "ok",
            "currency_converter": "ok"
        },
        "gemini_vision": "enabled" if os.getenv("GEMINI_API_KEY") else "disabled"
    }


@app.post("/api/v1/card/manual", response_model=CardPriceResponse)
async def manual_card_search(
    request: ManualCardInput,
    target_currency: str = Query(default="MOP", description="目標貨幣：MOP/HKD/RMB")
):
    """
    手動輸入卡牌信息並查詢價格
    
    - **card_name**: 卡牌名稱（必填）
    - **card_number**: 卡牌編號（如 153/SV-P）
    - **card_set**: 卡牌系列
    - **game**: 遊戲類型（PTCG/OPCG/YUGIOH/MTG）
    - **language**: 語言版本（ZH-HK/ZH-CN/JP/EN/KO）
    """
    try:
        card_info = {
            "name": request.card_name,
            "number": request.card_number or "Unknown",
            "set": request.card_set or "Unknown",
            "game": request.game or "PTCG",
            "language": request.language or "ZH-HK",
            "language_name": request.language or "繁體中文",
            "language_code": request.language or "ZH-HK",
            "confidence": 1.0,  # 手動輸入，置信度 100%
            "source": "manual"
        }
        
        # 抓取價格
        prices = await price_service.get_prices(card_info)
        
        if not prices:
            raise HTTPException(status_code=404, detail=f"未找到 '{request.card_name}' 的價格信息")
        
        # 貨幣轉換
        converted = await currency_service.convert_to_currencies(
            prices,
            ["MOP", "HKD", "RMB"]
        )
        
        return CardPriceResponse(
            card_name=card_info.get("name", "Unknown"),
            card_set=card_info.get("set", "Unknown"),
            card_number=card_info.get("number", "Unknown"),
            language=card_info.get("language", "Unknown"),
            prices=prices,
            converted_prices=converted
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗：{str(e)}")


@app.get("/api/v1/config/gemini")
async def get_gemini_config():
    """
    獲取 Gemini API 配置狀態
    """
    return {
        "enabled": os.getenv("GEMINI_API_KEY") is not None,
        "setup_instructions": {
            "step1": "訪問 https://aistudio.google.com/app/apikey",
            "step2": "使用 Google 帳號登入",
            "step3": "點擊 'Create API Key'",
            "step4": "複製 API Key",
            "step5": "設置環境變量：GEMINI_API_KEY=你的 key",
            "note": "免費層：60 請求/分鐘，足夠個人使用"
        }
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
