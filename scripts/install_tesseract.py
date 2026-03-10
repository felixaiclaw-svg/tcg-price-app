"""
Tesseract OCR 自動安裝腳本
"""
import urllib.request
import os
import sys
import subprocess

def download_tesseract():
    """下載 Tesseract 安裝程式"""
    url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.exe"
    temp_dir = os.environ.get('TEMP', 'C:\\Windows\\Temp')
    installer_path = os.path.join(temp_dir, 'tesseract-installer.exe')
    
    print(f"正在下載 Tesseract OCR...")
    print(f"來源：{url}")
    print(f"目標：{installer_path}")
    
    try:
        urllib.request.urlretrieve(url, installer_path)
        print(f"✓ 下載完成！")
        return installer_path
    except Exception as e:
        print(f"✗ 下載失敗：{e}")
        return None

def install_tesseract(installer_path):
    """安裝 Tesseract"""
    if not os.path.exists(installer_path):
        print("✗ 安裝程式不存在")
        return False
    
    print("\n正在安裝 Tesseract OCR...")
    print("(這可能需要幾分鐘)")
    
    # 靜默安裝
    install_cmd = f'"{installer_path}" /SILENT /SUPPRESSMSGBOXES /NORESTART'
    
    try:
        subprocess.run(install_cmd, shell=True, check=True)
        print("✓ 安裝完成！")
        return True
    except Exception as e:
        print(f"✗ 安裝失敗：{e}")
        return False

def verify_installation():
    """驗證安裝"""
    print("\n驗證安裝...")
    
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    if os.path.exists(tesseract_path):
        print(f"✓ Tesseract 已安裝：{tesseract_path}")
        
        # 檢查版本
        try:
            result = subprocess.run([tesseract_path, "--version"], 
                                  capture_output=True, text=True)
            print(f"✓ 版本：{result.stdout.split()[0] if result.stdout else 'Unknown'}")
        except:
            print("✓ 已安裝 (無法檢查版本)")
        
        return True
    else:
        print("✗ Tesseract 未找到")
        return False

def main():
    print("=" * 60)
    print("  Tesseract OCR 自動安裝程式")
    print("=" * 60)
    print()
    
    # 1. 下載
    installer_path = download_tesseract()
    if not installer_path:
        print("\n請手動下載並安裝:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    
    # 2. 安裝 (需要用戶確認)
    print("\n準備安裝 Tesseract OCR")
    print("安裝後請重啟終端機")
    
    # 3. 驗證
    if verify_installation():
        print("\n" + "=" * 60)
        print("  ✓ Tesseract OCR 安裝完成！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 重啟終端機")
        print("2. 運行：tesseract --list-langs")
        print("3. 測試 TCG Price Scanner")
        return True
    else:
        print("\n請手動安裝:")
        print(f"運行：{installer_path}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
