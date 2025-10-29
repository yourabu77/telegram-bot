from aiogram import Bot, Dispatcher, types
from aiohttp import web
import asyncio
import os

API_TOKEN = "8238182597:AAEOe784Eoai7n7v7d2xoeyfTsFpznjuTkk"

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- START komandasi ---
@dp.message()
async def handler(message: types.Message):
    if message.text == "/start":
        text = (
            "👋 <b>Xush kelibsiz!</b>\n\n"
            "🇩🇪 <b>Nemis–O‘zbek Tarjimon Bot</b> sizga yordam beradi!\n\n"
            "📋 <b>Mavjud komandalar:</b>\n"
            "• /about – Bot haqida ma’lumot\n"
            "• /settings – Tarjima yo‘nalishini tanlash\n\n"
            "🧠 Matn yuboring — bot uni avtomatik tarjima qiladi!"
        )
        await message.answer(text, parse_mode="HTML")

    elif message.text == "/about":
        text = (
            "ℹ️ <b>Bot haqida</b>\n\n"
            "🤖 <b>Nom:</b> Nemis–O‘zbek Tarjimon Bot\n"
            "⏰ <b>Holat:</b> 24/7 onlayn ishlaydi\n"
            "🧩 <b>Texnologiya:</b> Python + Aiogram + Render Webhook\n"
            "📦 <b>Versiya:</b> 2.2 (2025)\n\n"
            "👨‍💻 <b>Dasturchi:</b> "
            "<a href='https://t.me/yourabu'>@yourabu</a>"
        )
        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

    elif message.text == "/settings":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("🇩🇪 Nemis ➜ O‘zbek", callback_data="de_to_uz"),
            types.InlineKeyboardButton("🇺🇿 O‘zbek ➜ Nemis", callback_data="uz_to_de"),
        )
        await message.answer("⚙️ Tarjima yo‘nalishini tanlang:", reply_markup=keyboard)

    else:
        await message.answer("Matn yuboring, men uni tarjima qilib beraman 😊")


# --- Webhook funksiyalar ---
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook o‘rnatildi: {WEBHOOK_URL}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def handle(request):
    update = await request.json()
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)
    return web.Response()


# --- Asosiy ishga tushirish funksiyasi ---
def start():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    port = int(os.getenv("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()
