from datetime import date, datetime, timedelta
from app.database import SessionLocal, init_db
from app import models
from app.services.progression_service import update_skill_progress


LANGUAGES = [
    ("aa", "Afar", "Afaraf", None), ("ab", "Abkhazian", "Аҧсуа", None), ("ae", "Avestan", "Avesta", None),
    ("af", "Afrikaans", "Afrikaans", "ZA"), ("ak", "Akan", "Akan", "GH"), ("am", "Amharic", "አማርኛ", "ET"),
    ("an", "Aragonese", "Aragonés", "ES"), ("ar", "Arabic", "العربية", "SA"), ("as", "Assamese", "অসমীয়া", "IN"),
    ("av", "Avaric", "Авар", None), ("ay", "Aymara", "Aymar aru", "BO"), ("az", "Azerbaijani", "Azərbaycanca", "AZ"),
    ("ba", "Bashkir", "Башҡорт", "RU"), ("be", "Belarusian", "Беларуская", "BY"), ("bg", "Bulgarian", "Български", "BG"),
    ("bh", "Bihari", "भोजपुरी", "IN"), ("bi", "Bislama", "Bislama", "VU"), ("bm", "Bambara", "Bamanankan", "ML"),
    ("bn", "Bengali", "বাংলা", "BD"), ("bo", "Tibetan", "བོད་ཡིག", "CN"), ("br", "Breton", "Brezhoneg", "FR"),
    ("bs", "Bosnian", "Bosanski", "BA"), ("ca", "Catalan", "Català", "ES"), ("ce", "Chechen", "Нохчийн", "RU"),
    ("ch", "Chamorro", "Chamoru", "GU"), ("co", "Corsican", "Corsu", "FR"), ("cr", "Cree", "ᓀᐦᐃᔭᐍᐏᐣ", "CA"),
    ("cs", "Czech", "Čeština", "CZ"), ("cu", "Church Slavic", "Словѣньскъ", None), ("cv", "Chuvash", "Чӑвашла", "RU"),
    ("cy", "Welsh", "Cymraeg", "GB"), ("da", "Danish", "Dansk", "DK"), ("de", "German", "Deutsch", "DE"),
    ("dv", "Divehi", "ދިވެހި", "MV"), ("dz", "Dzongkha", "རྫོང་ཁ", "BT"), ("ee", "Ewe", "Eʋegbe", "GH"),
    ("el", "Greek", "Ελληνικά", "GR"), ("en", "English", "English", "US"), ("eo", "Esperanto", "Esperanto", None),
    ("es", "Spanish", "Español", "ES"), ("et", "Estonian", "Eesti", "EE"), ("eu", "Basque", "Euskara", "ES"),
    ("fa", "Persian", "فارسی", "IR"), ("ff", "Fulah", "Fulfulde", None), ("fi", "Finnish", "Suomi", "FI"),
    ("fj", "Fijian", "Vosa Vakaviti", "FJ"), ("fo", "Faroese", "Føroyskt", "FO"), ("fr", "French", "Français", "FR"),
    ("fy", "Western Frisian", "Frysk", "NL"), ("ga", "Irish", "Gaeilge", "IE"), ("gd", "Scottish Gaelic", "Gàidhlig", "GB"),
    ("gl", "Galician", "Galego", "ES"), ("gn", "Guarani", "Avañe'ẽ", "PY"), ("gu", "Gujarati", "ગુજરાતી", "IN"),
    ("gv", "Manx", "Gaelg", "IM"), ("ha", "Hausa", "Hausa", "NG"), ("he", "Hebrew", "עברית", "IL"),
    ("hi", "Hindi", "हिन्दी", "IN"), ("ho", "Hiri Motu", "Hiri Motu", "PG"), ("hr", "Croatian", "Hrvatski", "HR"),
    ("ht", "Haitian Creole", "Kreyòl ayisyen", "HT"), ("hu", "Hungarian", "Magyar", "HU"), ("hy", "Armenian", "Հայերեն", "AM"),
    ("hz", "Herero", "Otjiherero", "NA"), ("ia", "Interlingua", "Interlingua", None), ("id", "Indonesian", "Bahasa Indonesia", "ID"),
    ("ie", "Interlingue", "Interlingue", None), ("ig", "Igbo", "Igbo", "NG"), ("ii", "Sichuan Yi", "ꆈꌠ꒿", "CN"),
    ("ik", "Inupiaq", "Iñupiaq", "US"), ("io", "Ido", "Ido", None), ("is", "Icelandic", "Íslenska", "IS"),
    ("it", "Italian", "Italiano", "IT"), ("iu", "Inuktitut", "ᐃᓄᒃᑎᑐᑦ", "CA"), ("ja", "Japanese", "日本語", "JP"),
    ("jv", "Javanese", "Basa Jawa", "ID"), ("ka", "Georgian", "ქართული", "GE"), ("kg", "Kongo", "Kikongo", "CD"),
    ("ki", "Kikuyu", "Gĩkũyũ", "KE"), ("kj", "Kuanyama", "Kuanyama", "NA"), ("kk", "Kazakh", "Қазақша", "KZ"),
    ("kl", "Kalaallisut", "Kalaallisut", "GL"), ("km", "Khmer", "ខ្មែរ", "KH"), ("kn", "Kannada", "ಕನ್ನಡ", "IN"),
    ("ko", "Korean", "한국어", "KR"), ("kr", "Kanuri", "Kanuri", "NG"), ("ks", "Kashmiri", "कॉशुर", "IN"),
    ("ku", "Kurdish", "Kurdî", "TR"), ("kv", "Komi", "Коми", "RU"), ("kw", "Cornish", "Kernewek", "GB"),
    ("ky", "Kyrgyz", "Кыргызча", "KG"), ("la", "Latin", "Latina", "VA"), ("lb", "Luxembourgish", "Lëtzebuergesch", "LU"),
    ("lg", "Ganda", "Luganda", "UG"), ("li", "Limburgish", "Limburgs", "NL"), ("ln", "Lingala", "Lingála", "CD"),
    ("lo", "Lao", "ລາວ", "LA"), ("lt", "Lithuanian", "Lietuvių", "LT"), ("lu", "Luba-Katanga", "Tshiluba", "CD"),
    ("lv", "Latvian", "Latviešu", "LV"), ("mg", "Malagasy", "Malagasy", "MG"), ("mh", "Marshallese", "Kajin M̧ajeļ", "MH"),
    ("mi", "Maori", "Māori", "NZ"), ("mk", "Macedonian", "Македонски", "MK"), ("ml", "Malayalam", "മലയാളം", "IN"),
    ("mn", "Mongolian", "Монгол", "MN"), ("mr", "Marathi", "मराठी", "IN"), ("ms", "Malay", "Bahasa Melayu", "MY"),
    ("mt", "Maltese", "Malti", "MT"), ("my", "Burmese", "မြန်မာဘာသာ", "MM"), ("na", "Nauru", "Dorerin Naoero", "NR"),
    ("nb", "Norwegian Bokmal", "Norsk bokmål", "NO"), ("nd", "North Ndebele", "IsiNdebele", "ZW"), ("ne", "Nepali", "नेपाली", "NP"),
    ("ng", "Ndonga", "Owambo", "NA"), ("nl", "Dutch", "Nederlands", "NL"), ("nn", "Norwegian Nynorsk", "Norsk nynorsk", "NO"),
    ("no", "Norwegian", "Norsk", "NO"), ("nr", "South Ndebele", "IsiNdebele", "ZA"), ("nv", "Navajo", "Diné bizaad", "US"),
    ("ny", "Chichewa", "Chichewa", "MW"), ("oc", "Occitan", "Occitan", "FR"), ("oj", "Ojibwa", "Anishinaabemowin", "CA"),
    ("om", "Oromo", "Afaan Oromoo", "ET"), ("or", "Odia", "ଓଡ଼ିଆ", "IN"), ("os", "Ossetian", "Ирон", "RU"),
    ("pa", "Punjabi", "ਪੰਜਾਬੀ", "IN"), ("pi", "Pali", "पालि", None), ("pl", "Polish", "Polski", "PL"),
    ("ps", "Pashto", "پښتو", "AF"), ("pt", "Portuguese", "Português", "PT"), ("qu", "Quechua", "Runa Simi", "PE"),
    ("rm", "Romansh", "Rumantsch", "CH"), ("rn", "Rundi", "Ikirundi", "BI"), ("ro", "Romanian", "Română", "RO"),
    ("ru", "Russian", "Русский", "RU"), ("rw", "Kinyarwanda", "Ikinyarwanda", "RW"), ("sa", "Sanskrit", "संस्कृतम्", "IN"),
    ("sc", "Sardinian", "Sardu", "IT"), ("sd", "Sindhi", "سنڌي", "PK"), ("se", "Northern Sami", "Davvisámegiella", "NO"),
    ("sg", "Sango", "Sängö", "CF"), ("si", "Sinhala", "සිංහල", "LK"), ("sk", "Slovak", "Slovenčina", "SK"),
    ("sl", "Slovenian", "Slovenščina", "SI"), ("sm", "Samoan", "Gagana Samoa", "WS"), ("sn", "Shona", "ChiShona", "ZW"),
    ("so", "Somali", "Soomaali", "SO"), ("sq", "Albanian", "Shqip", "AL"), ("sr", "Serbian", "Српски", "RS"),
    ("ss", "Swati", "SiSwati", "SZ"), ("st", "Southern Sotho", "Sesotho", "LS"), ("su", "Sundanese", "Basa Sunda", "ID"),
    ("sv", "Swedish", "Svenska", "SE"), ("sw", "Swahili", "Kiswahili", "KE"), ("ta", "Tamil", "தமிழ்", "IN"),
    ("te", "Telugu", "తెలుగు", "IN"), ("tg", "Tajik", "Тоҷикӣ", "TJ"), ("th", "Thai", "ไทย", "TH"),
    ("ti", "Tigrinya", "ትግርኛ", "ER"), ("tk", "Turkmen", "Türkmençe", "TM"), ("tl", "Filipino", "Filipino", "PH"),
    ("tn", "Tswana", "Setswana", "BW"), ("to", "Tonga", "Lea faka-Tonga", "TO"), ("tr", "Turkish", "Türkçe", "TR"),
    ("ts", "Tsonga", "XiTsonga", "ZA"), ("tt", "Tatar", "Татарча", "RU"), ("tw", "Twi", "Twi", "GH"),
    ("ty", "Tahitian", "Reo Tahiti", "PF"), ("ug", "Uyghur", "ئۇيغۇرچە", "CN"), ("uk", "Ukrainian", "Українська", "UA"),
    ("ur", "Urdu", "اردو", "PK"), ("uz", "Uzbek", "Oʻzbekcha", "UZ"), ("ve", "Venda", "Tshivenḓa", "ZA"),
    ("vi", "Vietnamese", "Tiếng Việt", "VN"), ("vo", "Volapuk", "Volapük", None), ("wa", "Walloon", "Walon", "BE"),
    ("wo", "Wolof", "Wolof", "SN"), ("xh", "Xhosa", "IsiXhosa", "ZA"), ("yi", "Yiddish", "ייִדיש", None),
    ("yo", "Yoruba", "Yorùbá", "NG"), ("za", "Zhuang", "Saɯ cueŋƅ", "CN"), ("zh", "Chinese", "中文", "CN"),
    ("zu", "Zulu", "IsiZulu", "ZA"),
]

WORDS = [
    ("नमस्ते", "hello"), ("घर", "house"), ("गाड़ी", "car"), ("खाना", "food"),
    ("पानी", "water"), ("किताब", "book"), ("परिवार", "family"), ("बाज़ार", "market"),
]


def seed_languages(db):
    for code, name, native_name, flag in LANGUAGES:
        language = db.query(models.Language).filter_by(code=code).first()
        if not language:
            language = models.Language(code=code, name=name, native_name=native_name, flag=flag)
            db.add(language)
        language.available = code == "en"
    db.flush()


def add_exercises(db, lesson, start_id):
    templates = [
        ("multiple_choice", "What is '{hi}' in English?", "Choose the correct meaning", "{en}", ["house", "car", "food", "book"]),
        ("translate", "Translate this sentence: My {en} is big.", "Build the English sentence", "My {en} is big.", ["My", "{en}", "is", "big"]),
        ("word_bank", "मेरी {hi} बड़ी है।", "Tap the words in order", "my {en} is big", ["my", "{en}", "is", "big"]),
        ("fill_blank", "My ___ is small.", "Pick the missing word", "{en}", ["house", "car", "book", "water"]),
        ("type_answer", "Translate: मेरा {hi} छोटा है।", "Type the English answer", "My {en} is small.", []),
        ("match_pairs", "Match the word pairs", "Select matching pairs", "all pairs matched", []),
        ("multiple_choice", "Which word means '{en}'?", "Choose the Hindi word", "{hi}", ["नमस्ते", "घर", "गाड़ी", "खाना"]),
        ("type_answer", "Write this in English: I want {en}.", "Type the answer", "I want {en}.", []),
    ]
    for index, tpl in enumerate(templates, start_id):
        hi, en = WORDS[(lesson.id + index) % len(WORDS)]
        exercise = models.Exercise(
            lesson_id=lesson.id,
            type=tpl[0],
            prompt=tpl[1].format(hi=hi, en=en),
            instruction=tpl[2],
            correct_answer=tpl[3].format(hi=hi, en=en),
            explanation=f"{hi} means {en}.",
            order_index=index,
        )
        db.add(exercise)
        db.flush()
        if tpl[0] == "match_pairs":
            for left, right in [("hello", "नमस्ते"), ("car", "गाड़ी"), ("house", "घर"), ("food", "खाना")]:
                db.add(models.MatchPair(exercise_id=exercise.id, left_text=left, right_text=right))
        else:
            choices = [choice.format(hi=hi, en=en) for choice in tpl[4]]
            if exercise.correct_answer not in choices and choices:
                choices[0] = exercise.correct_answer
            for option_index, text in enumerate(dict.fromkeys(choices), 1):
                db.add(models.ExerciseOption(exercise_id=exercise.id, text=text, is_correct=text == exercise.correct_answer, order_index=option_index))


def seed_courses(db):
    hindi = db.query(models.Language).filter_by(code="hi").one()
    english = db.query(models.Language).filter_by(code="en").one()
    course = db.query(models.Course).first()
    if not course:
        course = models.Course(
            name="English for Hindi Speakers",
            source_language="Hindi",
            target_language="English",
            description="Practice everyday English through short guided lessons.",
            icon="US",
        )
        db.add(course)
        db.flush()
    course.source_language_id = hindi.id
    course.target_language_id = english.id
    return course


def seed_units_skills_lessons(db, course):
    if db.query(models.Unit).filter_by(course_id=course.id).first():
        return
    unit_titles = [
        ("Basics", "Simple words, greetings, food and family."),
        ("Daily Life", "Talk about your home, routines and needs."),
        ("People and Places", "Describe people, locations and movement."),
        ("Travel and Conversation", "Useful phrases for trips and chats."),
    ]
    skill_names = [
        ["Greetings", "Common Words", "Simple Sentences", "Family"],
        ["At Home", "Food", "Daily Routine", "Questions"],
        ["People", "Places", "Directions", "Descriptions"],
        ["Travel", "Shopping", "Conversation", "Review"],
    ]
    previous_skill_id = None
    for unit_index, (title, desc) in enumerate(unit_titles, 1):
        unit = models.Unit(course_id=course.id, number=unit_index, title=title, description=desc, order_index=unit_index)
        db.add(unit)
        db.flush()
        for skill_index, skill_title in enumerate(skill_names[unit_index - 1], 1):
            skill = models.Skill(
                unit_id=unit.id,
                title=skill_title,
                description=f"Build confidence with {skill_title.lower()}.",
                icon=["Star", "MessageCircle", "BookOpen", "Trophy"][skill_index - 1],
                color=["#58cc02", "#1cb0f6", "#ffb020", "#ce82ff"][skill_index - 1],
                order_index=skill_index,
                required_skill_id=previous_skill_id,
            )
            db.add(skill)
            db.flush()
            for lesson_index in range(1, 4):
                lesson = models.Lesson(skill_id=skill.id, title=f"{skill_title} {lesson_index}", order_index=lesson_index, xp_reward=20, estimated_minutes=4)
                db.add(lesson)
                db.flush()
                add_exercises(db, lesson, 1)
            previous_skill_id = skill.id


def seed_user(db, course):
    user = db.query(models.User).filter_by(username="Uday").first()
    if not user:
        user = models.User(id=1, username="Uday", display_name="Uday Dixit", email="uday@example.com", avatar="UD", age=21)
        db.add(user)
        db.add(models.UserStats(user_id=1, total_xp=505, daily_xp=7, streak=1, longest_streak=3, hearts=3, gems=100, daily_goal=10, today_goal_progress=7, last_activity_date=date.today()))
        db.add(models.UserCourseProgress(user_id=1, course_id=course.id, current_unit_id=1, current_skill_id=1, completed_lessons=2))
        db.flush()


def seed_progress(db):
    if not db.query(models.UserLessonProgress).filter_by(user_id=1).first():
        for lesson_id, score in [(1, 100), (2, 87)]:
            db.add(models.UserLessonProgress(user_id=1, lesson_id=lesson_id, completed=True, score=score, attempts=1, best_score=score, completed_at=datetime.utcnow() - timedelta(days=1)))
        db.flush()
    for skill_id in [skill.id for skill in db.query(models.Skill).all()]:
        update_skill_progress(db, 1, skill_id)


def seed_quests(db):
    if db.query(models.Quest).first():
        return
    quests = [
        ("Complete 3 lessons", "Finish three lessons today.", "lessons", 3, 10, 10),
        ("Earn 50 XP", "Collect XP from lessons.", "xp", 50, 10, 20),
        ("Perfect lesson", "Complete one lesson with no mistakes.", "perfect", 1, 15, 10),
    ]
    for title, desc, kind, target, xp, gems in quests:
        quest = models.Quest(title=title, description=desc, type=kind, target=target, reward_xp=xp, reward_gems=gems)
        db.add(quest)
        db.flush()
        db.add(models.UserQuestProgress(user_id=1, quest_id=quest.id, progress=1 if kind == "lessons" else 7 if kind == "xp" else 0))


def seed_achievements(db):
    if db.query(models.Achievement).first():
        return
    for title, desc, icon, kind, value in [
        ("First Lesson", "Complete your first lesson.", "Medal", "lessons", 1),
        ("XP Hunter", "Earn 500 XP.", "Zap", "xp", 500),
        ("Perfect Lesson", "Finish with 100%.", "Sparkles", "perfect", 1),
        ("7 Day Streak", "Study seven days in a row.", "Flame", "streak", 7),
        ("Path Explorer", "Complete ten lessons.", "Map", "lessons", 10),
    ]:
        db.add(models.Achievement(title=title, description=desc, icon=icon, requirement_type=kind, requirement_value=value))


def seed_leaderboard(db):
    if db.query(models.LeaderboardEntry).first():
        return
    for name, xp, user_id in [("Alex", 420, 2), ("Uday Dixit", 380, 1), ("Rahul", 340, 3), ("Priya", 280, 4), ("Meera", 190, 5)]:
        db.add(models.LeaderboardEntry(user_id=user_id, display_name=name, weekly_xp=xp, rank=1))


def seed_all():
    init_db()
    db = SessionLocal()
    seed_languages(db)
    course = seed_courses(db)
    seed_units_skills_lessons(db, course)
    seed_user(db, course)
    seed_progress(db)
    seed_quests(db)
    seed_achievements(db)
    seed_leaderboard(db)
    db.commit()
    from app.services.gamification_service import rerank_leaderboard, unlock_achievements
    rerank_leaderboard(db)
    unlock_achievements(db, 1, 0)
    db.commit()
    db.close()


def seed():
    seed_all()


if __name__ == "__main__":
    seed_all()
