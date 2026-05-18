import os
import random
import requests
import schedule
import time
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# جلب التوكن والمعرفات بأمان من إعدادات السيرفر (Environment Variables)
TOKEN = os.environ.get("BOT_TOKEN", "7573014274:AAGzqIfiFJTjw0UO4MLw57idOv2ng7EdRbw")
CHAT_ID = int(os.environ.get("CHAT_ID", -1001956872134))

bot = telebot.TeleBot(TOKEN)

# --- قاعدة بيانات البوت (الأذكار والرسائل) ---

love_quotes = [
    "الحب هو أن ترى النور في قلب شخص واحد فقط 💖",
    "أنت روحي وقلبي وكل حياتي ❤️",
    "كلما نظرت إليك، أدركت أن الحب أجمل شعور 💕"
]

morning_azkar = [
    "أعوذ بالله من الشيطان الرجيم، بسم الله الرحمن الرحيم 🌿\nاللّهُ لاَ إِلَـهَ إِلاَّ هُوَ الْحَيُّ الْقَيُّومُ...",
    "اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت... 🤲",
    "اللهم بك أصبحنا، وبك أمسينا، وبك نحيا، وبك نموت، وإليك النشور ☀️",
    "رضيت بالله رباً، وبالإسلام ديناً، وبمحمد صلى الله عليه وسلم نبياً 🌸"
]

evening_azkar = [
    "اللهم ما أمسى بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر 🌙",
    "أمسينا وأمسى الملك لله، والحمد لله لا إله إلا الله وحده لا شريك له... 💖",
    "بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العليم 🌿",
    "أعوذ بكلمات الله التامات من شر ما خلق 🌌"
]

aya_kursi = """اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ 
لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ 
لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ 
مَنْ ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ 
يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ 
وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ 
وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۚ 
وَلَا يَئُودُهُ حِفْظُهُمَا ۚ 
وهُوَ الْعَلِيُّ الْعَظِيمُ."""

islamic_motivation = [
    "لا تحزن، فالله معك دائمًا وفي أحلك الظروف يأتيك الفرج ☝️",
    "تذكر دائمًا: {فَإِنَّ مَعَ الْعُسْرِ يُسْرًا * إِنَّ مَعَ الْعُسْرِ يُسْرًا} 🌿",
    "أكثروا من الاستغفار؛ فإنه يفتح الأقفال ويشرح البال 🔑",
    "لو علم العبد كيف يدبر الله له الأمور، لبكى من الفرحة والاطمئنان 🌸"
]

advice_list = [
    "عامل الناس بأخلاقك وبما تحب أن يعاملوك به 🤝",
    "لا تؤجل عمل اليوم إلى الغد، فالوقت أنفاس لا تعود ⏳",
    "ابتسم دائمًا، فالحياة قصيرة ولا تستحق أن تحمل في قلبك هماً 😃",
    "اجعل لنفسك خبيئة من عمل صالح لا يعلمها إلا الله 🤫"
]

# --- وظائف إرسال الرسائل التلقائية (الصدقة الجارية) ---

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error sending automatic message: {e}")

def morning_message():
    text = (
        "☀️ *صباح الخير والبركة* ☀️\n\n"
        "🌿 *صدقة جارية* 🌿\n"
        "أسأل الله لكم في هذا الصباح يوماً مليئاً بالخير، التوفيق، والرضا. "
        "اللهم اجعلنا واياكم من الذاكرين الشاكرين 🌸\n\n"
        f"📿 ذكر الصباح اليوم:\n{random.choice(morning_azkar)}"
    )
    send_message(text)

def evening_message():
    text = (
        "🌙 *مساء الخير والسكينة* 🌙\n\n"
        "🌹 *صدقة جارية* 🌹\n"
        "أسأل الله أن يجعل ليلتكم هادئة وسعيدة، وأن يغفر لنا ولكم ويسر أموركم دائمًا وعافاكم 🌼\n\n"
        f"🌌 ذكر المساء اليوم:\n{random.choice(evening_azkar)}"
    )
    send_message(text)

# جدولة الرسائل التلقائية (تأكد من ضبط توقيت السيرفر)
schedule.every().day.at("06:00").do(morning_message)
schedule.every().day.at("18:00").do(evening_message)

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- أوامر البوت والتفاعل ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📿 أذكار الصباح", callback_data="morning_azkar"),
        InlineKeyboardButton("🌙 أذكار المساء", callback_data="evening_azkar")
    )
    markup.add(
        InlineKeyboardButton("📖 آية الكرسي", callback_data="aya_kursi")
    )
    markup.add(
        InlineKeyboardButton("📖 تحفيز ديني", callback_data="islamic_motivation"),
        InlineKeyboardButton("💡 نصائح", callback_data="advice")
    )
    markup.add(
        InlineKeyboardButton("المزيد 💕", callback_data="more_love")
    )
    # زر الإنستجرام الخاص بك
    markup.add(
        InlineKeyboardButton("📸 إنستجرام", url="https://www.instagram.com/amen_1x/profilecard/?igsh=cXczcjE4d3pjeTQ5")
    )
    
    welcome_text = "مرحباً بك في البوت 🤍\n\nاختر أحد الخيارات من القائمة أدناه لقراءة الأذكار أو التحفيز (تذكر: الدال على الخير كفاعله) ✨:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == "morning_azkar":
            bot.send_message(call.message.chat.id, f"📿 *ذكر الصباح:*\n\n{random.choice(morning_azkar)}", parse_mode="Markdown")
        elif call.data == "evening_azkar":
            bot.send_message(call.message.chat.id, f"🌙 *ذكر المساء:*\n\n{random.choice(evening_azkar)}", parse_mode="Markdown")
        elif call.data == "aya_kursi":
            bot.send_message(call.message.chat.id, f"📖 *آية الكرسي:*\n\n{aya_kursi}")
        elif call.data == "islamic_motivation":
            bot.send_message(call.message.chat.id, f"📖 *تحفيز ديني:*\n\n{random.choice(islamic_motivation)}")
        elif call.data == "advice":
            bot.send_message(call.message.chat.id, f"💡 *نصيحة اليوم:*\n\n{random.choice(advice_list)}")
        elif call.data == "more_love":
            bot.send_message(call.message.chat.id, f"💖 *رسالة حب:*\n\n{random.choice(love_quotes)}")
        
        # إنهاء حالة التحميل للزر في تليجرام
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Callback error: {e}")

def run_bot():
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Bot polling crashed, restarting... Error: {e}")
            time.sleep(5)

# --- Flask Server لضمان استمرارية التشغيل 24 ساعة ---
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>البوت شغال بنجاح وجاري إرسال الصدقة الجارية والرسائل المجدولة! ✅</h1>"

if __name__ == "__main__":
    # تشغيل خيوط الخلفية (Threads)
    threading.Thread(target=schedule_checker, daemon=True).start()
    threading.Thread(target=run_bot, daemon=True).start()
    
    # تشغيل السيرفر على البورت المطلوب لـ Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)