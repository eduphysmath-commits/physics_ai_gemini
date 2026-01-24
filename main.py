import streamlit as st
from groq import Groq

# --- БАПТАУЛАР ---
# API кілтті Streamlit "Secrets" бөлімінен аламыз
# Егер кілт табылмаса, бос қалдырамыз (сайт құлап қалмауы үшін)
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = None

# Модель атауы
MODEL_NAME = "llama-3.3-70b-versatile"

# --- БЖБ СҰРАҚТАРЫ ("ДИНАМИКА НЕГІЗДЕРІ") ---
BJB_TITLE = "БЖБ: Динамика негіздері (9-сынып)"
QUESTIONS = [
    {
        "id": 1,
        "text": """1-тапсырма [6 ұпай].
Сатурн ғаламшарының массасы 5,7 ∙ 10²⁶ кг, ал оның радиусы 60 270 км.
a) Сатурн бетіндегі еркін түсу үдеуін (g) анықтаңыз.
b) Сатурн үшін бірінші ғарыштық жылдамдықты (v₁) есептеңіз.
(G = 6,67 ∙ 10⁻¹¹ Н∙м²/кг²)""",
        "correct_answer": """
        Шешу үлгісі:
        ХБЖ (SI): R = 60270 км = 6,027 ∙ 10^7 м.
        a) g = (G * M) / R^2. 
           g ≈ (6.67e-11 * 5.7e26) / (6.027e7)^2 ≈ 10.47 м/с².
        b) v1 = √(G * M / R) немесе v1 = √(g * R).
           v1 ≈ √(10.47 * 6.027e7) ≈ 25120 м/с ≈ 25.1 км/с.
        """
    },
    {
        "id": 2,
        "text": """2-тапсырма [3 ұпай].
Жер мен Айдың арасындағы орташа қашықтық r = 384 400 км. Жердің массасы m₁ = 5,97 ∙ 10²⁴ кг, ал Айдың массасы m₂ = 7,35 ∙ 10²² кг.
Жер мен Ай арасындағы бүкіләлемдік тартылыс күшін табыңыз.""",
        "correct_answer": """
        Шешу үлгісі:
        ХБЖ (SI): r = 384400 км = 3.844 ∙ 10^8 м.
        Формула: F = G * (m1 * m2) / r^2.
        Есептеу: F = (6.67e-11 * 5.97e24 * 7.35e22) / (3.844e8)^2
        Жауабы: F ≈ 1.98 ∙ 10^20 Н.
        """
    },
    {
        "id": 3,
        "text": """3-тапсырма [6 ұпай].
Жердің жасанды серігі Жер бетінен h = 2R биіктікте қозғалуда.
(R(жер) = 6400 км; M(жер) = 6 ∙ 10²⁴ кг).
a) Серіктің айналу периодын анықтаңыз.
b) Осы биіктіктегі еркін түсу үдеуін есептеңіз.""",
        "correct_answer": """
        Шешу үлгісі:
        ХБЖ (SI): R = 6.4 ∙ 10^6 м. h = 2R. Орбита радиусы r = R + h = 3R = 19.2 ∙ 10^6 м.
        a) v = √(GM/r). T = 2πr / v = 2π * √(r^3 / GM).
           T ≈ 2 * 3.14 * √((1.92e7)^3 / (6.67e-11 * 6e24)) ≈ 26400 с ≈ 7.3 сағат.
        b) g_h = GM / r^2 = GM / (3R)^2 = g_жер / 9.
           g_h ≈ 9.8 / 9 ≈ 1.09 м/с² (немесе формуламен есептесе де болады).
        """
    }
]

# --- САЙТ ИНТЕРФЕЙСІ ---
st.set_page_config(page_title="Динамика БЖБ", page_icon="🪐", layout="wide")

st.title(f"📝 {BJB_TITLE}")
st.markdown("**Нұсқаулық:** Есепті шығару жолын толық жазыңыз (Берілгені, ХБЖ, Формула, Есептеу).")
st.info("Бұл жүйе жауаптарды жасанды интеллект көмегімен тексереді.")
st.markdown("---")

# Оқушы мәліметі (Бүйірлік мәзір)
with st.sidebar:
    st.header("Оқушы мәліметі")
    student_name = st.text_input("Аты-жөніңіз:", placeholder="Мысалы: Арман Оспанов")
    student_class = st.selectbox("Сыныбыңыз:", ["9 A", "9 Ә", "9 Б", "9 В", "10 A"])
    st.warning("⚠️ Барлық өрістерді толтырыңыз.")

# Сұрақтар формасы
with st.form("bjb_physics_form"):
    student_answers = {}
    
    for question in QUESTIONS:
        st.subheader(f"🔹 {question['text']}")
        student_answers[question['id']] = st.text_area(
            f"Жауабыңыз ({question['id']}-тапсырма):", 
            height=150,
            placeholder="Берілгені: ...\nФормула: ...\nЕсептеу: ...",
            key=f"q_{question['id']}"
        )
        st.markdown("---")

    submit_button = st.form_submit_button("Жұмысты тексеру ✅", type="primary")

# --- ТЕКСЕРУ ЛОГИКАСЫ ---
if submit_button:
    # Тексерулер
    if not student_name:
        st.error("⚠️ Қате: Аты-жөніңізді жазбадыңыз!")
    elif not api_key: # ТҮЗЕТІЛГЕН ЖЕРІ: API_KEY емес, api_key
        st.error("⚠️ Қате: API кілт табылмады! Streamlit Secrets баптауларын тексеріңіз.")
    else:
        try:
            client = Groq(api_key=api_key) # ТҮЗЕТІЛГЕН ЖЕРІ
            
            # ЖИ-ге берілетін "Промпт"
            prompt_text = f"""
            Сен қатал бірақ әділ Физика мұғалімісің. Оқушының "Динамика негіздері" бойынша БЖБ жұмысын тексер.
            Оқушы: {student_name}, {student_class}
            
            БАҒАЛАУ КРИТЕРИЙІ (Әр есеп үшін):
            1. Формула дұрыс жазылған ба? (1 ұпай)
            2. ХБЖ (SI) жүйесіне дұрыс келтірілген бе (километр -> метр)? (1 ұпай)
            3. Есептеулері және жауабы дұрыс па? (1 ұпай)
            
            ТАПСЫРМАЛАР МЕН ДҰРЫС ЖАУАПТАР:
            """
            
            for q in QUESTIONS:
                ans = student_answers[q['id']] if student_answers[q['id']] else "Жауап жазылмаған"
                prompt_text += f"\n--- ТАПСЫРМА {q['id']} ---\n"
                prompt_text += f"Сұрақ: {q['text']}\n"
                prompt_text += f"Дұрыс шешім үлгісі: {q['correct_answer']}\n"
                prompt_text += f"Оқушының жауабы: {ans}\n"
            
            prompt_text += """
            
            НӘТИЖЕНІ МЫНА ФОРМАТТА ҚАЙТАР:
            Тіл: Қазақша.
            
            ### 📊 Нәтижелер:
            
            **1-тапсырма:**
            *   Бағалау: (Дұрыс/Қате/Жартылай) - (Ұпай саны)
            *   Түсініктеме: (Қай жерден қате кетті: формула ма, ХБЖ ма, есептеу ме?)
            
            **2-тапсырма:**
            ... (дәл солай)
            
            **3-тапсырма:**
            ... (дәл солай)
            
            ---
            **Жалпы қорытынды:**
            **Жинаған ұпайы:** X / 15
            **Мұғалімнің пікірі:** (Қысқаша мақтау немесе ескерту)
            """

            with st.spinner("Жауаптар талдануда... Бұл 5-10 секунд алуы мүмкін."):
                completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_text}],
                    model=MODEL_NAME,
                    temperature=0.3
                )
                response = completion.choices[0].message.content
                
                st.balloons()
                st.success("Тексеру аяқталды!")
                
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                    {response}
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Жүйелік қате орын алды: {e}")