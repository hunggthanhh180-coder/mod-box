import os, shutil, subprocess, json, telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8317502262:AAHY_u0-UI4Gmo0dd0a_WzbDI2yKCjzdTmk"
bot = telebot.TeleBot(TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'FPSDisplay.m')
VERIFIED_FILE = os.path.join(BASE_DIR, 'verified_users.json')

def load_verified():
    if not os.path.exists(VERIFIED_FILE): return set()
    try:
        with open(VERIFIED_FILE, 'r') as f: return set(json.load(f))
    except: return set()

def save_verified(users):
    with open(VERIFIED_FILE, 'w') as f: json.dump(list(users), f)

def join_keyboard():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔗 Vào nhóm Zalo", url="https://zalo.me/g/xxxx"))
    m.add(InlineKeyboardButton("✅ Xác nhận", callback_data='verify_zalo'))
    return m

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào Mày, Tao Là Bot Độ FPS\n\n⚠️ Gõ /start và xác nhận Zalo trước khi dùng /fps", reply_markup=join_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == 'verify_zalo')
def verify_zalo(call):
    users = load_verified(); users.add(str(call.from_user.id)); save_verified(users)
    bot.answer_callback_query(call.id, "Đã xác nhận!", show_alert=True)
    bot.send_message(call.message.chat.id, "✅ Đã xác nhận. Dùng: /fps {Tên}")

@bot.message_handler(commands=['fps'])
def handle_fps(message):
    users = load_verified()
    if str(message.from_user.id) not in users:
        bot.reply_to(message, "❌ Chưa xác nhận. Gõ /start"); return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Dùng: /fps 120FPS"); return
    fps_name = parts[1].strip()
    bot.reply_to(message, f"⏳ Đang Cày: {fps_name}")
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        new_content = content.replace("FPS_PLACEHOLDER", fps_name).replace("120 FPS", fps_name)
        if new_content == content:
            new_content = f'// {fps_name}\n#define CUSTOM_FPS_NAME @"{fps_name}"\n' + content

        build_root = f"/tmp/fps_{message.from_user.id}"
        if os.path.exists(build_root): shutil.rmtree(build_root)
        deb_dir = os.path.join(build_root, "deb")
        dylib_path = os.path.join(deb_dir, "Library/MobileSubstrate/DynamicLibraries")
        debian_path = os.path.join(deb_dir, "DEBIAN")
        os.makedirs(dylib_path, exist_ok=True)
        os.makedirs(debian_path, exist_ok=True)

        with open(os.path.join(dylib_path, "FPSDisplay.m"), 'w', encoding='utf-8') as out:
            out.write(new_content)
        with open(os.path.join(dylib_path, "FPSDisplay.dylib"), 'wb') as out:
            out.write(b"dummy " + fps_name.encode())

        safe = "".join(c for c in fps_name if c.isalnum()) or "FPS"
        control = f"Package: com.hung.fps{safe.lower()}\nName: {fps_name}\nVersion: 1.0\nArchitecture: iphoneos-arm\nDescription: {fps_name}\nMaintainer: Hung\n"
        with open(os.path.join(debian_path, "control"), 'w') as cf: cf.write(control)

        deb_output = f"/tmp/{safe}.deb"
        subprocess.run(["dpkg-deb", "--build", deb_dir, deb_output], check=True)
        with open(deb_output, 'rb') as df:
            bot.send_document(message.chat.id, df, caption=f"✅ Xong: {fps_name}")
        shutil.rmtree(build_root, ignore_errors=True)
        os.remove(deb_output)
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {e}")

print("Bot đang chạy...")
bot.infinity_polling()
