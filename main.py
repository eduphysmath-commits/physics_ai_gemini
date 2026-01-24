import streamlit as st
from groq import Groq
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# --- БАПТАУЛАР ---

# 1. Groq API тексеру
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("⚠️ Groq API кілті табылмады! Secrets бөлімін тексеріңіз.")
    st.stop()

# 2. Google Sheets функциясы
def save_to_google_sheets(name, student_class, result_text, total_score):
    try:
        # Secrets-тен кілтті алу
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # [service_account] бөлімінен деректерді оқимыз
        creds_dict = dict(st.secrets["service_account"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # Кестені ашу (Кесте аты дәл осылай болуы керек!)
        sheet = client.open("physics_grades").sheet1
        
        # Уақыт
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        
        # Кестеге жазу: [Уақыт, Аты, Сынып, Ұпай, Толық жауап]
        sheet.append_row([now, name, student_class, total_score, result_text])
        return True
    except Exception as e:
        st.error(f"Кестеге сақтау кезінде қате шықты: {e}")
        return False

# Модель атауы
MODEL_NAME = "llama-3.3-70b-versatile"

# --- БЖБ СҰРАҚТАРЫ ---
BJB_TITLE = "БЖБ: Динамика негіздері (9-сынып)"
QUESTIONS = [
    {
        "id": 1,
        "text": """1-тапсырма [6 ұпай].
Сатурн ғаламшарының массасы 5,7 ∙ 10²⁶ кг, ал оның радиусы 60 270 км.
a) Сатурн бетіндегі еркін түсу үдеуін (g) анықтаңыз.
b) Сатурн үшін бірінші ғарыштық жылдамдықты (v₁) есептеңіз.
(G = 6,67 ∙ 10⁻¹¹ Н∙м²/кг²)""",
        "correct_answer": "g ≈ 10.47 м/с², v1 ≈ 25.1 км/с"
    },
    {
        "id": 2,
        "text": """2-тапсырма [3 ұпай].
Жер мен Айдың арасындағы орташа қашықтық r = 384 400 км. Жердің массасы m₁ = 5,97 ∙ 10²⁴ кг, ал Айдың массасы m₂ = 7,35 ∙ 10²² кг.
Жер мен Ай арасындағы бүкіләлемдік тартылыс күшін табыңыз.""",
        "correct_answer": "F ≈ 1.98 ∙ 10^20 Н"
    },
    {
        "id": 3,
        "text": """3-тапсырма [6 ұпай].
Жердің жасанды серігі Жер бетінен h = 2R биіктікте қозғалуда.
(R(жер) = 6400 км; M(жер) = 6 ∙ 10²⁴ кг).
a) Серіктің айналу периодын анықтаңыз.
b) Осы биіктіктегі еркін түсу үдеуін есептеңіз.""",
        "correct_answer": "T ≈ 7.3 сағат, g ≈ 1.09 м/с²"
    }
]

# --- САЙТ ИНТЕРФЕЙСІ ---
st.set_page_config(page_title="Физика БЖБ", page_icon="📝", layout="wide")

st.title(f"📝 {BJB_TITLE}")
st.info("Жауаптарыңыз автоматты түрде мұғалімге жіберіледі.")
st.markdown("---")

with st.sidebar:
    st.header("Оқушы мәліметі")
    student_name = st.text_input("Аты-жөніңіз (Толық):", placeholder="Мысалы: Арман Оспанов")
    student_class = st.selectbox("Сыныбыңыз:", ["9 A", "9 Ә", "9 Б", "9 В", "10 A"])
    st.warning("Барлық есепті шығарып болған соң ғана Тексеру түймесін басыңыз.")

with st.form("bjb_form"):
    student_answers = {}
    for question in QUESTIONS:
        st.subheader(f"🔹 {question['text']}")
        student_answers[question['id']] = st.text_area(
            f"Жауап {question['id']}:", 
            height=150, 
            key=f"q_{question['id']}",
            placeholder="Шешу жолын жазыңыз..."
        )
        st.markdown("---")
    
    submit_button = st.form_submit_button("Жұмысты тапсыру және Тексеру ✅", type="primary")

# --- ТЕКСЕРУ ЛОГИКАСЫ ---
if submit_button:
    if not student_name:
        st.error("⚠️ Аты-жөніңізді жазуды ұмыттыңыз!")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # AI-ға тапсырма
            prompt_text = f"""
            Сен Физика мұғалімісің. Оқушының жұмысын тексер.
            Оқушы: {student_name}, {student_class}
            
            ТАПСЫРМАЛАР:
            """
            for q in QUESTIONS:
                ans = student_answers[q['id']] if student_answers[q['id']] else "Жауап жоқ"
                prompt_text += f"Сұрақ {q['id']}: {q['text']}\nОқушы жауабы: {ans}\nДұрыс жауап: {q['correct_answer']}\n---\n"
            
            prompt_text += """
            ТАЛАПТАР:
            1. Әр есепті бағала (Дұрыс/Қате/Жартылай).
            2. Ең соңында "ЖАЛПЫ ҰПАЙ: X / 15" деп жаз.
            3. Жауапты Markdown форматында, қазақша қайтар.
            """

            with st.spinner("Жұмыс тексерілуде және журналға қойылуда..."):
                # AI тексеруі
                completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_text}],
                    model=MODEL_NAME
                )
                result_text = completion.choices[0].message.content
                
                # Ұпайды мәтіннен іздеп табу (қарапайым жолмен)
                total_score = "Белгісіз"
                if "ЖАЛПЫ ҰПАЙ:" in result_text:
                    # Мәтіннен ұпайды қиып алуға тырысу
                    parts = result_text.split("ЖАЛПЫ ҰПАЙ:")
                    if len(parts) > 1:
                        total_score = parts[1].split("\n")[0].strip()

                # Google Sheets-ке сақтау
                save_success = save_to_google_sheets(student_name, student_class, result_text, total_score)
                
                if save_success:
                    st.balloons()
                    st.success(f"✅ Жарайсыз, {student_name}! Жұмысыңыз қабылданды.")
                    st.markdown("### Нәтиже:")
                    st.markdown(result_text)
                else:
                    st.warning("Нәтиже шықты, бірақ журналға жазылмады. Мұғалімге скриншот жіберіңіз.")
                    st.markdown(result_text)

        except Exception as e:
            st.error(f"Жүйелік қате: {e}")
