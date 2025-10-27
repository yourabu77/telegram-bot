from aiogram import Bot, Dispatcher, types
import asyncio
from aiohttp import web

API_TOKEN = "SIZNING_BOT_TOKENINGIZ"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message()
async def handler(message: types.Message):
    if message.text == "/start":
        await message.answer("Assalomu alaykum! Botimiz 24/7 ishlayapti 🇩🇪🇺🇿")
    else:
        await message.answer("Matn yuboring, men tarjima qilib beraman 😊")

async def main():
    print("Bot ishga tushdi ✅")
    await dp.start_polling(bot)

async def handle(request):
    return web.Response(text="Bot ishlayapti ✅")

app = web.Application()
app.router.add_get("/", handle)

if __name__ == "__main__":
    asyncio.get_event_loop().create_task(main())
    web.run_app(app, host="0.0.0.0", port=8000)
