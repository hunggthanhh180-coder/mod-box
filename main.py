import os, shutil, subprocess, json, telebot
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
def join_keyboard():
 m=InlineKeyboardMarkup()
 m.add(InlineKeyboardButton("Vao nhom Zalo",url="https://zalo.me/g/xxxx"))
 m.add(InlineKeyboardButton("Xac nhan",callback_data='verify_zalo'))
 return m
@bot.message_handler(commands=['start'])
def w(m): bot.reply_to(m,"Bot FPS",reply_markup=join_keyboard())
@bot.callback_query_handler(func=lambda call: call.data=='verify_zalo')
def v(call):
 users=load_verified();users.add(str(call.from_user.id));save_verified(users)
 bot.send_message(call.message.chat.id,"Xong, /fps Ten")
@bot.message_handler(commands=['fps'])
def handle_fps(message):
 parts=message.text.split(maxsplit=1)
 if len(parts)<2: return
 fps_name=parts[1].strip()
 bot.reply_to(message,f"Dang Cay: {fps_name}")
 try:
  build_root=f"/tmp/fps_{message.from_user.id}"
  if os.path.exists(build_root): shutil.rmtree(build_root)
  deb_dir=os.path.join(build_root,"deb")
  dylib_path=os.path.join(deb_dir,"Library/MobileSubstrate/DynamicLibraries")
  debian_path=os.path.join(deb_dir,"DEBIAN")
  os.makedirs(dylib_path,exist_ok=True);os.makedirs(debian_path,exist_ok=True)
  safe="".join(c for c in fps_name if c.isalnum()) or "FPS"
  dylib_file=os.path.join(dylib_path,"FPSDisplay.dylib")
  with open(dylib_file,'wb') as out: out.write(b"dummy "+fps_name.encode())
  with open(os.path.join(debian_path,"control"),'w',newline='\n') as cf: cf.write(f"Package: com.hung.fps{safe.lower()}\nName: {fps_name}\nVersion: 1.0-1\nArchitecture: iphoneos-arm\nDescription: {fps_name}\nMaintainer: Hung\nSection: Tweaks\nDepends: mobilesubstrate\n")
  subprocess.run(["chmod","-R","0755",deb_dir],check=True)
  subprocess.run(["chmod","0644",os.path.join(debian_path,"control")],check=True)
  subprocess.run(["chmod","0644",dylib_file],check=True)
  subprocess.run(["chmod","0755",debian_path],check=True)
  deb_output=f"/tmp/{safe}.deb"
  subprocess.run(["fakeroot","dpkg-deb","-b",deb_dir,deb_output],check=True)
  with open(deb_output,'rb') as df: bot.send_document(message.chat.id,df,caption=f"Xong: {fps_name}")
 except Exception as e: bot.reply_to(message,f"Loi: {e}")
print("Bot dang chay...")
bot.infinity_polling()
