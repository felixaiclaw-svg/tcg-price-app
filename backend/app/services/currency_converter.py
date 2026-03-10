"""
貨幣轉換服務
提供實時匯率轉換
"""

import aiohttp
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class CurrencyConverterService:
    """貨幣轉換服務"""
    
    def __init__(self):
        # 固定匯率參考 (實際應用應使用 API)
        self.base_rates = {
            'USD': 1.0,
            'JPY': 149.50,
            'CNY': 7.24,
            'HKD': 7.82,
            'MOP': 8.05,
            'RMB': 7.24,  # RMB = CNY
        }
        
        # 匯率快取
        self.rate_cache = {}
        self.cache_expiry = {}
    
    async def get_rates(self, base_currency: str = 'USD') -> Dict[str, float]:
        """
        獲取匯率
        
        Args:
            base_currency: 基準貨幣
            
        Returns:
            Dict: 匯率字典
        """
        # 檢查快取
        if base_currency in self.rate_cache:
            if datetime.now() < self.cache_expiry.get(base_currency, datetime.now()):
                return self.rate_cache[base_currency]
        
        # 獲取新匯率
        rates = await self._fetch_rates(base_currency)
        
        # 更新快取 (1 小時過期)
        self.rate_cache[base_currency] = rates
        self.cache_expiry[base_currency] = datetime.now() + timedelta(hours=1)
        
        return rates
    
    async def _fetch_rates(self, base_currency: str) -> Dict[str, float]:
        """
        從 API 獲取匯率
        """
        try:
            # 使用免費匯率 API (實際生產環境建議使用付費 API)
            url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('rates', self.base_rates)
        except Exception as e:
            print(f"匯率 API 錯誤：{e}")
            return self.base_rates
    
    async def convert_to_currencies(
        self, 
        prices: List[Dict], 
        target_currencies: List[str]
    ) -> Dict[str, float]:
        """
        將價格列表轉換為目標貨幣
        
        Args:
            prices: 價格列表 [{price, currency}, ...]
            target_currencies: 目標貨幣列表 ['MOP', 'HKD', 'RMB']
            
        Returns:
            Dict: {MOP: 平均價格，HKD: 平均價格，...}
        """
        result = {}
        
        for target in target_currencies:
            converted_prices = []
            
            for price_info in prices:
                price = price_info.get('price', 0)
                from_currency = price_info.get('currency', 'USD')
                
                # 轉換為目標貨幣
                converted = await self.convert(price, from_currency, target)
                converted_prices.append(converted)
            
            # 計算平均價格
            if converted_prices:
                result[target] = sum(converted_prices) / len(converted_prices)
            else:
                result[target] = 0.0
        
        return result
    
    async def convert(
        self, 
        amount: float, 
        from_currency: str, 
        to_currency: str
    ) -> float:
        """
        單筆貨幣轉換
        
        Args:
            amount: 金額
            from_currency: 原貨幣
            to_currency: 目標貨幣
            
        Returns:
            float: 轉換後金額
        """
        if from_currency == to_currency:
            return amount
        
        # 獲取匯率
        rates = await self.get_rates(from_currency)
        
        # 計算轉換
        rate = rates.get(to_currency, 1.0)
        return amount * rate
    
    def get_currency_info(self, currency_code: str) -> Dict:
        """
        獲取貨幣信息
        
        Args:
            currency_code: 貨幣代碼
            
        Returns:
            Dict: {name, symbol, decimal_places}
        """
        currency_info = {
            'MOP': {'name': '澳門元', 'symbol': 'MOP$', 'decimal_places': 2},
            'HKD': {'name': '港幣', 'symbol': 'HK$', 'decimal_places': 2},
            'RMB': {'name': '人民幣', 'symbol': '¥', 'decimal_places': 2},
            'CNY': {'name': '人民幣', 'symbol': '¥', 'decimal_places': 2},
            'USD': {'name': '美元', 'symbol': '$', 'decimal_places': 2},
            'JPY': {'name': '日圓', 'symbol': '¥', 'decimal_places': 0},
        }
        
        return currency_info.get(currency_code, {
            'name': currency_code,
            'symbol': '',
            'decimal_places': 2
        })


if __name__ == "__main__":
    service = CurrencyConverterService()
    print("Currency Converter Service initialized")
