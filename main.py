import streamlit as st
import requests

# БАПТАУЛАР
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]

def post_to_supabase(data):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    return requests.post(f"{URL}/rest/v1/bjb_results", json=data, headers=headers)

st.set_page_config(page_title="Физика ТЖБ", layout="wide")
st.title("9-СЫНЫП ФИЗИКА. 1-ЖАРТЫЖЫЛДЫҚ БАҚЫЛАУ")
st.info("Уақыты: 45 минут | Жалпы ұпай: 25 ұпай")

with st.sidebar:
    st.header("Оқушы мәліметі")
    student_name = st.text_input("Аты-жөніңіз:")
    student_class = st.selectbox("Сыныбыңыз:", ["9 A", "9 Ә", "9 Б", "9 В"])

with st.form("tjb_form"):
    st.header("А БӨЛІМІ: Тест тапсырмалары (10 ұпай)")
    
    q1 = st.radio("1. Материялық нүкте шеңбер бойымен қозғалып, бастапқы нүктесіне қайта келді. Орын ауыстыруы (S) мен жүрген жолы (l) қандай?", ["A) S = 2πR; l = 0", "B) S = 0; l = 2πR", "C) S = 0; l = 0", "D) S = 2πR; l = 2πR"], index=None)
    q2 = st.radio("2. Дене 5 секунд ішінде жылдамдығын 0-ден 10 м/с-қа дейін арттырды. Үдеуі?", ["A) 5 м/с²", "B) 2 м/с²", "C) 10 м/с²", "D) 0 м/с²"], index=None)
    q3 = st.radio("3. Жұлдыздардың өзара орналасуын сақтайтын тұрақты топтар?", ["A) Галактикалар", "B) Планеталар", "C) Шоқжұлдыздар", "D) Тұмандықтар"], index=None)
    q4 = st.radio("4. Инерциялық санақ жүйесі дегеніміз?", ["A) Үдеумен қозғалатын жүйе", "B) Тыныштықтағы немесе бірқалыпты түзусызықты қозғалатын жүйе", "C) Шеңбер бойымен қозғалатын жүйе", "D) Кез келген жүйе"], index=None)
    q5 = st.radio("5. Ауырлық күшінің формуласы:", ["A) F = kx", "B) F = μN", "C) F = mg", "D) F = ma"], index=None)
    q6 = st.radio("6. Ньютонның үшінші заңы бойынша күштер:", ["A) Әр түрлі денелерге әсер етеді, бағыттары қарама-қарсы, шамалары тең", "B) Бір денеге әсер етеді, теңгеріледі", "C) Бағыттары бірдей, шамалары әр түрлі", "D) Тек тыныштықтағы денелерге әсер етеді"], index=None)
    q7 = st.radio("7. Қашықтықты 2 есе арттырсақ, тартылыс күші қалай өзгереді?", ["A) 2 есе артады", "B) 2 есе кемиді", "C) 4 есе артады", "D) 4 есе кемиді"], index=None)
    q8 = st.radio("8. Кеплердің 1-заңы бойынша ғаламшарлар траекториясы қандай?", ["A) Шеңбер", "B) Эллипс", "C) Парабола", "D) Түзу"], index=None)
    q9 = st.radio("9. Центрге тартқыш үдеудің формуласы:", ["A) a = v/t", "B) a = v²/R", "C) a = ωR", "D) a = 4π²R"], index=None)
    q10 = st.radio("10. Лифт 10 м/с² үдеумен төмен құлағанда, жолаушының салмағы?", ["A) P = mg", "B) P = 2mg", "C) P = 0 (Салмақсыздық)", "D) P = m(g-a)"], index=None)

    st.header("В БӨЛІМІ: Қысқа жауапты тапсырмалар (12 ұпай)")
    st.write("11-тапсырма. Автобус жүріп келе жатып кенеттен тоқтағанда, жолаушылар алға қарай еңкейеді")
    q11a = st.text_input("а) Бұл құбылыс физикада қалай аталады?")
    q11b = st.text_input("b) Инерция құбылысына өмірден бір мысал келтіріңіз:")
    
    st.write("12-тапсырма. Динамика есебі")
    q12a = st.text_input("а) Дененің үдеуі неге тең (F=8H, m=2кг)?")
    q12b = st.text_area("b) Күшті 2 есе арттырсақ, үдеу қалай өзгереді? Түсіндіріңіз:")
    
    st.write("13-тапсырма. Астрономия")
    q13a = st.text_area("а) Жұлдыз бен ғаламшардың айырмашылығы?")
    q13b = st.text_input("b) Күн жүйесіндегі ең үлкен ғаламшар:")

    st.header("С БӨЛІМІ: Талдау тапсырмасы (3 ұпай)")
    st.write("14-тапсырма. Горизонталь лақтырылған дене (h=20м, v₀=10м/с)")
    q14a = st.text_input("a) Түсу уақыты (t):")
    q14b = st.text_input("b) Түсу қашықтығы (L):")
    q14c = st.text_input("c) Траектория пішіні қандай?")

    submit = st.form_submit_button("Жұмысты аяқтау және тапсыру ✅")

if submit:
    if not student_name:
        st.error("Аты-жөніңізді жазыңыз!")
    else:
        all_answers = {
            "test": [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10],
            "b_section": {"11a": q11a, "11b": q11b, "12a": q12a, "12b": q12b, "13a": q13a, "13b": q13b},
            "c_section": {"14a": q14a, "14b": q14b, "14c": q14c}
        }
        res = post_to_supabase({"student_name": student_name, "student_class": student_class, "answers": all_answers, "status": "pending"})
        if res.status_code in [200, 201]:
            st.success("Жұмысың сәтті тапсырылды!")