from aiogram import Bot, Dispatcher, types
import asyncio

API_TOKEN = "8238182597:AAFHRc6ATDGqrPCbg0SJGxNusVUV2niA-4s"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message()
async def handler(message: types.Message):
    if message.text == "/start":
        await message.answer("Assalomu alaykum! Botimizga xush kelibsiz 🇩🇪🇺🇿")
    else:
        await message.answer("Matn yuboring, men uni tarjima qilib beraman 😊")

async def main():
    print("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
