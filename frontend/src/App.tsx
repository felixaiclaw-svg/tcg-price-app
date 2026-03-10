import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

interface PriceInfo {
  website: string;
  price: number;
  currency: string;
  url: string;
  last_updated: string;
}

interface CardData {
  card_name: string;
  card_set: string;
  card_number: string;
  language: string;
  prices: PriceInfo[];
  converted_prices: {
    MOP: number;
    HKD: number;
    RMB: number;
  };
}

function App() {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CardData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedCurrency, setSelectedCurrency] = useState<'MOP' | 'HKD' | 'RMB'>('MOP');
  
  // 手動輸入/編輯狀態
  const [showManualInput, setShowManualInput] = useState(false);
  const [manualCardName, setManualCardName] = useState('');
  const [manualCardNumber, setManualCardNumber] = useState('');
  const [manualCardSet, setManualCardSet] = useState('');
  const [manualLanguage, setManualLanguage] = useState('EN');

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleScan = async () => {
    if (!image) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setShowManualInput(false);

    try {
      const formData = new FormData();
      formData.append('image', image);
      formData.append('target_currency', selectedCurrency);

      const response = await axios.post(`${API_URL}/card/scan`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // 檢查是否需要手動輸入
      if (response.data.needs_manual_input || response.data.card_name === 'Unknown') {
        setShowManualInput(true);
        setManualCardName('');
        setManualCardNumber(response.data.card_number !== 'Unknown' ? response.data.card_number : '');
        setManualCardSet('');
        setError('⚠️ AI 無法完全識別卡牌，請手動輸入卡牌信息');
      } else {
        setResult(response.data);
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || '掃描失敗，請重試';
      setError(errorMsg);
      
      // 如果是識別失敗，顯示手動輸入
      if (errorMsg.includes('識別') || errorMsg.includes('置信度')) {
        setShowManualInput(true);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleManualSubmit = async () => {
    if (!manualCardName && !manualCardNumber) {
      setError('請至少輸入卡牌名稱或編號');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        card_name: manualCardName || 'Unknown',
      });
      if (manualCardNumber) params.append('card_number', manualCardNumber);
      if (manualCardSet) params.append('card_set', manualCardSet);
      if (manualLanguage) params.append('language', manualLanguage);

      const response = await axios.get(`${API_URL}/card/prices?${params.toString()}`);
      setResult(response.data);
      setShowManualInput(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || '未找到價格信息，請檢查輸入');
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price: number, currency: string) => {
    const symbols: Record<string, string> = {
      MOP: 'MOP$',
      HKD: 'HK$',
      RMB: '¥',
      USD: '$',
      JPY: '¥',
      CNY: '¥',
    };
    return `${symbols[currency] || currency}${price.toFixed(2)}`;
  };

  const handleManualSearch = async () => {
    if (!manualCardName.trim()) {
      setError('請輸入卡牌名稱');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/card/manual`, {
        card_name: manualCardName,
        card_number: manualCardNumber || undefined,
        card_set: manualCardSet || undefined,
        game: 'PTCG',
        language: manualLanguage,
      }, {
        params: {
          target_currency: selectedCurrency,
        },
      });

      setResult(response.data);
      setShowManualInput(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || '查詢失敗，請重試');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            🃏 TCG Price Scanner
          </h1>
          <p className="text-purple-200">
            上傳卡牌圖片，即時查詢全網價格
          </p>
        </header>

        {/* Upload Section */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 mb-6">
          <div className="flex flex-col items-center">
            {/* Preview */}
            {preview && (
              <div className="mb-4 relative">
                <img
                  src={preview}
                  alt="Preview"
                  className="max-h-64 rounded-lg shadow-lg"
                />
                <button
                  onClick={() => {
                    setImage(null);
                    setPreview(null);
                  }}
                  className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600"
                >
                  ✕
                </button>
              </div>
            )}

            {/* Upload Button */}
            <label className="cursor-pointer bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-4 rounded-xl font-semibold hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 shadow-lg">
              <input
                type="file"
                accept="image/*"
                capture="environment"
                onChange={handleImageSelect}
                className="hidden"
              />
              📸 {preview ? '重新上傳' : '上傳/拍攝卡牌'}
            </label>

            {/* Currency Selection */}
            <div className="mt-4 flex gap-2">
              {(['MOP', 'HKD', 'RMB'] as const).map((currency) => (
                <button
                  key={currency}
                  onClick={() => setSelectedCurrency(currency)}
                  className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                    selectedCurrency === currency
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {currency}
                </button>
              ))}
            </div>

            {/* Scan Button */}
            <button
              onClick={handleScan}
              disabled={!image || loading}
              className={`mt-6 w-full max-w-md py-4 rounded-xl font-bold text-lg transition-all ${
                image && !loading
                  ? 'bg-gradient-to-r from-green-500 to-teal-500 text-white hover:from-green-600 hover:to-teal-600 transform hover:scale-105'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              {loading ? '🔄 掃描中...' : '🔍 開始掃描'}
            </button>

            {/* Manual Input Toggle */}
            <div className="mt-4 text-center">
              <p className="text-gray-500 mb-2">或</p>
              <button
                onClick={() => setShowManualInput(!showManualInput)}
                className="text-purple-600 hover:text-purple-800 font-semibold underline"
              >
                {showManualInput ? '返回圖片掃描' : '✍️ 手動輸入卡牌信息'}
              </button>
            </div>
          </div>
        </div>

        {/* Manual Input Form */}
        {showManualInput && (
          <div className="bg-yellow-50 border border-yellow-300 rounded-xl p-6 mb-6">
            <h3 className="text-lg font-semibold text-yellow-800 mb-4">
              ✍️ 手動輸入卡牌信息
            </h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  卡牌名稱 *
                </label>
                <input
                  type="text"
                  value={manualCardName}
                  onChange={(e) => setManualCardName(e.target.value)}
                  placeholder="例如：Pikachu"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  卡牌編號
                </label>
                <input
                  type="text"
                  value={manualCardNumber}
                  onChange={(e) => setManualCardNumber(e.target.value)}
                  placeholder="例如：153/SV-P"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  系列
                </label>
                <input
                  type="text"
                  value={manualCardSet}
                  onChange={(e) => setManualCardSet(e.target.value)}
                  placeholder="例如：Scarlet & Violet"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  語言
                </label>
                <select
                  value={manualLanguage}
                  onChange={(e) => setManualLanguage(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                >
                  <option value="EN">英文</option>
                  <option value="ZH-HK">繁體中文</option>
                  <option value="ZH-CN">簡體中文</option>
                  <option value="JP">日文</option>
                  <option value="KO">韓文</option>
                </select>
              </div>
            </div>
            
            <button
              onClick={handleManualSubmit}
              disabled={loading || (!manualCardName && !manualCardNumber)}
              className={`mt-4 w-full py-3 rounded-lg font-semibold transition-all ${
                loading || (!manualCardName && !manualCardNumber)
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-purple-600 text-white hover:bg-purple-700'
              }`}
            >
              {loading ? '🔄 查詢中...' : '🔍 查詢價格'}
            </button>
            
            <button
              onClick={() => setShowManualInput(false)}
              className="mt-2 w-full py-2 text-gray-600 hover:text-gray-800"
            >
              取消
            </button>
          </div>
        )}

        {/* Error Message */}
        {error && !showManualInput && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-6 py-4 rounded-xl mb-6">
            ⚠️ {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="bg-white rounded-2xl shadow-2xl p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              📊 掃描結果
            </h2>

            {/* Card Info */}
            <div className="bg-purple-50 rounded-xl p-4 mb-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">卡牌名稱</p>
                  <p className="font-semibold text-gray-800">{result.card_name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">系列</p>
                  <p className="font-semibold text-gray-800">{result.card_set}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">編號</p>
                  <p className="font-semibold text-gray-800">{result.card_number}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">語言</p>
                  <p className="font-semibold text-gray-800">{result.language}</p>
                </div>
              </div>
            </div>

            {/* Converted Prices */}
            <div className="grid grid-cols-3 gap-4 mb-6">
              {Object.entries(result.converted_prices).map(([currency, price]) => (
                <div
                  key={currency}
                  className={`rounded-xl p-4 text-center ${
                    selectedCurrency === currency
                      ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white'
                      : 'bg-gray-100'
                  }`}
                >
                  <p className="text-sm opacity-80">{currency}</p>
                  <p className="text-2xl font-bold">{formatPrice(price, currency)}</p>
                </div>
              ))}
            </div>

            {/* Price Sources */}
            <h3 className="text-lg font-semibold text-gray-700 mb-3">
              🌐 價格來源
            </h3>
            <div className="space-y-2">
              {result.prices.map((priceInfo, index) => (
                <div
                  key={index}
                  className="flex justify-between items-center bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors"
                >
                  <div>
                    <p className="font-semibold text-gray-800">{priceInfo.website}</p>
                    <p className="text-sm text-gray-500">
                      更新：{new Date(priceInfo.last_updated).toLocaleString('zh-TW')}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-purple-600">
                      {formatPrice(priceInfo.price, priceInfo.currency)}
                    </p>
                    <a
                      href={priceInfo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-500 hover:underline"
                    >
                      查看詳情 →
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="text-center text-purple-200 text-sm mt-8">
          <p>支援：PTCG • OPCG • Yu-Gi-Oh! • MTG</p>
          <p className="mt-2">價格來源：eBay • snkrdunk • 集換社 • Mercari • yuyu-tei.jp</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
