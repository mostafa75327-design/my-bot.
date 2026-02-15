import telebot, requests, base64

TOKEN = "8555031080:AAHKv_xFrNa2POPRPN9eI4TMjXAmEw1XLTw"
GEMINI_KEY = "AIzaSyB-VG4ARH1P1GqXcsp1C9x2e8a1VpT6QE8"

bot = telebot.TeleBot(TOKEN)
user_storage = {}

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    user_storage[message.chat.id] = base64.b64encode(bot.download_file(file_info.file_path)).decode('utf-8')
    bot.reply_to(message, "Nano Banana 3 Pro: Image received. Send instructions.")

@bot.message_handler(func=lambda m: True)
def process_ai(message):
    if message.chat.id not in user_storage:
        bot.reply_to(message, "Upload a photo first.")
        return
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        payload = {"contents": [{"parts": [{"text": f"System: Gemini 3.0 mode. BRIEF ENGLISH ONLY. Task: {message.text}"}, {"inline_data": {"mime_type": "image/jpeg", "data": user_storage[message.chat.id]}}]}]}
        answer = requests.post(url, json=payload).json()['candidates'][0]['content']['parts'][0]['text']
        bot.reply_to(message, answer)
    except:
        bot.reply_to(message, "Error. Try again.")

bot.infinity_polling()
