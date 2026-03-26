import telebot
import google.generativeai as genai
import os

TOKEN = '8761014188:AAGAHB4QMpeHiLfRWl0FecNpzSEIAJ4XIVE'
KEY = 'AIzaSyBiLJ-8jVhjE6Vl6RswuInXk-ivoWdmhEM'

genai.configure(api_key=KEY)
bot = telebot.TeleBot(TOKEN)

PROMPTS = {
    'study': "Ты строгий агроном для Алины. Помогай с учебой.",
    'ririn': "Ты Ририн. Белый хвост. 3-е лицо.",
    'lis': "Ты дерзкая Лисичка. Звуки 'мгнх', 'ф-ф'."
}

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Инструкция: {PROMPTS['lis']}. Алина пишет: {m.text}")
        bot.send_message(m.chat.id, res.text)
    except:
        bot.send_message(m.chat.id, "Лисичка спит... Попробуй позже.")

if __name__ == "__main__":
    bot.infinity_polling()
