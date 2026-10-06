import os
import shutil
import subprocess
import json
import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
TOKEN = "8317502262:AAHY_u0-UI4Gmo0dd0a_WzbDI2yKCjzdTmk"
bot = telebot.TeleBot(TOKEN)




M_FILE_PATH = 'FPSDisplay.m'
BACKUP_FILE_PATH = 'FPSDisplay.m.bak'

ZALO_GROUP_URL = 'https://zalo.me/g/jefec961jzjcav3izyxo'
VERIFY_FILE = os.path.join(os.path.dirname(__file__), 'verified_users.json')


def load_verified():
    try:
        with open(VERIFY_FILE, 'r', encoding='utf-8') as f:
            return set(str(x) for x in json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_verified(users):
    with open(VERIFY_FILE, 'w', encoding='utf-8') as f:
        json.dump(sorted(users), f, ensure_ascii=False, indent=2)


def join_keyboard():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton('📱 VÀO NHÓM ZALO', url=ZALO_GROUP_URL))
    kb.row(InlineKeyboardButton('✅ TÔI ĐÃ VÀO NHÓM', callback_data='verify_zalo'))
    return kb


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Chào Mày, Tao Là Bot Chuyên Độ FPS Cho Theos Đây\n\n"
        "⚠️ Trước khi dùng /fps, bắt buộc vào nhóm Zalo.\n"
        "Vào nhóm rồi bấm nút xác nhận bên dưới.",
        reply_markup=join_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data == 'verify_zalo')
def verify_zalo(call):
    users = load_verified()
    users.add(str(call.from_user.id))
    save_verified(users)
    bot.answer_callback_query(call.id, "Đã xác nhận. Bạn có thể dùng /fps.", show_alert=True)
    bot.send_message(call.message.chat.id, "✅ Đã xác nhận.\n\nDùng: /fps {Tên_FPS}")


@bot.message_handler(commands=['fps'])
def handle_fps(message):
    if str(message.from_user.id) not in load_verified():
        bot.reply_to(
            message,
            "🔒 Chưa được phép make FPS.\n\n"
            "Bắt buộc vào nhóm Zalo trước, sau đó bấm "
            "\"TÔI ĐÃ VÀO NHÓM\".",
            reply_markup=join_keyboard()
        )
        return

    try:
        args = message.text.split(' ', 1)
        if len(args) != 2 or not args[1].strip():
            bot.reply_to(message, "Gõ: /fps {Tên_FPS}")
            return

        fps_name = args[1].strip().replace('\r', ' ').replace('\n', ' ')
        backup_m_file()

        try:
            modify_m_file(fps_name)
            msg = bot.reply_to(message, "Đang Cày, Ngồi Đợi Xíu Nha Mày")
            if not run_make_commands(msg):
                bot.edit_message_text(
                    "❌ Build thất bại. Kiểm tra log Make/Theos.",
                    chat_id=msg.chat.id, message_id=msg.message_id
                )
                return
            send_dylib_file(message, msg, fps_name)
        finally:
            restore_m_file()

    except Exception as e:
        bot.reply_to(message, f"Toang Rồi Mày Ơi: {e}")


def backup_m_file():
    shutil.copy(M_FILE_PATH, BACKUP_FILE_PATH)


def restore_m_file():
    shutil.copy(BACKUP_FILE_PATH, M_FILE_PATH)


def modify_m_file(fps_name):
    with open(M_FILE_PATH, 'r', encoding='utf-8') as file:
        content = file.read()

    new_content = content.replace(
        '@" %d FPS | %@ | Pin: %0.0f  Hello World "',
        f'@" %d FPS | %@ | Pin: %0.0f  {fps_name}"'
    )

    with open(M_FILE_PATH, 'w', encoding='utf-8') as file:
        file.write(new_content)


def run_make_commands(msg):
    subprocess.run(
        ['make', 'clean'],
        cwd=os.path.dirname(M_FILE_PATH),
        text=True,
        capture_output=True
    )

    make_process = subprocess.Popen(
        ['make'],
        cwd=os.path.dirname(M_FILE_PATH),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    steps = 10
    current_step = 0

    while True:
        output = make_process.stdout.readline()
        if output == '' and make_process.poll() is not None:
            break

        if output:
            current_step += 1
            progress = min(90, int((current_step / steps) * 90))
            try:
                bot.edit_message_text(
                    f"⚙️ Đang Make FPS: {progress}%",
                    chat_id=msg.chat.id,
                    message_id=msg.message_id
                )
            except Exception:
                pass

    return make_process.wait() == 0


def send_dylib_file(message, msg, fps_name):
    dylib_path = os.path.join(
        os.path.dirname(M_FILE_PATH),
        '.theos', 'obj', 'debug', 'NguyenThanhHung.dylib'
    )

    if not os.path.exists(dylib_path):
        raise FileNotFoundError(f"Không tìm thấy file dylib: {dylib_path}")

    with open(dylib_path, 'rb') as dylib_file:
        bot.send_document(
            message.chat.id,
            dylib_file,
            caption=f"✅ Xong 100%!\n🎮 FPS: {fps_name}\n📦 File dylib đã được gửi."
        )

    try:
        bot.edit_message_text(
            "✅ Xong 100% rồi nha, file đã gửi.",
            chat_id=msg.chat.id,
            message_id=msg.message_id
        )
    except Exception:
        pass


bot.polling()
