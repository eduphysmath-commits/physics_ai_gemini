import streamlit as st
import requests
import streamlit.components.v1 as components
import json

# --- 1. БАЗА БАПТАУЛАРЫ ---
URL = "https://bjqoazdkiyhrdrfkkgaz.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJqcW9hemRraXlocmRyZmtrZ2F6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk3NTM4NjIsImV4cCI6MjA4NTMyOTg2Mn0.0t4S6fa9CmYa6WBdDvkVr4V4H91wLx9xLYtcEdriX4I"
TABLE_NAME = "tjb_8_synyp"

st.set_page_config(page_title="8-СЫНЫП ФИЗИКА БЖБ", layout="wide", page_icon="⚡")

# Сессияны басқару
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- 2. СТИЛЬ (Дизайнды жақсарту) ---
st.markdown("""
    <style>
    * { -webkit-user-select: none; user-select: none; } 
    .stApp { background-color: #f8f9fa; }
    .stRadio > div { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .stTextArea textarea { font-size: 16px; border-radius: 10px; }
    .main-title { color: #1e3a8a; text-align: center; font-weight: 800; }
    .result-card { background-color: #ffffff; padding: 25px; border-radius: 15px; border-left: 5px solid #3b82f6; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

def send_data(payload):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    return requests.post(f"{URL}/rest/v1/{TABLE_NAME}", json=payload, headers=headers)

# --- 3. БАСТЫ БЕТ ---
st.markdown("<h1 class='main-title'>⚡ 8-СЫНЫП ФИЗИКА: БЖБ ЖҰМЫСЫ</h1>", unsafe_allow_html=True)

if st.session_state.submitted:
    st.balloons()
    st.success("🎉 Жұмысың сәтті қабылданды! Енді мұғалім тексергенше күте тұр немесе төменнен нәтижеңді ізде.")
    if st.button("Жаңадан бастау 🔄"):
        st.session_state.submitted = False
        st.rerun()
else:
    st.info("ℹ️ **Нұсқаулық:** Сұрақтарды мұқият оқып, жауап беріңіз. Барлық өрістерді толтыру міндетті. Максималды ұпай: 20.")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Оқушының аты-жөні:", placeholder="Мысалы: Оспанов Арман")
    with col2:
        s_class = st.selectbox("🏫 Сыныбыңыз:", ["8 А", "8 Б", "8 В", "8 Г"])

    if name:
        # ANTI-CHEAT JS
        components.html(f"""
            <script>
            let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            let alarmInterval;
            let isSubmitting = false;

            function startAlarm() {{
                if (isSubmitting) return;
                if (audioCtx.state === 'suspended') {{ audioCtx.resume(); }}
                alarmInterval = setInterval(() => {{
                    let osc = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(880, audioCtx.currentTime);
                    gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.2);
                }}, 300);
            }}

            function stopAlarm() {{ clearInterval(alarmInterval); }}

            document.addEventListener("visibilitychange", function() {{
                if (document.hidden && !isSubmitting) {{
                    startAlarm();
                    setTimeout(function() {{
                        if (document.hidden && !isSubmitting) {{
                            const payload = {{
                                student_name: "{name}",
                                student_class: "{s_class}",
                                status: "cheated",
                                ai_feedback: "🚫 Жұмыс ЖОЙЫЛДЫ: Тест кезінде басқа терезеге ауыстыңыз (Анти-чит)."
                            }};
                            fetch('{URL}/rest/v1/{TABLE_NAME}', {{
                                method: 'POST',
                                headers: {{ 'apikey': '{KEY}', 'Authorization': 'Bearer {KEY}', 'Content-Type': 'application/json' }},
                                body: JSON.stringify(payload)
                            }}).then(() => {{ 
                                isSubmitting = true;
                                stopAlarm();
                                window.parent.location.reload(); 
                            }});
                        }}
                    }}, 5000);
                }} else {{
                    stopAlarm();
                }}
            }});
            </script>
        """, height=0)

        with st.form("exam_8_physics"):
            st.subheader("📍 А БӨЛІМІ: Тест тапсырмалары (10 ұпай)")
            q1 = st.radio("1. Ішкі энергияның өлшем бірлігі қандай?", ["A) Ватт", "B) Джоуль", "C) Ньютон", "D) Паскаль"], index=None)
            q2 = st.radio("2. Жылу берілудің қай түрі вакуумда жүзеге асады?", ["A) Конвекция", "B) Жылу өткізгіштік", "C) Сәуле шығару", "D) Диффузия"], index=None)
            q3 = st.radio("3. Судың қайнау температурасы қалыпты жағдайда қанша?", ["A) 0°C", "B) 80°C", "C) 100°C", "D) 273°C"], index=None)
            q4 = st.radio("4. Термодинамиканың 1-заңының формуласы:", ["A) Q = ΔU + A", "B) Q = cmΔt", "C) η = A/Q", "D) pV = nRT"], index=None)
            q5 = st.radio("5. Булану кезінде сұйықтықтың температурасы қалай өзгереді?", ["A) Жоғарылайды", "B) Төмендейді", "C) Өзгермейді", "D) Басында артады"], index=None)
            q6 = st.radio("6. Элементар электр зарядының мәні қанша?", ["A) 1.6 * 10^-19 Кл", "B) 9 * 10^9 Кл", "C) 1.6 * 10^-31 Кл", "D) 1 Кл"], index=None)
            q7 = st.radio("7. Аттас зарядтар (+ және +) қалай әрекеттеседі?", ["A) Тартылады", "B) Тебіледі", "C) Әрекеттеспейді", "D) Бейтараптанады"], index=None)
            q8 = st.radio("8. Дененің электрленгенін анықтайтын аспап:", ["A) Термометр", "B) Барометр", "C) Электроскоп", "D) Спидометр"], index=None)
            q9 = st.radio("9. Кулон заңының формуласы:", ["A) F = ma", "B) F = k*q1*q2/r^2", "C) F = mg", "D) E = F/q"], index=None)
            q10 = st.radio("10. Шыны таяқшаны жібекке үйкегенде таяқша қандай заряд алады?", ["A) Теріс (-)", "B) Оң (+)", "C) Бейтарап (0)", "D) Басында оң"], index=None)

            st.subheader("📍 В БӨЛІМІ: Қысқа жауаптар (6 ұпай)")
            q11 = st.text_area("11. Неліктен металл қасық ағаш қасыққа қарағанда суық болып көрінеді?", height=70, placeholder="Өз жауабыңызды жазыңыз...")
            q12 = st.text_area("12. Егер екі зарядтың арақашықтығын 3 есе арттырсақ, Кулон күші қалай өзгереді?", height=70, placeholder="Есептелу жолын немесе жауабын жазыңыз...")

            st.subheader("📍 С БӨЛІМІ: Есеп шығару (4 ұпай)")
            q13 = st.text_area("13. Есеп: r = 10 см, q1 = 2*10^-7 Кл, q2 = 5*10^-7 Кл. Өзара әрекеттесу күшін (F) табыңыз:", height=100, placeholder="Шешуі мен жауабын көрсетіңіз...")

            submit_btn = st.form_submit_button("ЖҰМЫСТЫ АЯҚТАУ ✅")

            if submit_btn:
                if not name or len(name) < 3:
                    st.error("❌ Өтінеміз, толық аты-жөніңізді жазыңыз!")
                else:
                    all_answers = {
                        "section_a": [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10],
                        "section_b": {"q11": q11, "q12": q12},
                        "section_c": {"q13": q13}
                    }
                    payload = {
                        "student_name": name, 
                        "student_class": s_class,
                        "answers": all_answers, # json.dumps-сыз жіберу (jsonb үшін)
                        "status": "pending"
                    }
                    resp = send_data(payload)
                    if resp.status_code in [200, 201, 204]:
                        st.session_state.submitted = True
                        st.rerun()
                    else:
                        st.error(f"⚠️ Қате кетті: {resp.text}")

# --- 4. НӘТИЖЕНІ ІЗДЕУ ---
st.markdown("---")
st.markdown("### 🔎 Нәтижені тексеру")
search_query = st.text_input("Аты-жөніңізді енгізіңіз (мысалы: Арман):", key="search_input")

if search_query:
    s_headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
    res = requests.get(f"{URL}/rest/v1/{TABLE_NAME}?student_name=ilike.*{search_query}*&select=*&order=id.desc", headers=s_headers)
    
    if res.status_code == 200:
        results = res.json()
        if len(results) > 0:
            for data in results:
                with st.container():
                    st.markdown(f"#### 👤 {data['student_name']} ({data['student_class']})")
                    if data['status'] == 'cheated':
                        st.error(data['ai_feedback'])
                    elif data['status'] == 'pending':
                        st.warning("⏳ Жұмысың әлі тексерілуде... Сәлден соң қайта тексеріп көр.")
                    else:
                        col_score, col_fb = st.columns([1, 3])
                        with col_score:
                            st.metric("Жалпы ұпай", f"{data.get('score', 0)} / 20")
                        with col_fb:
                            with st.expander("📝 Мұғалімнің кері байланысы (AI)", expanded=True):
                                st.write(data.get('ai_feedback', 'Кері байланыс дайындалуда...'))
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("ℹ️ Бұл есім бойынша жұмыс табылған жоқ. Аты-жөніңізді дұрыс жазғаныңызды тексеріңіз.")
    else:
        st.error(f"⚠️ Базаға қосылу қатесі: {res.status_code}")