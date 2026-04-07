"""Seed script to populate chapters and sample shlokas into the database."""
import asyncio
from sqlalchemy import select
from app.database import async_session, engine, Base
from app.models.chapter import Chapter
from app.models.shloka import Shloka

CHAPTERS = [
    {"id": 1, "title": "Arjuna's Dilemma", "sanskrit_name": "Arjuna Vishada Yoga", "description": "Arjuna's moral crisis on the battlefield of Kurukshetra, where he sees his relatives and teachers arrayed against him.", "shloka_count": 47},
    {"id": 2, "title": "The Way of Knowledge", "sanskrit_name": "Sankhya Yoga", "description": "Krishna explains the nature of the soul, the concept of duty, and the path of knowledge to Arjuna.", "shloka_count": 72},
    {"id": 3, "title": "The Way of Action", "sanskrit_name": "Karma Yoga", "description": "Krishna teaches selfless action without attachment to results as the path to spiritual liberation.", "shloka_count": 43},
    {"id": 4, "title": "The Way of Knowledge and Renunciation", "sanskrit_name": "Jnana Karma Sanyasa Yoga", "description": "Krishna reveals the divine nature of his incarnations and the ancient tradition of spiritual knowledge.", "shloka_count": 42},
    {"id": 5, "title": "The Way of Renunciation", "sanskrit_name": "Karma Sanyasa Yoga", "description": "Krishna compares the paths of renunciation of action and selfless action, declaring both lead to liberation.", "shloka_count": 29},
    {"id": 6, "title": "The Way of Meditation", "sanskrit_name": "Dhyana Yoga", "description": "Krishna describes the practice of meditation, self-discipline, and the qualities of a true yogi.", "shloka_count": 47},
    {"id": 7, "title": "Knowledge and Wisdom", "sanskrit_name": "Jnana Vijnana Yoga", "description": "Krishna reveals both theoretical knowledge and experiential wisdom about the nature of reality.", "shloka_count": 30},
    {"id": 8, "title": "The Way to the Eternal Brahman", "sanskrit_name": "Aksara Brahma Yoga", "description": "Krishna explains the imperishable Brahman and the process of attaining the supreme goal at death.", "shloka_count": 28},
    {"id": 9, "title": "The Royal Knowledge", "sanskrit_name": "Raja Vidya Raja Guhya Yoga", "description": "Krishna shares the most confidential knowledge about his supreme nature and universal presence.", "shloka_count": 34},
    {"id": 10, "title": "Divine Manifestations", "sanskrit_name": "Vibhuti Yoga", "description": "Krishna describes his divine manifestations and how he pervades the entire universe.", "shloka_count": 42},
    {"id": 11, "title": "The Vision of the Universal Form", "sanskrit_name": "Vishwarupa Darshana Yoga", "description": "Arjuna is granted divine vision to see Krishna's cosmic form containing the entire universe.", "shloka_count": 55},
    {"id": 12, "title": "The Way of Devotion", "sanskrit_name": "Bhakti Yoga", "description": "Krishna explains devotion as the supreme path and describes the qualities of his dear devotees.", "shloka_count": 20},
    {"id": 13, "title": "The Field and the Knower", "sanskrit_name": "Kshetra Kshetragna Vibhaga Yoga", "description": "Krishna explains the body as the field and the soul as the knower, along with the nature of matter and spirit.", "shloka_count": 35},
    {"id": 14, "title": "The Three Gunas", "sanskrit_name": "Gunatraya Vibhaga Yoga", "description": "Krishna describes the three qualities of material nature: goodness, passion, and ignorance.", "shloka_count": 27},
    {"id": 15, "title": "The Supreme Person", "sanskrit_name": "Purushottama Yoga", "description": "Krishna explains the metaphor of the sacred fig tree and reveals himself as the Supreme Person.", "shloka_count": 20},
    {"id": 16, "title": "Divine and Demonic Natures", "sanskrit_name": "Daivasura Sampad Vibhaga Yoga", "description": "Krishna distinguishes between divine qualities that lead to liberation and demonic qualities that lead to bondage.", "shloka_count": 24},
    {"id": 17, "title": "Three Kinds of Faith", "sanskrit_name": "Shraddhatraya Vibhaga Yoga", "description": "Krishna classifies faith, food, worship, charity, and austerity according to the three gunas.", "shloka_count": 28},
    {"id": 18, "title": "Liberation Through Renunciation", "sanskrit_name": "Moksha Sanyasa Yoga", "description": "Krishna gives his final teaching on renunciation, duty, and surrender, culminating in the ultimate message of the Gita.", "shloka_count": 78},
]

# Sample shlokas for Chapter 1 and 2 to start with
SAMPLE_SHLOKAS = [
    # Chapter 1
    {"chapter": 1, "shloka_number": 1, "sanskrit_text": "धृतराष्ट्र उवाच |\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः |\nमामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय ||", "transliteration": "dhritarashtra uvaca\ndharma-kshetre kuru-kshetre samaveta yuyutsavah\nmamakah pandavash caiva kim akurvata sanjaya", "meaning": "Dhritarashtra said: O Sanjaya, what did my sons and the sons of Pandu do when they assembled on the holy field of Kurukshetra, eager to fight?", "themes": ["battlefield", "inquiry", "dharma", "kurukshetra"]},
    {"chapter": 1, "shloka_number": 2, "sanskrit_text": "सञ्जय उवाच |\nदृष्ट्वा तु पाण्डवानीकं व्यूढं दुर्योधनस्तदा |\nआचार्यमुपसंगम्य राजा वचनमब्रवीत् ||", "transliteration": "sanjaya uvaca\ndrishtva tu pandavanikam vyudham duryodhanas tada\nacharya upasangamya raja vacanam abravit", "meaning": "Sanjaya said: O King, seeing the army of the Pandavas arrayed in military formation, King Duryodhana approached his teacher Drona and spoke these words.", "themes": ["observation", "army", "preparation", "duryodhana"]},
    {"chapter": 1, "shloka_number": 3, "sanskrit_text": "पश्यैतां पाण्डुपुत्राणामाचार्य महतीं चमूम् |\nव्यूढां द्रुपदपुत्रेण तव शिष्येण धीमता ||", "transliteration": "pashyaitam pandu-putranam acarya mahatim camum\nvyudham drupada-putrena tava shishyena dhimata", "meaning": "Behold, O Teacher, this mighty army of the sons of Pandu, arranged in formation by your wise student, the son of Drupada.", "themes": ["army", "formation", "teacher", "drupada"]},

    # Chapter 2 - Key foundational verses
    {"chapter": 2, "shloka_number": 1, "sanskrit_text": "सञ्जय उवाच |\nतं तथा कृपयाविष्टमश्रुपूर्णाकुलेक्षणम् |\nविषीदन्तमिदं वाक्यमुवाच मधुसूदनः ||", "transliteration": "sanjaya uvaca\ntam tatha kripayavishtam ashru-purnakulekshanam\nvishidantam idam vakyam uvaca madhusudanah", "meaning": "Sanjaya said: To him who was thus overcome with compassion, whose eyes were filled with tears and who was despondent, Madhusudana (Krishna) spoke these words.", "themes": ["compassion", "sorrow", "krishna", "teaching"]},
    {"chapter": 2, "shloka_number": 7, "sanskrit_text": "कार्पण्यदोषोपहतस्वभावः\nपृच्छामि त्वां धर्मसम्मूढचेताः |\nयच्छ्रेयः स्यान्निश्चितं ब्रूहि तन्मे\nशिष्यस्तेऽहं शाधि मां त्वां प्रपन्नम् ||", "transliteration": "karpanya-doshopahata-svabhavah\npricchhami tvam dharma-sammudha-cetah\nyac chreyah syan nishcitam bruhi tan me\nshishyas te 'ham shadhi mam tvam prapannam", "meaning": "My nature is overcome by weakness and confusion about my duty. I ask you to tell me clearly what is best for me. I am your student; please instruct me, for I have surrendered to you.", "themes": ["surrender", "guidance", "duty", "confusion", "student"]},
    {"chapter": 2, "shloka_number": 14, "sanskrit_text": "मात्रास्पर्शास्तु कौन्तेय शीतोष्णसुखदुःखदाः |\nआगमापायिनोऽनित्यास्तांस्तितिक्षस्व भारत ||", "transliteration": "matra-sparshash tu kaunteya shitoshna-sukha-duhkha-dah\nagamapayino 'nityas tams titikshasva bharata", "meaning": "O son of Kunti, the contact of the senses with their objects gives rise to feelings of cold and heat, pleasure and pain. They are temporary, coming and going. Learn to endure them, O Bharata.", "themes": ["endurance", "impermanence", "senses", "equanimity"]},
    {"chapter": 2, "shloka_number": 20, "sanskrit_text": "न जायते म्रियते वा कदाचि-\nन्नायं भूत्वा भविता वा न भूयः |\nअजो नित्यः शाश्वतोऽयं पुराणो\nन हन्यते हन्यमाने शरीरे ||", "transliteration": "na jayate mriyate va kadacin\nnayam bhutva bhavita va na bhuyah\najo nityah shashvato 'yam purano\nna hanyate hanyamane sharire", "meaning": "The soul is never born, nor does it ever die. It has never come into being, nor will it cease to exist. It is unborn, eternal, ever-existing, and primeval. It is not slain when the body is slain.", "themes": ["soul", "eternal", "immortality", "death", "birth"]},
    {"chapter": 2, "shloka_number": 47, "sanskrit_text": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन |\nमा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ||", "transliteration": "karmanye vadhikaraste ma phaleshu kadachana\nma karma-phala-hetur bhur ma te sango 'stv akarmani", "meaning": "You have a right to perform your duty, but you are not entitled to the fruits of your actions. Never consider yourself the cause of the results, and never be attached to inaction.", "themes": ["duty", "detachment", "action", "karma", "selflessness", "purpose"]},
    {"chapter": 2, "shloka_number": 48, "sanskrit_text": "योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय |\nसिद्ध्यसिद्ध्योः समो भूत्वा समत्वं योग उच्यते ||", "transliteration": "yoga-sthah kuru karmani sangam tyaktva dhananjaya\nsiddhy-asiddhyoh samo bhutva samatvam yoga ucyate", "meaning": "Perform your duties established in yoga, abandoning attachment, and be even-minded in success and failure. Such equanimity of mind is called yoga.", "themes": ["yoga", "equanimity", "detachment", "action", "balance"]},
    {"chapter": 2, "shloka_number": 62, "sanskrit_text": "ध्यायतो विषयान्पुंसः सङ्गस्तेषूपजायते |\nसङ्गात्सञ्जायते कामः कामात्क्रोधोऽभिजायते ||", "transliteration": "dhyayato vishayan pumsah sangas teshupajayate\nsangat sanjayate kamah kamat krodho 'bhijayate", "meaning": "When a person dwells on sense objects, attachment arises. From attachment grows desire, and from desire arises anger.", "themes": ["attachment", "desire", "anger", "mind", "senses"]},
    {"chapter": 2, "shloka_number": 63, "sanskrit_text": "क्रोधाद्भवति सम्मोहः सम्मोहात्स्मृतिविभ्रमः |\nस्मृतिभ्रंशाद् बुद्धिनाशो बुद्धिनाशात्प्रणश्यति ||", "transliteration": "krodhad bhavati sammohah sammohat smriti-vibhramah\nsmriti-bhramshad buddhi-nasho buddhi-nashat pranashyati", "meaning": "From anger comes delusion; from delusion, loss of memory; from loss of memory, destruction of intelligence; and from destruction of intelligence, one perishes.", "themes": ["anger", "delusion", "wisdom", "destruction", "mind"]},
]


async def seed_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Check if already seeded
        result = await session.execute(select(Chapter).limit(1))
        if result.scalar_one_or_none():
            print("Database already seeded. Skipping.")
            return

        # Seed chapters
        for ch in CHAPTERS:
            session.add(Chapter(**ch))
        await session.flush()

        # Seed sample shlokas
        for idx, sh in enumerate(SAMPLE_SHLOKAS):
            session.add(Shloka(**sh, embedding_index=idx))

        await session.commit()
        print(f"Seeded {len(CHAPTERS)} chapters and {len(SAMPLE_SHLOKAS)} sample shlokas.")


if __name__ == "__main__":
    asyncio.run(seed_database())
