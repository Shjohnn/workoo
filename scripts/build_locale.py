"""
Build django.po / django.mo for uz and ru without GNU gettext tools.
Run: python scripts/build_locale.py
"""
from pathlib import Path

import polib

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE = BASE_DIR / "locale"

# (msgid, Uzbek, Russian)
PAIRS = [
    # base / chrome
    ("Workooo — daily and short-term jobs in Uzbekistan.", "Workooo — O'zbekistonda kunlik va qisqa muddatli ishlar.", "Workooo — ежедневные и краткосрочные вакансии в Узбекистане."),
    ("Workooo — Find a job!", "Workooo — Ish toping!", "Workooo — Найдите работу!"),
    ("Switch to dark mode", "Qorong'u rejimga o'tish", "Переключить на тёмную тему"),
    ("Switch to light mode", "Yorug' rejimga o'tish", "Переключить на светлую тему"),
    ("Dark mode", "Qorong'u rejim", "Тёмная тема"),
    ("Light mode", "Yorug' rejim", "Светлая тема"),
    ("Main navigation", "Asosiy navigatsiya", "Основная навигация"),
    ("Menu", "Menyu", "Меню"),
    ("Jobs", "Ishlar", "Вакансии"),
    ("+ Post a job", "+ E'lon qo'shish", "+ Разместить вакансию"),
    ("My jobs", "Mening ishlarim", "Мои объявления"),
    ("My applications", "Arizalarim", "Мои отклики"),
    ("Chats", "Chatlar", "Чаты"),
    ("My profile", "Profilim", "Мой профиль"),
    ("Edit", "Tahrirlash", "Редактировать"),
    ("Log out", "Chiqish", "Выйти"),
    ("Log in", "Kirish", "Войти"),
    ("Sign up", "Ro'yxatdan o'tish", "Регистрация"),
    ("Theme", "Mavzu", "Тема"),
    ("Language", "Til", "Язык"),
    ("Close notification", "Bildirishnomani yopish", "Закрыть уведомление"),
    ("Daily job market in Uzbekistan", "O'zbekistonda kunlik ish bozori", "Рынок ежедневной работы в Узбекистане"),
    ("Pages", "Sahifalar", "Страницы"),
    ("All jobs", "Barcha ishlar", "Все вакансии"),
    ("Post a job", "Ish e'lon qilish", "Разместить вакансию"),
    ("Account", "Hisob", "Аккаунт"),
    ("© 2026 Workooo. All rights reserved.", "© 2026 Workooo. Barcha huquqlar himoyalangan.", "© 2026 Workooo. Все права защищены."),
    # Home
    ("Home", "Bosh sahifa", "Главная"),
    ("In Uzbekistan", "O'zbekistonda", "В Узбекистане"),
    ("find a job", "ish toping", "найдите работу"),
    ("or", "yoki", "или"),
    ("hire workers", "ishchi yollang", "наймите работников"),
    ("Find daily and short-term jobs in your region. Fast, easy, and reliable.", "Viloyatingizdagi kunlik va qisqa muddatli ishlarni toping. Tez, oson va ishonchli.", "Найдите ежедневную и краткосрочную работу в вашем регионе. Быстро, просто и надёжно."),
    ("Browse jobs", "Ishlarni ko'rish", "Смотреть вакансии"),
    ("12 regions", "12 viloyat", "12 регионов"),
    ("Quick application", "Tez ariza", "Быстрый отклик"),
    ("Rating system", "Baholash tizimi", "Система рейтингов"),
    ("Search jobs", "Ishlarni qidirish", "Поиск вакансий"),
    ("Job title, keywords…", "Ish nomi, kalit so'z…", "Название, ключевые слова…"),
    ("Search", "Qidirish", "Поиск"),
    ("Construction", "Qurilish", "Строительство"),
    ("Moving", "Yuk tashish", "Переезды"),
    ("Cleaning", "Tozalash", "Уборка"),
    ("Agriculture", "Qishloq xo'jaligi", "Сельское хозяйство"),
    ("Retail", "Savdo", "Торговля"),
    ("Education", "Ta'lim", "Образование"),
    ("Cafe", "Cafe", "Кафе"),
    ("IT", "IT", "IT"),
    ("Latest listings", "Yangi e'lonlar", "Новые объявления"),
    ("See all", "Barchasini ko'rish", "Смотреть все"),
    ("Address not specified", "Manzil ko'rsatilmagan", "Адрес не указан"),
    ("ago", "oldin", "назад"),
    ("No jobs yet", "Hozircha ishlar yo'q", "Пока нет вакансий"),
    ("Check back soon or post the first listing.", "Birinchi e'lon bo'lishini kuting yoki o'zingiz joylashtiring.", "Загляните позже или разместите первое объявление."),
    ("Post the first job", "Birinchi e'lonni joylashtiring", "Разместить первую вакансию"),
    ("How it works", "Qanday ishlaydi", "Как это работает"),
    ("Four simple steps", "4 ta oddiy qadam", "Четыре простых шага"),
    ("1. Sign up", "1. Ro'yxatdan o'ting", "1. Регистрация"),
    ("Register quickly as a worker or employer.", "Ishchi yoki ish beruvchi sifatida tez ro'yxatdan o'ting.", "Быстро зарегистрируйтесь как работодатель или работник."),
    ("2. Find a job", "2. Ish toping", "2. Найдите работу"),
    ("Browse jobs in your region and use filters.", "Viloyatingizdagi ishlarni ko'ring, filter qiling.", "Смотрите вакансии в регионе и фильтры."),
    ("3. Chat", "3. Chat", "3. Чат"),
    ("Apply — when accepted, chat opens.", "Ariza yuboring, qabul qilinsa chat ochiladi.", "Откликнитесь — после принятия откроется чат."),
    ("4. Rate", "4. Baholang", "4. Оценка"),
    ("After the job, leave a rating — trust grows.", "Ish tugagach baho qoldiring — ishonch quriladi.", "После работы оставьте оценку — растёт доверие."),
    # Auth
    ("Sign in", "Tizimga kirish", "Вход"),
    ("Username", "Foydalanuvchi nomi", "Имя пользователя"),
    ("Password", "Parol", "Пароль"),
    ("No account?", "Hisobingiz yo'qmi?", "Нет аккаунта?"),
    ("I am a worker", "Men ishchi", "Я исполнитель"),
    ("I am looking for work", "Ish qidiraman", "Ищу работу"),
    ("I am an employer", "Men ish beruvchi", "Я работодатель"),
    ("I want to hire", "Ishchi yollayman", "Хочу нанять"),
    ("Already have an account?", "Hisobingiz bormi?", "Уже есть аккаунт?"),
    # Job list / detail
    ("Search and filters", "Qidirish va filter", "Поиск и фильтры"),
    ("Keywords", "Kalit so'z", "Ключевые слова"),
    ("Job title or address…", "Ish nomi yoki manzil…", "Название или адрес…"),
    ("All regions", "Barcha viloyatlar", "Все регионы"),
    ("All categories", "Barcha kategoriyalar", "Все категории"),
    ("Clear", "Tozalash", "Сбросить"),
    ("Search results", "Qidiruv natijalari", "Результаты поиска"),
    ("All listings", "Barcha e'lonlar", "Все объявления"),
    ("workers", "ishchi", "работников"),
    ("No jobs found", "Ishlar topilmadi", "Вакансии не найдены"),
    ("Try changing your filters.", "Filter sozlamalarini o'zgartiring.", "Измените фильтры."),
    ("Show all jobs", "Barcha ishlarni ko'rish", "Показать все вакансии"),
    ("About the job", "Ish haqida", "О работе"),
    ("Location", "Joylashuv", "Местоположение"),
    ("Loading…", "Yuklanmoqda…", "Загрузка…"),
    ("Fullscreen", "To'liq ekran", "Полный экран"),
    ("My location", "Mening joylashuvim", "Моё местоположение"),
    ("Directions", "Yo'nalish olish", "Маршрут"),
    ("Applications", "Arizalar", "Отклики"),
    ("Accept", "Qabul qilish", "Принять"),
    ("Reject", "Rad etish", "Отклонить"),
    ("Rate", "Baholash", "Оценить"),
    ("Employer", "Ish beruvchi", "Работодатель"),
    ("Open chat", "Chatga o'tish", "Открыть чат"),
    ("More jobs", "Boshqa ishlar", "Ещё вакансии"),
    ("Apply", "Ariza topshirish", "Откликнуться"),
    ("Delete", "O'chirish", "Удалить"),
    ("Address not found", "Manzil topilmadi", "Адрес не найден"),
    ("You are here", "Siz shu yerdasiz", "Вы здесь"),
    # Job create
    ("Edit", "Tahrirlash", "Редактировать"),
    ("Post a job", "Ish e'lon qilish", "Разместить вакансию"),
    ("Edit listing", "E'lonni tahrirlash", "Редактировать объявление"),
    ("Post a new job", "Yangi ish e'lon qilish", "Новая вакансия"),
    ("Basic information", "Asosiy ma'lumotlar", "Основная информация"),
    ("Payment and schedule", "To'lov va muddat", "Оплата и сроки"),
    ("Click to enlarge", "Kattalashtirish uchun bosing", "Нажмите для увеличения"),
    ("Clear", "Tozalash", "Очистить"),
    ("Click the map to set location or use GPS.", "Xaritani bosib joylashuvni tanlang yoki GPS dan foydalaning.", "Нажмите на карту или используйте GPS."),
    ("Extras", "Qo'shimcha", "Дополнительно"),
    ("Save", "Saqlash", "Сохранить"),
    ("Publish", "E'lon qilish", "Опубликовать"),
    ("Cancel", "Bekor qilish", "Отмена"),
    ("Back", "Orqaga", "Назад"),
    ("Choose location", "Joylashuvni tanlang", "Выберите место"),
    ("Confirm", "Tasdiqlash", "Подтвердить"),
    ("Tap the map or drag the marker", "Xaritadan joy bosing yoki belgi sudrang", "Нажмите на карту или перетащите метку"),
    ("Pick a location on the map", "Xaritadan joy tanlang", "Выберите точку на карте"),
    ("Geolocation is not supported", "Geolokatsiya qo'llab-quvvatlanmaydi", "Геолокация не поддерживается"),
    ("Locating…", "Aniqlanmoqda…", "Определение…"),
    ("Could not get location. Check browser permissions.", "Joylashuv aniqlanmadi. Brauzer ruxsatini tekshiring.", "Не удалось получить местоположение. Проверьте разрешения."),
    # My jobs / applications
    ("My listings", "Mening e'lonlarim", "Мои объявления"),
    ("+ New listing", "+ Yangi e'lon", "+ Новое объявление"),
    ("applications", "ariza", "откликов"),
    ("accepted", "qabul", "принято"),
    ("View", "Ko'rish", "Просмотр"),
    ("Mark this job as completed?", "Ishni tugallanding?", "Отметить работу завершённой?"),
    ("Complete", "Tugallash", "Завершить"),
    ("Delete this listing?", "O'chirilsinmi?", "Удалить объявление?"),
    ("No listings yet", "Hali e'lon yo'q", "Пока нет объявлений"),
    ("Post your first job!", "Birinchi ish e'loningizni joylashtiring!", "Разместите первую вакансию!"),
    ("No applications yet", "Hali ariza yo'q", "Пока нет откликов"),
    # Delete confirm
    ("Delete listing", "E'lonni o'chirish", "Удалить объявление"),
    ("Delete this listing?", "E'lonni o'chirmoqchimisiz?", "Удалить это объявление?"),
    ("This action cannot be undone.", "Bu amalni qaytarib bo'lmaydi.", "Это действие нельзя отменить."),
    ("Yes, delete", "Ha, o'chirish", "Да, удалить"),
    # Profile
    ("reviews", "sharh", "отзывов"),
    ("Posted jobs", "Joylashtirilgan ishlar", "Размещённые вакансии"),
    ("Application history", "Ariza tarixim", "История откликов"),
    ("Ratings and reviews", "Baholar va sharhlar", "Оценки и отзывы"),
    ("Edit profile", "Profilni tahrirlash", "Редактировать профиль"),
    ("Current photo", "Joriy rasm", "Текущее фото"),
    # Chat
    ("Chat", "Chat", "Чат"),
    ("No messages yet. Say hello!", "Hali xabar yo'q. Birinchi bo'ling!", "Пока нет сообщений. Напишите первым!"),
    ("Message", "Xabar", "Сообщение"),
    ("Type a message…", "Xabar yozing…", "Введите сообщение…"),
    ("Send", "Yuborish", "Отправить"),
    ("No chats yet", "Hali chat yo'q", "Пока нет чатов"),
    ("Unread messages", "O'qilmagan xabarlar", "Непрочитанные сообщения"),
    ("Unread", "O'qilmagan", "Непрочитано"),
    ("Apply to a job — when accepted, a chat will open.", "Ishga ariza topshiring va qabul qilinganda chat ochiladi.", "Откликнитесь на вакансию — после принятия откроется чат."),
    # Ratings
    ("Rate worker", "Ishchini baholash", "Оценить исполнителя"),
    ("Job:", "Ish:", "Вакансия:"),
    ("Rating (1 to 5)", "Baho (1 dan 5 gacha)", "Оценка (от 1 до 5)"),
    ("Stars", "Yulduz", "Звёзды"),
    ("Comment (optional)", "Izoh (ixtiyoriy)", "Комментарий (необязательно)"),
    ("Your feedback about the work…", "Ish haqida fikringiz…", "Ваш отзыв о работе…"),
    ("Submit rating", "Baholash", "Отправить оценку"),
    ("Ratings", "Baholar", "Оценки"),
    ("Ratings for", "Baholar", "Оценки для"),
    ("Average:", "O'rtacha:", "Средняя оценка:"),
    ("No ratings yet.", "Hali baholar yo'q.", "Пока нет оценок."),
    ("Back to profile", "Profilga qaytish", "К профилю"),
    # Python messages
    ("Only employers can post jobs.", "Faqat ish beruvchilar ish e'lon qila oladi.", "Только работодатели могут публиковать вакансии."),
    ("Your job listing was published successfully!", "Ish e'loni muvaffaqiyatli joylashtirildi!", "Вакансия успешно опубликована!"),
    ("The job listing was updated!", "Ish e'loni yangilandi!", "Объявление обновлено!"),
    ("The job listing was deleted.", "Ish e'loni o'chirildi.", "Объявление удалено."),
    ("Only workers can apply.", "Faqat ishchilar ariza topshira oladi.", "Откликаться могут только исполнители."),
    ("You cannot apply to your own listing.", "O'z e'loningizga ariza topshira olmaysiz.", "Нельзя откликнуться на своё объявление."),
    ("You have already applied to this job.", "Siz allaqachon bu ishga ariza topshirgansiz.", "Вы уже откликнулись на эту вакансию."),
    ("Your application was sent! Wait for the employer to respond.", "Arizangiz yuborildi! Ish beruvchi tasdiqlashini kuting.", "Отклик отправлен! Дождитесь ответа работодателя."),
    ("Permission denied.", "Ruxsat yo'q.", "Доступ запрещён."),
    ("%(name)s was accepted. Chat is now open!", "%(name)s qabul qilindi. Chat ochildi!", "%(name)s принят. Чат открыт!"),
    ("Application was rejected.", "Ariza rad etildi.", "Отклонено."),
    ("The job was marked as completed.", "Ish tugallangan deb belgilandi.", "Работа отмечена как завершённая."),
    ("Only the employer can leave a rating.", "Faqat ish beruvchi baholashi mumkin.", "Оценку может оставить только работодатель."),
    ("You have already rated this worker for this job.", "Siz bu ishchini allaqachon baholagansiz.", "Вы уже оценили этого исполнителя."),
    ("This worker was not accepted for this job.", "Bu ishchi sizning ishingizda qabul qilinmagan.", "Исполнитель не был принят на эту работу."),
    ("%(name)s was rated!", "%(name)s baholandi!", "%(name)s оценён!"),
    ("Invalid rating.", "Noto'g'ri baho.", "Некорректная оценка."),
    ("Invalid request.", "Noto'g'ri so'rov", "Неверный запрос"),
    ("Invalid JSON.", "Noto'g'ri JSON", "Некорректный JSON"),
    ("Welcome, %(name)s! Your account was created successfully.", "Xush kelibsiz, %(name)s! Hisobingiz muvaffaqiyatli yaratildi.", "Добро пожаловать, %(name)s! Аккаунт успешно создан."),
    ("Incorrect username or password.", "Foydalanuvchi nomi yoki parol noto'g'ri.", "Неверное имя пользователя или пароль."),
    ("Profile updated successfully!", "Profil muvaffaqiyatli yangilandi!", "Профиль успешно обновлён!"),
    # Forms / models (short)
    ("— Select region —", "— Viloyatni tanlang —", "— Выберите регион —"),
    ("Email (optional)", "Email (ixtiyoriy)", "Email (необязательно)"),
    ("Phone (optional)", "Telefon raqam (ixtiyoriy)", "Телефон (необязательно)"),
    ("Password confirmation", "Parolni tasdiqlash", "Подтверждение пароля"),
    ("Job title", "Ish nomi", "Название"),
    ("Job description", "Ish tavsifi", "Описание"),
    ("Category", "Kategoriya", "Категория"),
    ("Payment amount (UZS)", "To'lov miqdori (so'mda)", "Сумма оплаты (UZS)"),
    ("Payment type", "To'lov turi", "Тип оплаты"),
    ("Region", "Viloyat", "Регион"),
    ("Address", "Manzil", "Адрес"),
    ("Image (optional)", "Rasm (ixtiyoriy)", "Изображение (необязательно)"),
    ("Workers needed", "Nechta ishchi kerak", "Сколько человек"),
    ("Work date", "Ish sanasi", "Дата работы"),
    ("Status", "Holat", "Статус"),
    ("Additional message (optional)", "Qo'shimcha xabar (ixtiyoriy)", "Дополнительное сообщение"),
    ("Briefly describe yourself...", "O'zingiz haqingizda qisqacha yozing...", "Кратко о себе..."),
    ("First name", "Ismi", "Имя"),
    ("Last name", "Familiyasi", "Фамилия"),
    ("Email", "Email", "Email"),
    ("Profile photo", "Profil rasmi", "Фото профиля"),
    ("About you", "O'zingiz haqingizda", "О себе"),
    ("Phone", "Telefon raqam", "Телефон"),
    ("Rating from 1 to 5", "1 dan 5 gacha baho", "Оценка от 1 до 5"),
    ("Construction and repair", "Qurilish va ta'mirlash", "Строительство и ремонт"),
    ("Moving and delivery", "Yuk tashish va ko'chirish", "Переезды и доставка"),
    ("Cleaning service", "Tozalash xizmati", "Уборка"),
    ("Agriculture", "Qishloq xo'jaligi", "Сельское хозяйство"),
    ("Retail and services", "Savdo va xizmat", "Торговля и услуги"),
    ("IT and computers", "IT va kompyuter", "IT и компьютеры"),
    ("Education and tutoring", "Ta'lim va repetitorlik", "Обучение и репетиторство"),
    ("Healthcare", "Sog'liqni saqlash", "Здравоохранение"),
    ("Cafe and restaurant", "Cafe va restoran", "Кафе и ресторан"),
    ("Other", "Boshqa", "Другое"),
    ("Open", "Ochiq", "Открыта"),
    ("Closed", "Yopiq", "Закрыта"),
    ("Completed", "Tugallangan", "Завершена"),
    ("Pending", "Kutilmoqda", "Ожидает"),
    ("Accepted", "Qabul qilindi", "Принят"),
    ("Rejected", "Rad etildi", "Отклонён"),
    ("In UZS", "So'mda", "В сумах"),
    ("Daily", "Kunlik", "За день"),
    ("Hourly", "Soatlik", "Почасовая"),
    ("Project", "Loyiha", "Проект"),
    ("Optional message", "Qo'shimcha xabar (ixtiyoriy)", "Дополнительное сообщение"),
    ("%(amount)s UZS / %(period)s", "%(amount)s so'm / %(period)s", "%(amount)s сум / %(period)s"),
    ("Worker", "Ishchi", "Исполнитель"),
    ("Employer", "Ish beruvchi", "Работодатель"),
    ("Light", "Yorug'", "Светлая"),
    ("Dark", "Qorong'u", "Тёмная"),
    ("Tashkent city", "Toshkent shahri", "г. Ташкент"),
    ("Tashkent region", "Toshkent viloyati", "Ташкентская область"),
    ("Andijan region", "Andijon viloyati", "Андижанская область"),
    ("Fergana region", "Farg'ona viloyati", "Ферганская область"),
    ("Namangan region", "Namangan viloyati", "Наманганская область"),
    ("Samarkand region", "Samarqand viloyati", "Самаркандская область"),
    ("Bukhara region", "Buxoro viloyati", "Бухарская область"),
    ("Kashkadarya region", "Qashqadaryo viloyati", "Кашкадарьинская область"),
    ("Surkhandarya region", "Surxondaryo viloyati", "Сурхандарьинская область"),
    ("Jizzakh region", "Jizzax viloyati", "Джизакская область"),
    ("Syrdarya region", "Sirdaryo viloyati", "Сырдарьинская область"),
    ("Navoi region", "Navoiy viloyati", "Навоийская область"),
    ("Khorezm region", "Xorazm viloyati", "Хорезмская область"),
    ("Republic of Karakalpakstan", "Qoraqalpog'iston Respublikasi", "Республика Каракалпакстан"),
]


def write_po_mo(lang: str, index: int) -> None:
    po = polib.POFile()
    po.metadata = {
        "Project-Id-Version": "Workooo 1.0",
        "Report-Msgid-Bugs-To": "",
        "POT-Creation-Date": "2026-04-12 12:00+0000",
        "PO-Revision-Date": "2026-04-12 12:00+0000",
        "Last-Translator": "",
        "Language-Team": "",
        "Language": lang,
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
    }
    if lang == "uz":
        po.metadata["Plural-Forms"] = "nplurals=1; plural=0;"
    elif lang == "ru":
        po.metadata["Plural-Forms"] = (
            "nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : "
            "n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);"
        )

    seen = set()
    for msgid, uz, ru in PAIRS:
        if msgid in seen:
            continue
        seen.add(msgid)
        msgstr = uz if index == 0 else ru
        po.append(polib.POEntry(msgid=msgid, msgstr=msgstr))

    out_dir = LOCALE / lang / "LC_MESSAGES"
    out_dir.mkdir(parents=True, exist_ok=True)
    po_path = out_dir / "django.po"
    mo_path = out_dir / "django.mo"
    po.save(str(po_path))
    po.save_as_mofile(str(mo_path))
    print("Wrote", po_path, mo_path)


def main() -> None:
    LOCALE.mkdir(exist_ok=True)
    write_po_mo("uz", 0)
    write_po_mo("ru", 1)


if __name__ == "__main__":
    main()
