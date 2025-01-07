#muafaqiyatli botning maqsadi txt dagi mavjud hashtag ostida qancha post borligini aniqlash va web ilova ishlab chiqarish
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

API_TOKEN = '7537545801:AAHdSVwZi_RL1xOdYpSYrgMDBr6OwzjtaEk'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# So‘zlarni fayldan o‘qish
def load_words_from_file(file_path):
    with open(file_path, 'r') as file:
        return set(word.strip() for word in file.readlines())

# Fayldan so‘zlarni o‘qish
WORDS_SET = load_words_from_file('list.txt')

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer('Iltimos, so‘z yuboring. Agar bu so‘z bizning ro‘yxatimizda bo‘lsa, Web ilovani ochamiz.')

@dp.message()
async def handle_text(message: types.Message):
    user_input = message.text.strip()
    if user_input in WORDS_SET:
        # Web ilova URL yaratish
        WEB_APP_URL = f"https://www.instagram.com/explore/tags/{user_input}/"
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Web ilova", web_app=WebAppInfo(url=WEB_APP_URL))]
        ])
        await message.answer(f"Topildi! Web ilovani oching:", reply_markup=markup)
    else:
        await message.answer("So‘z ro‘yxatda mavjud emas.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
