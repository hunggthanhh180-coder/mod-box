from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
TOKEN = os.getenv("TOKEN")
ITEMS = ["Mũ Tiểu Tiên","Nón TVC2","Áo TVC1","Quần Trẻ Trâu","Giày Hacker"]
KEYS = {"ThanhHungCteHiHi": {"max":200,"used":[]},"ThanhHungCteVcl":{"max":15,"used":[]}}
user_selected, user_activated = {}, {}
def box_key():
    return InlineKeyboardMarkup([[InlineKeyboardButton(f"🔑 {k}", callback_data=f"key_{k}")] for k in KEYS])
def box_mod(uid):
    sel = user_selected.get(uid,set())
    kb = [[InlineKeyboardButton(f"{'✅' if i in sel else '⬜'} {ITEMS[i]}", callback_data=f"mod_{i}")] for i in range(len(ITEMS))]
    kb.append([InlineKeyboardButton(f"📦 XUẤT FILE ({len(sel)})", callback_data="xuat")])
    return InlineKeyboardMarkup(kb)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_activated:
        await update.message.reply_text("🔒 Chọn Key:", reply_markup=box_key())
    else:
        await update.message.reply_text("Chọn mod:", reply_markup=box_mod(uid))
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id; data = q.data
    if data.startswith("key_"):
        user_activated[uid]=data[4:]; user_selected[uid]=set()
        await q.edit_message_text(f"✅ Kích hoạt {data[4:]}"); await q.message.reply_text("Chọn mod:", reply_markup=box_mod(uid))
    elif data.startswith("mod_"):
        i=int(data[4:]); user_selected.setdefault(uid,set())
        user_selected[uid].remove(i) if i in user_selected[uid] else user_selected[uid].add(i)
        await q.edit_message_reply_markup(reply_markup=box_mod(uid))
    elif data=="xuat":
        await q.message.reply_text(f"Đã chọn: {[ITEMS[i] for i in user_selected.get(uid,[])]}")
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle))
app.run_polling()
