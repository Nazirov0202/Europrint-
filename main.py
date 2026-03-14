import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "BU_YERGA_TOKEN_QOYING")
GROUP_CHAT_ID = -1003809622723

NUM_EMOJI = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

QUESTIONS_LOTIN = [
    "Siz qaysi uchastkada ishlaysiz?\n(Masalan: Pechat, tigel, laminatsiya, qadoqlash, gofra liniya, kashirovka, ombor)",
    "Ish davringiz mobaynida qaysi buyurtma ustida ishlayotganda muammoga duch keldingiz? Buyurtma nomini yozing.\n(Masalan: Indorama, Belissimo)",
    "Aniq qanday muammo yuzaga keldi? Nima bo'lganini batafsil tushuntiring.\n(Masalan: rang farq qildi, qog'oz tiqildi, kesish noto'g'ri chiqdi, muddatga ulgurilmadi...)",
    "Bu muammo ishlab chiqarishning qaysi bosqichida paydo bo'ldi?\n(Masalan: maket tayyorlashda, plastina chiqarishda, bosishda, kesishda, laminatsiyada, yig'ishda, jo'natishda)",
    "Bu muammo qancha tez-tez takrorlanadi?\n(Har kuni / haftada bir necha marta / oyda bir-ikki marta / kamdan-kam / birinchi marta)",
    "Muammo tufayli qanday zarar bo'ldi? Vaqt yo'qotildimi, material isrof bo'ldimi, buyurtma qayta ishlandimi yoki mijoz norozi bo'ldimi?",
    "Sizningcha, bu muammoning asosiy sababi nimada?\n(Masalan: uskuna eski, material sifatsiz, tajriba yetishmaydi, bo'limlar o'rtasida aloqa yo'q, yuklama ko'p...)",
    "Bu muammoni yechish uchun nima qilish kerak deb o'ylaysiz? Qadamma-qadam yozing.",
    "Yechimni amalga oshirish uchun nimalar kerak bo'ladi?\n(Masalan: yangi uskuna, xodimlarni o'qitish, qo'shimcha odam, jarayonni o'zgartirish, dasturiy ta'minot...)",
    "Yana qanday taklifingiz bor? Biz bilmagan, lekin siz har kuni ko'rib yurgan boshqa muammo yoki yaxshilash mumkin bo'lgan joy bormi?",
]

QUESTIONS_KIRILL = [
    "Сиз қайси участкада ишлайсиз?\n(Масалан: Печат, тигель, ламинация, қадоқлаш, гофра линия, кашировка, омбор)",
    "Иш даврингиз мобайнида қайси буюртма устида ишлаётганда муаммога дуч келдингиз? Буюртма номини ёзинг.\n(Масалан: Индорама, Белиссимо)",
    "Аниқ қандай муаммо юзага келди? Нима бўлганини батафсил тушунтиринг.\n(Масалан: ранг фарқ қилди, қоғоз тиқилди, кесиш нотўғри чиқди, муддатга улгурилмади...)",
    "Бу муаммо ишлаб чиқаришнинг қайси босқичида пайдо бўлди?\n(Масалан: макет тайёрлашда, пластина чиқаришда, босишда, кесишда, ламинацияда, йиғишда, жўнатишда)",
    "Бу муаммо қанча тез-тез такрорланади?\n(Ҳар куни / ҳафтада бир неча марта / ойда бир-икки марта / камдан-кам / биринчи марта)",
    "Муаммо туфайли қандай зарар бўлди? Вақт йўқотилдими, материал исроф бўлдими, буюртма қайта ишландими ёки мижоз норози бўлдими?",
    "Сизнингча, бу муаммонинг асосий сабаби нимада?\n(Масалан: ускуна эски, материал сифатсиз, тажриба етишмайди, бўлимлар ўртасида алоқа йўқ, юклама кўп...)",
    "Бу муаммони ечиш учун нима қилиш керак деб ўйлайсиз? Қадамма-қадам ёзинг.",
    "Ечимни амалга ошириш учун нималар керак бўлади?\n(Масалан: янги ускуна, ходимларни ўқитиш, қўшимча одам, жараённи ўзгартириш, дастурий таъминот...)",
    "Яна қандай таклифингиз бор? Биз билмаган, лекин сиз ҳар куни кўриб юрган бошқа муаммо ёки яхшилаш мумкин бўлган жой борми?",
]

QUESTIONS_RU = [
    "На каком участке вы работаете?\n(Например: печать, тигель, ламинация, упаковка, гофролиния, кашировка, склад)",
    "С каким заказом вы столкнулись с проблемой во время работы? Укажите название заказа.\n(Например: Indorama, Belissimo)",
    "Какая именно проблема возникла? Подробно опишите, что произошло.\n(Например: различие в цвете, застряла бумага, неправильная резка, не успели в срок и т.д.)",
    "На каком этапе производства возникла эта проблема?\n(Например: при подготовке макета, изготовлении пластины, печати, резке, ламинации, сборке или отгрузке)",
    "Как часто повторяется эта проблема?\n(Каждый день / несколько раз в неделю / один-два раза в месяц / редко / впервые)",
    "Какой ущерб был нанесён из-за этой проблемы? Была ли потеря времени, перерасход материалов, переделка заказа или недовольство клиента?",
    "По вашему мнению, в чём основная причина этой проблемы?\n(Например: устаревшее оборудование, низкое качество материала, недостаток опыта, отсутствие взаимодействия между отделами, высокая нагрузка и т.д.)",
    "Как, по вашему мнению, можно решить эту проблему? Опишите по шагам.",
    "Что потребуется для реализации этого решения?\n(Например: новое оборудование, обучение сотрудников, дополнительный персонал, изменение процесса, программное обеспечение и т.д.)",
    "Есть ли у вас ещё какие-либо предложения? Есть ли другие проблемы или возможности для улучшения, которые вы видите каждый день, но о которых мы можем не знать?",
]

# Eslatma xabarlari
REMINDER_LOTIN = "⚠️ Eslatma!! Barcha ma'lumotlar sir saqlanadi.\nVaqtingizni ajratganingiz uchun tashakkur."
REMINDER_KIRILL = "⚠️ Эслатма!! Барча маълумотлар сир сақланади.\nВақтингизни ажратганингиз учун ташаккур."
REMINDER_RU = "⚠️ Напоминание!! Все данные хранятся в тайне.\nСпасибо за уделённое время."

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

LANG, SCRIPT, DEPARTMENT, FULLNAME, SURVEY = range(5)


def get_questions(context):
    lang = context.user_data.get("lang")
    script = context.user_data.get("script")
    if lang == "ru":
        return QUESTIONS_RU
    elif script == "kirill":
        return QUESTIONS_KIRILL
    else:
        return QUESTIONS_LOTIN


async def delete_msg(context, chat_id, msg_id):
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except Exception:
        pass


async def clear_old_messages(context, chat_id):
    for mid in context.user_data.get("del", []):
        await delete_msg(context, chat_id, mid)
    context.user_data["del"] = []


async def post_init(application):
    description = (
        "👋 Assalomu alaykum!\n\n"
        "🏢 Europrint kompaniyasi xodimlar bilan "
        "savol-javob botiga xush kelibsiz!!\n\n"
        "Kompaniyamiz g'oyasi:\n\n"
        "Xodim va rahbarlarga bog'liq bo'lmagan, "
        "barcha jarayonlari to'liq avtomatlashtirilgan, "
        "aniq qoida va siyosatlari yozilgan, "
        "xodimlari hamda dastgohlari 101% "
        "samaradorlikka erishgan, "
        "mijozga 101% sifatga ega bo'lgan mahsulot "
        "taqdim etuvchi "
        "Markaziy Osiyodagi yetakchi tizimli kompaniya."
    )
    short_description = "🏢 Europrint kompaniyasi xodimlar savol-javob boti"

    try:
        await application.bot.set_my_description(description)
        await application.bot.set_my_short_description(short_description)
        await application.bot.set_my_commands([
            BotCommand("start", "So'rovnomani boshlash"),
            BotCommand("cancel", "Bekor qilish"),
        ])
    except Exception as e:
        logger.error(f"Bot sozlamalarida xatolik: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "del" in context.user_data:
        for mid in context.user_data.get("del", []):
            await delete_msg(context, update.message.chat_id, mid)

    context.user_data.clear()
    context.user_data["del"] = []

    try:
        await update.message.delete()
    except Exception:
        pass

    kb = [[
        InlineKeyboardButton("🇺🇿 O'zbek", callback_data="uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="ru"),
    ]]

    msg = await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык:",
        reply_markup=InlineKeyboardMarkup(kb),
    )
    context.user_data["del"].append(msg.message_id)
    return LANG


async def lang_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = q.data
    context.user_data["lang"] = lang

    await clear_old_messages(context, q.message.chat_id)

    if lang == "uz":
        kb = [[
            InlineKeyboardButton("🔤 Lotin", callback_data="lotin"),
            InlineKeyboardButton("🔡 Кирилл", callback_data="kirill"),
        ]]
        msg = await context.bot.send_message(
            chat_id=q.message.chat_id,
            text="📝 Yozuv turini tanlang:",
            reply_markup=InlineKeyboardMarkup(kb),
        )
        context.user_data["del"].append(msg.message_id)
        return SCRIPT
    else:
        context.user_data["script"] = "ru"
        kb = [[
            InlineKeyboardButton("🖨 Офсет", callback_data="dept_ofset"),
            InlineKeyboardButton("🖨 Флексо", callback_data="dept_flekso"),
        ]]
        msg = await context.bot.send_message(
            chat_id=q.message.chat_id,
            text="🏭 Выберите ваш отдел:",
            reply_markup=InlineKeyboardMarkup(kb),
        )
        context.user_data["del"].append(msg.message_id)
        return DEPARTMENT


async def script_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["script"] = q.data

    await clear_old_messages(context, q.message.chat_id)

    if q.data == "kirill":
        kb = [[
            InlineKeyboardButton("🖨 Офсет", callback_data="dept_ofset"),
            InlineKeyboardButton("🖨 Флексо", callback_data="dept_flekso"),
        ]]
        text = "🏭 Бўлимингизни танланг:"
    else:
        kb = [[
            InlineKeyboardButton("🖨 Ofset", callback_data="dept_ofset"),
            InlineKeyboardButton("🖨 Flekso", callback_data="dept_flekso"),
        ]]
        text = "🏭 Bo'limingizni tanlang:"

    msg = await context.bot.send_message(
        chat_id=q.message.chat_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(kb),
    )
    context.user_data["del"].append(msg.message_id)
    return DEPARTMENT


async def dept_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    dept = q.data.replace("dept_", "")
    if dept == "ofset":
        context.user_data["department"] = "Ofset"
    else:
        context.user_data["department"] = "Flekso"

    lang = context.user_data.get("lang")
    script = context.user_data.get("script")

    await clear_old_messages(context, q.message.chat_id)

    if lang == "ru":
        text = "👤 Напишите ваше имя и фамилию:"
    elif script == "kirill":
        text = "👤 Исм ва фамилиянгизни ёзинг:"
    else:
        text = "👤 Ism va familiyangizni yozing:"

    msg = await context.bot.send_message(chat_id=q.message.chat_id, text=text)
    context.user_data["del"].append(msg.message_id)
    return FULLNAME


async def got_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fullname"] = update.message.text
    context.user_data["answers"] = []
    context.user_data["q_num"] = 0

    await clear_old_messages(context, update.message.chat_id)
    try:
        await update.message.delete()
    except Exception:
        pass

    return await send_question(update.message.chat_id, context)


async def send_question(chat_id, context):
    questions = get_questions(context)
    i = context.user_data["q_num"]
    lang = context.user_data.get("lang")
    script = context.user_data.get("script")

    if lang == "ru":
        label = "Опрос"
    elif script == "kirill":
        label = "Сўровнома"
    else:
        label = "So'rovnoma"

    num = NUM_EMOJI[i] if i < len(NUM_EMOJI) else f"{i+1}."
    header = f"📋 {label} ({i + 1}/{len(questions)})\n\n{num} "

    msg = await context.bot.send_message(chat_id=chat_id, text=header + questions[i])
    context.user_data["del"].append(msg.message_id)
    return SURVEY


async def got_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    questions = get_questions(context)
    context.user_data["answers"].append(update.message.text)
    context.user_data["q_num"] += 1

    await clear_old_messages(context, update.message.chat_id)
    try:
        await update.message.delete()
    except Exception:
        pass

    if context.user_data["q_num"] >= len(questions):
        return await finish(update.message.chat_id, context)
    return await send_question(update.message.chat_id, context)


async def finish(chat_id, context):
    lang = context.user_data.get("lang")
    script = context.user_data.get("script")
    name = context.user_data["fullname"]
    dept = context.user_data["department"]
    answers = context.user_data["answers"]
    questions = get_questions(context)

    if lang == "ru":
        thanks = "✅ Спасибо! Опрос успешно завершён.\n\nВаши ответы приняты."
        reminder = REMINDER_RU
        til = "🇷🇺 Русский"
    elif script == "kirill":
        thanks = "✅ Раҳмат! Сўровнома муваффақиятли якунланди.\n\nЖавобларингиз қабул қилинди."
        reminder = REMINDER_KIRILL
        til = "🇺🇿 Ўзбек (Кирилл)"
    else:
        thanks = "✅ Rahmat! So'rovnoma muvaffaqiyatli yakunlandi.\n\nJavoblaringiz qabul qilindi."
        reminder = REMINDER_LOTIN
        til = "🇺🇿 O'zbek (Lotin)"

    await context.bot.send_message(chat_id=chat_id, text=thanks + "\n\n" + reminder)

    text = (
        f"📊 YANGI SO'ROVNOMA\n"
        f"{'━' * 30}\n"
        f"👤 {name}\n"
        f"🏭 {dept}\n"
        f"🌐 {til}\n"
        f"{'━' * 30}\n\n"
    )
    for idx, (question, answer) in enumerate(zip(questions, answers)):
        num = NUM_EMOJI[idx] if idx < len(NUM_EMOJI) else f"{idx+1}."
        text += f"{num} {question}\n💬 {answer}\n\n"

    try:
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
    except Exception as e:
        logger.error(f"Guruhga yuborishda xatolik: {e}")

    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "uz")
    script = context.user_data.get("script", "lotin")

    if "del" in context.user_data:
        await clear_old_messages(context, update.message.chat_id)

    if lang == "ru":
        text = "❌ Отменено. Нажмите /start."
    elif script == "kirill":
        text = "❌ Бекор қилинди. /start босинг."
    else:
        text = "❌ Bekor qilindi. /start bosing."

    await update.message.reply_text(text)
    context.user_data.clear()
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [CallbackQueryHandler(lang_chosen, pattern="^(uz|ru)$")],
            SCRIPT: [CallbackQueryHandler(script_chosen, pattern="^(lotin|kirill)$")],
            DEPARTMENT: [CallbackQueryHandler(dept_chosen, pattern="^dept_")],
            FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_name)],
            SURVEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
        allow_reentry=True,
    ))
    print("✅ Bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
