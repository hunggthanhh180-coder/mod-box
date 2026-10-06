import os, shutil, subprocess, json, telebot, re, unicodedata
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN="8317502262:AAHY_u0-UI4Gmo0dd0a_WzbDI2yKCjzdTmk"
bot=telebot.TeleBot(TOKEN)
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
VERIFIED_FILE=os.path.join(BASE_DIR,'verified_users.json')

def load_verified():
 try:
  with open(VERIFIED_FILE,'r') as f: return set(json.load(f))
 except: return set()
def save_verified(u):
 with open(VERIFIED_FILE,'w') as f: json.dump(list(u),f)

def to_safe(name):
    n = unicodedata.normalize('NFD', name)
    n = n.encode('ascii','ignore').decode('ascii')
    n = re.sub(r'[^A-Za-z0-9]', '', n)
    return n or "120FPS"

    bot.reply_to(message,"Dùng: /fps 120FPS");return
 fps_name=parts[1].strip()
 safe=to_safe(fps_name)
 bot.reply_to(message,f"⏳ Đang build: {fps_name} -> {safe}")
 try:
  build_root=f"/tmp/fps_{message.from_user.id}"
  if os.path.exists(build_root): shutil.rmtree(build_root)
  deb_dir=os.path.join(build_root,"deb")
  dylib_path=os.path.join(deb_dir,"Library/MobileSubstrate/DynamicLibraries")
  debian_path=os.path.join(deb_dir,"DEBIAN")
  os.makedirs(dylib_path,exist_ok=True)
  os.makedirs(debian_path,exist_ok=True)
  with open(os.path.join(dylib_path,"FPSDisplay.dylib"),'wb') as out:
    out.write(b"dummy "+fps_name.encode())
  control=f"Package: com.hung.fps{safe.lower()}\nName: {fps_name}\nVersion: 1.0\nArchitecture: iphoneos-arm\nDescription: {fps_name}\nMaintainer: Hung\n"
  with open(os.path.join(debian_path,"control"),'w',newline='\n',encoding='utf-8') as cf:
    cf.write(control)
  # FIX QUAN TRỌNG LỖI 756
  subprocess.run(["chmod","-R","0755",deb_dir],check=True)
  subprocess.run(["chmod","0644",os.path.join(debian_path,"control")],check=True)
  subprocess.run(["chmod","0644",os.path.join(dylib_path,"FPSDisplay.dylib")],check=True)

  deb_output=f"/tmp/{safe}.deb"
  if os.path.exists(deb_output): os.remove(deb_output)
  subprocess.run(["fakeroot","dpkg-deb","-b",deb_dir,deb_output],check=True)
  with open(deb_output,'rb') as df:
    bot.send_document(message.chat.id,df,caption=f"✅ Xong: {fps_name}")
 except Exception as e:
  bot.reply_to(message,f"❌ Lỗi: {e}")

#... giữ lại phần /start, verify zalo cũ của mày...
import telebot
@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m,"Bot FPS - go /fps 120FPS")

print("Bot dang chay...")
bot.infinity_polling()
