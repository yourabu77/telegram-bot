from aiogram import Bot, Dispatcher, types
from aiohttp import web
from googletrans import Translator
import os

API_TOKEN = "8238182597:AAEOe784Eoai7n7v7d2xoeyfTsFpznjuTkk"

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
translator = Translator()

# Foydalanuvchi sozlamalari (tarjima yo‘nalishi)
user_settings = {}


@dp.message()
async def handler(message: types.Message):
    text = message.text
    user_id = message.from_user.id

    # --- START komandasi ---
    if text == "/start":
        await message.answer(
            "👋 <b>Assalomu alaykum!</b>\n\n"
            "🇩🇪 <b>Nemis–O‘zbek tarjimon botiga</b> xush kelibsiz!\n"
            "Bu bot sizga 24/7 tarjima xizmatini taqdim etadi.\n\n"
            "📜 <b>Mavjud buyruqlar:</b>\n\n"
            "💬 /start — Botni ishga tushirish va buyruqlar ro‘yxati\n"
            "⚙️ /settings — Tarjima yo‘nalishini tanlash\n"
            "ℹ️ /about — Bot haqida ma’lumot\n"
            "🆘 /help — Foydalanish bo‘yicha yordam\n\n"
            "👨‍💻 Dasturchi: <a href='https://t.me/yourabu'>@yourabu</a>",
            parse_mode="HTML"
        )

    elif text == "/help":
        await message.answer(
            "🆘 <b>Yordam</b>\n\n"
            "Siz shunchaki matn yuboring — bot uni avtomatik tarjima qiladi.\n"
            "Misollar:\n➡️ 'Wie geht’s?' → 'Qandaysiz?'\n➡️ 'Men yaxshi' → 'Ich bin gut'\n\n"
            "⚙️ Tilni o‘zgartirish uchun /settings buyrug‘idan foydalaning.",
            parse_mode="HTML"
        )

    elif text == "/about":
        await message.answer(
            "ℹ️ <b>Bot haqida</b>\n\n"
            "🤖 <b>Nom:</b> Nemis–O‘zbek Tarjimon Bot\n"
            "🧠 <b>Texnologiya:</b> Python + Aiogram + Googletrans\n"
            "📅 <b>Versiya:</b> 2.5 (2025)",
            parse_mode="HTML"
        )

    elif text == "/settings":
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="🇩🇪 Nemis ➜ O‘zbek", callback_data="lang_de_uz"),
                types.InlineKeyboardButton(text="🇺🇿 O‘zbek ➜ Nemis", callback_data="lang_uz_de")
            ]
        ])
        await message.answer("⚙️ <b>Tarjima yo‘nalishini tanlang:</b>", reply_markup=keyboard, parse_mode="HTML")

    else:
        direction = user_settings.get(user_id, "de_uz")
        try:
            if direction == "de_uz":
                result = translator.translate(text, src="de", dest="uz")
                await message.answer(f"🇩🇪➡️🇺🇿 <b>Tarjima:</b>\n{result.text}", parse_mode="HTML")
            else:
                result = translator.translate(text, src="uz", dest="de")
                await message.answer(f"🇺🇿➡️🇩🇪 <b>Übersetzung:</b>\n{result.text}", parse_mode="HTML")
        except Exception as e:
            await message.answer("❌ Tarjima vaqtida xatolik yuz berdi. Iltimos, qaytadan urinib ko‘ring.")
            print(e)


@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if callback.data == "lang_de_uz":
        user_settings[user_id] = "de_uz"
        await callback.message.edit_text("✅ Til yo‘nalishi: 🇩🇪 Nemis ➜ 🇺🇿 O‘zbek")
    elif callback.data == "lang_uz_de":
        user_settings[user_id] = "uz_de"
        await callback.message.edit_text("✅ Til yo‘nalishi: 🇺🇿 O‘zbek ➜ 🇩🇪 Nemis")


# --- Webhook ---
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook o‘rnatildi: {WEBHOOK_URL}")


async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()
    print("🛑 Bot to‘xtatildi")


async def handle(request):
    update = await request.json()
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)
    return web.Response()


def start():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    port = int(os.getenv("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()
