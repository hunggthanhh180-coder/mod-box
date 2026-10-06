import os, shutil, subprocess, json, telebot, re, unicodedata

TOKEN="8317502262:AAHY_u0-UI4Gmo0dd0a_WzbDI"
bot=telebot.TeleBot(TOKEN)

def to_safe(name):
  n=unicodedata.normalize('NFD',name).encode('ascii','ignore').decode('utf-8')
  n=re.sub(r'[^A-Za-z0-9]','',n)
  return n or "120FPS"

def build_deb(fps_name, safe_name, user_id):
  base=f"/tmp/fps_{user_id}"
  if os.path.exists(base): shutil.rmtree(base)
  deb_root=os.path.join(base,"deb")
  debian_path=os.path.join(deb_root,"DEBIAN")
  os.makedirs(debian_path, exist_ok=True)
  lib=os.path.join(deb_root,"Library/MobileSubstrate/DynamicLibraries")
  os.makedirs(lib, exist_ok=True)

  safe_low=safe_name.lower()
  control=f"""Package: com.modbox.{safe_low}
Name: {fps_name}
Version: 1.0
Architecture: iphoneos-arm
Description: Unlock {fps_name}
Maintainer: mod-box
Section: Tweaks
Depends: mobilesubstrate
"""
  cf=os.path.join(debian_path,"control")
  with open(cf,"w",newline="\n") as f:
    f.write(control.strip()+"\n\n")
  os.chmod(debian_path,0o755)
  os.chmod(cf,0o644)
  os.chmod(deb_root,0o755)
  subprocess.run(["chmod","-R","0755",lib],check=True)
  out=os.path.join(base,f"{safe_name}.deb")
  subprocess.run(["dpkg-deb","--build",deb_root,out],check=True)
  return out

@bot.message_handler(commands=['fps'])
def handle(m):
  try:
    parts=m.text.split(" ",1)
    if len(parts)<2: return bot.reply_to(m,"Dung: /fps 120FPS")
    fps_name=parts[1].strip()
    safe=to_safe(fps_name)
    bot.reply_to(m,f"⌛ Đang Cày: {safe}")
    deb=build_deb(fps_name,safe,m.from_user.id)
    with open(deb,"rb") as f: bot.send_document(m.chat.id,f,caption=f"✅ {safe}.deb")
  except Exception as e:
    bot.reply_to(m,f"❌ Lỗi: {e}")

print("Bot chay...")
bot.infinity_polling()
