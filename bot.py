from aiogram import Bot, Dispatcher, types
from aiohttp import web
import asyncio
import os

API_TOKEN = "8238182597:AAEOe784Eoai7n7v7d2xoeyfTsFpznjuTkk"

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message()
async def handler(message: types.Message):
    if message.text == "/start":
        await message.answer("✅ Bot 24/7 ishlayapti! Xush kelibsiz 🇩🇪🇺🇿")
    else:
        await message.answer("Matn yuboring, men uni tarjima qilib beraman 😊")


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


def start():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    port = int(os.getenv("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)


if name == "__main__":
    start()
