from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Tokenni to'g'ridan-to'g'ri yozish (faqat test uchun, production-da Environment Variable ishlatish tavsiya qilinadi)
API_TOKEN = "8238182597:AAFHRc6ATDGqrPCbg0SJGxNusVUV2niA-4s"

# Bot va Dispatcher yaratish
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# /start buyrug'iga javob
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Men ishlayapman 🙂")

# Oddiy matnli xabarni echo qilish
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply(f"Siz aytdingiz: {message.text}")

if __name__ == "__main__":
    # Botni ishga tushurish
    executor.start_polling(dp, skip_updates=True)
