import os
import telebot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from telebot import apihelper

# --- ПРОКСИ (БЕЗ НИХ НЕ РАБОТАЕТ) ---
proxy = 'http://proxy.server:3128'
apihelper.proxy = {'https': proxy}
os.environ['https_proxy'] = proxy
os.environ['http_proxy'] = proxy

TOKEN = '8761014188:AAGAHB4QMpeHiLfRWl0FecNpzSEIAJ4XIVE'
KEY = 'AIzaSyBiLJ-8jVhjE6Vl6RswuInXk-ivoWdmhEM'

genai.configure(api_key=KEY)
bot = telebot.TeleBot(TOKEN)

# Настройки персонажей
PROMPTS = {
    'study': "Ты строгий агроном для Алины. Помогай с учебой.",
    'ririn': "Ты Ририн. Ласковая, но строгая. Белый хвост. 3-е лицо.",
    'lis': "Ты дерзкая Лисичка. Звуки 'мгнх', 'ф-ф'."
}

user_modes = {}

@bot.message_handler(commands=['study', 'ririn', 'lis'])
def set_mode(m):
    user_modes[m.chat.id] = m.text[1:]
    bot.reply_to(m, f"✅ Режим {m.text[1:]} включен!")

@bot.message_handler(func=lambda m: True)
def handle(m):
    mode = user_modes.get(m.chat.id, 'lis')
    try:
        # ИСПРАВЛЕННОЕ НАЗВАНИЕ МОДЕЛИ ЗДЕСЬ:
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        
        res = model.generate_content(
            f"Системная установка: {PROMPTS[mode]}. Алина пишет: {m.text}"
        )
        bot.send_message(m.chat.id, res.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(m.chat.id, "Лисичка задумалась... Попробуй еще раз.")

if __name__ == "__main__":
    print("Попытка запуска №2...")
    bot.infinity_polling()
