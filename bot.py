import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os

# ─── CONFIG ────────────────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "8725433278:AAF6Hh8MJw_kKHNNiq-IQEX-2gJ09T7kF3A")
CHANNEL_URL = "https://t.me/glossbeautyNLA"
ADMIN_IDS = [1344523187]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ─── STATES ────────────────────────────────────────────────────────────────────
class CaseForm(StatesGroup):
    name = State()
    brand = State()
    request_type = State()
    description = State()
    contact = State()

class PollForm(StatesGroup):
    waiting_answer = State()


# ─── KEYBOARDS ─────────────────────────────────────────────────────────────────
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💄 Бьюти-консультация"), KeyboardButton(text="📖 О проекте Gloss")],
            [KeyboardButton(text="📩 Подать кейс на разбор"), KeyboardButton(text="📣 Перейти в канал")],
            [KeyboardButton(text="📊 Пройти опрос")]
        ],
        resize_keyboard=True
    )

def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )


# ─── /start ────────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "✨ Привет! Я — бот <b>Gloss Beauty NLA</b>.\n\n"
        "Мы — PR-медиа о бьюти-индустрии Ташкента: пишем о трендах, брендах, мастерах и рекламных кейсах.\n\n"
        "Чем могу помочь?",
        parse_mode="HTML",
        reply_markup=main_menu()
    )


# ─── О ПРОЕКТЕ ─────────────────────────────────────────────────────────────────
@dp.message(F.text == "📖 О проекте Gloss")
async def about_project(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📣 Открыть канал", url=CHANNEL_URL)]
    ])
    await message.answer(
        "💅 <b>Gloss Beauty NLA</b> — это медиа о бьюти-индустрии Ташкента.\n\n"
        "Мы:\n"
        "• Разбираем рекламные и PR-кейсы брендов\n"
        "• Рассказываем о трендах и новинках рынка\n"
        "• Даём площадку для продвижения бьюти-бизнеса\n"
        "• Формируем культуру потребления красоты в Узбекистане\n\n"
        "📍 Аудитория — профессионалы и энтузиасты бьюти-сферы Ташкента и СНГ.",
        parse_mode="HTML",
        reply_markup=kb
    )


# ─── В КАНАЛ ───────────────────────────────────────────────────────────────────
@dp.message(F.text == "📣 Перейти в канал")
async def go_to_channel(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨ Gloss Beauty NLA", url=CHANNEL_URL)]
    ])
    await message.answer(
        "Подписывайся на наш канал — там выходят разборы кейсов, тренды и всё самое интересное о бьюти-рынке Ташкента 👇",
        reply_markup=kb
    )


# ─── БЬЮТИ-КОНСУЛЬТАЦИЯ ────────────────────────────────────────────────────────
BEAUTY_TOPICS = {
    "💋 Уход за кожей": (
        "🧴 <b>Базовый уход за кожей</b>\n\n"
        "Любой рутине нужны три шага: очищение, увлажнение, защита (SPF днём).\n\n"
        "• Для жирной кожи: лёгкие гели, ниацинамид, салициловая кислота\n"
        "• Для сухой: кремовые текстуры, гиалуроновая кислота, церамиды\n"
        "• Для чувствительной: минимализм, без отдушек, пантенол\n\n"
        "💡 Хочешь — разберём конкретную проблему подробнее!"
    ),
    "💄 Макияж и тренды": (
        "✨ <b>Актуальные бьюти-тренды</b>\n\n"
        "• «Стеклянная кожа» — увлажнение и люминайзер\n"
        "• Монохромный макияж — губы, щёки и веки в одном тоне\n"
        "• Жирный блеск на губах — gloss возвращается!\n"
        "• Пушистые брови — натуральность в тренде\n\n"
        "За разборами трендов следи в нашем канале 👉 @glossbeautyNLA"
    ),
    "💆 Салоны и мастера": (
        "📍 <b>Как выбрать салон или мастера в Ташкенте?</b>\n\n"
        "• Смотри портфолио — реальные фото работ, не стоковые\n"
        "• Читай отзывы на нескольких платформах\n"
        "• Уточняй, какие используются материалы и бренды\n"
        "• Первый визит — лучше на несложную процедуру\n\n"
        "Мы в канале регулярно делаем обзоры салонов 💅"
    ),
    "🏷️ Бренды и продукты": (
        "🛍️ <b>Как выбрать бьюти-продукт?</b>\n\n"
        "• Читай состав: первые 5 ингредиентов — основа продукта\n"
        "• Избегай: спирт в начале состава, агрессивные SLS для чувствительной кожи\n"
        "• Ищи: гиалуроновая кислота, ниацинамид, витамин C, ретинол (по задаче)\n\n"
        "Разборы конкретных брендов и продуктов — в нашем канале @glossbeautyNLA 📲"
    ),
}

@dp.message(F.text == "💄 Бьюти-консультация")
async def beauty_consult(message: types.Message):
    builder = InlineKeyboardBuilder()
    for topic in BEAUTY_TOPICS:
        builder.button(text=topic, callback_data=f"beauty_{list(BEAUTY_TOPICS.keys()).index(topic)}")
    builder.adjust(2)
    await message.answer(
        "По какой теме хочешь получить совет? 👇",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("beauty_"))
async def beauty_topic_answer(callback: types.CallbackQuery):
    idx = int(callback.data.split("_")[1])
    topic = list(BEAUTY_TOPICS.keys())[idx]
    text = BEAUTY_TOPICS[topic]
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


# ─── ПОДАЧА КЕЙСА ──────────────────────────────────────────────────────────────
@dp.message(F.text == "📩 Подать кейс на разбор")
async def case_start(message: types.Message, state: FSMContext):
    await state.set_state(CaseForm.name)
    await message.answer(
        "📋 <b>Подача кейса на разбор</b>\n\n"
        "Разберём твой рекламный, PR или брендинговый кейс в канале.\n\n"
        "Для начала — как тебя зовут? (имя или ник)",
        parse_mode="HTML",
        reply_markup=cancel_kb()
    )

@dp.message(CaseForm.name)
async def case_brand(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(name=message.text)
    await state.set_state(CaseForm.brand)
    await message.answer("Название бренда или проекта?")

@dp.message(CaseForm.brand)
async def case_type(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(brand=message.text)
    await state.set_state(CaseForm.request_type)
    builder = InlineKeyboardBuilder()
    for t in ["Рекламный кейс", "PR-кейс", "Брендинг", "Коллаборация", "Другое"]:
        builder.button(text=t, callback_data=f"casetype_{t}")
    builder.adjust(2)
    await message.answer("Тип кейса:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("casetype_"))
async def case_description(callback: types.CallbackQuery, state: FSMContext):
    case_type_val = callback.data.replace("casetype_", "")
    await state.update_data(request_type=case_type_val)
    await state.set_state(CaseForm.description)
    await callback.message.answer(
        "Коротко опиши суть кейса — что делали, какая была цель, какой результат?",
        reply_markup=cancel_kb()
    )
    await callback.answer()

@dp.message(CaseForm.description)
async def case_contact(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(description=message.text)
    await state.set_state(CaseForm.contact)
    await message.answer("Оставь контакт для связи (Telegram, Instagram или email):")

@dp.message(CaseForm.contact)
async def case_submit(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    data = await state.get_data()
    await state.clear()

    # Уведомление администратору
    admin_text = (
        f"📩 <b>Новый кейс на разбор!</b>\n\n"
        f"👤 Имя: {data.get('name')}\n"
        f"🏷️ Бренд: {data.get('brand')}\n"
        f"📂 Тип: {data.get('request_type')}\n"
        f"📝 Описание: {data.get('description')}\n"
        f"📞 Контакт: {message.text}\n\n"
        f"🔗 Пользователь: @{message.from_user.username or message.from_user.id}"
    )
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, admin_text, parse_mode="HTML")
        except Exception as e:
            logger.warning(f"Не удалось отправить уведомление админу {admin_id}: {e}")

    await message.answer(
        "✅ <b>Кейс отправлен!</b>\n\n"
        "Мы рассмотрим его и свяжемся с тобой. Следи за обновлениями в канале 💅",
        parse_mode="HTML",
        reply_markup=main_menu()
    )


# ─── ОПРОС ─────────────────────────────────────────────────────────────────────
POLL_QUESTIONS = [
    {
        "q": "Как часто ты следишь за бьюти-трендами?",
        "options": ["Каждый день", "Несколько раз в неделю", "Раз в месяц", "Почти никогда"]
    },
    {
        "q": "Какой контент тебе интереснее всего?",
        "options": ["Разборы брендов", "Тренды макияжа", "Уход за кожей", "Кейсы и реклама"]
    },
    {
        "q": "Откуда ты узнала о Gloss Beauty?",
        "options": ["Рекомендация друга", "Поиск в Telegram", "Instagram", "Другое"]
    },
]

@dp.message(F.text == "📊 Пройти опрос")
async def poll_start(message: types.Message, state: FSMContext):
    await state.set_state(PollForm.waiting_answer)
    await state.update_data(poll_step=0, poll_answers=[])
    await ask_poll_question(message, state)

async def ask_poll_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    step = data.get("poll_step", 0)

    if step >= len(POLL_QUESTIONS):
        answers = data.get("poll_answers", [])
        await state.clear()

        # Отправить результаты админу
        result_text = "📊 <b>Новый ответ на опрос</b>\n\n"
        for i, q in enumerate(POLL_QUESTIONS):
            result_text += f"❓ {q['q']}\n✅ {answers[i] if i < len(answers) else '—'}\n\n"
        result_text += f"👤 @{message.from_user.username or message.from_user.id}"
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(admin_id, result_text, parse_mode="HTML")
            except Exception as e:
                logger.warning(f"Ошибка отправки опроса админу: {e}")

        await message.answer(
            "🎉 Спасибо за участие в опросе! Твоё мнение помогает нам делать Gloss лучше 💗",
            reply_markup=main_menu()
        )
        return

    q = POLL_QUESTIONS[step]
    builder = InlineKeyboardBuilder()
    for opt in q["options"]:
        builder.button(text=opt, callback_data=f"poll_{opt[:40]}")
    builder.adjust(1)

    await message.answer(
        f"📊 <b>Вопрос {step + 1} из {len(POLL_QUESTIONS)}</b>\n\n{q['q']}",
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("poll_"), PollForm.waiting_answer)
async def poll_answer(callback: types.CallbackQuery, state: FSMContext):
    answer = callback.data.replace("poll_", "")
    data = await state.get_data()
    answers = data.get("poll_answers", [])
    answers.append(answer)
    step = data.get("poll_step", 0) + 1
    await state.update_data(poll_step=step, poll_answers=answers)
    await callback.answer("Ответ записан ✓")
    await ask_poll_question(callback.message, state)


# ─── НЕИЗВЕСТНОЕ СООБЩЕНИЕ ─────────────────────────────────────────────────────
@dp.message()
async def unknown(message: types.Message):
    await message.answer(
        "Воспользуйся меню ниже 👇",
        reply_markup=main_menu()
    )


# ─── ЗАПУСК ────────────────────────────────────────────────────────────────────
async def main():
    logger.info("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
