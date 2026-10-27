import streamlit as st
import math

st.set_page_config(
    page_title="Football Analyzer",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FOOTBALL ANALYZER")
st.caption("Анализ футбольных матчей и вероятностей рынков")

st.info(
    "Введи результаты последних матчей команд. "
    "Программа рассчитает вероятности на основе введённых данных."
)

st.header("1. Названия команд")

col1, col2 = st.columns(2)

with col1:
    home = st.text_input("Хозяева", "Real Madrid")

with col2:
    away = st.text_input("Гости", "Barcelona")

st.header("2. Последние результаты")

st.write(
    "Введи количество забитых голов в последних матчах "
    "через запятую, например: 2,1,3,0,2"
)

col1, col2 = st.columns(2)

with col1:
    hs = st.text_input(
        f"Забито хозяевами ({home})",
        "2,1,3,0,2"
    )
    hc = st.text_input(
        f"Пропущено хозяевами ({home})",
        "1,0,1,2,1"
    )

with col2:
    aws = st.text_input(
        f"Забито гостями ({away})",
        "1,2,0,2,1"
    )
    awc = st.text_input(
        f"Пропущено гостями ({away})",
        "1,2,1,0,2"
    )

st.header("3. Настройки")

minimum_odds = st.number_input(
    "Минимальный коэффициент для отбора",
    min_value=1.01,
    max_value=20.0,
    value=1.70,
    step=0.10
)

def parse_scores(text):
    values = [
        int(x.strip())
        for x in text.split(",")
    ]

    if not values or any(x < 0 or x > 20 for x in values):
        raise ValueError("Проверь введённые голы")

    return values

def average(values):
    return sum(values) / len(values)

def poisson(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)

if st.button("🔍 РАССЧИТАТЬ ПРОГНОЗ", type="primary"):

    try:
        home_scored = parse_scores(hs)
        home_conceded = parse_scores(hc)
        away_scored = parse_scores(aws)
        away_conceded = parse_scores(awc)

        if not all([
            home_scored,
            home_conceded,
            away_scored,
            away_conceded
        ]):
            raise ValueError("Не хватает данных")

        # Оценка ожидаемых голов по результатам команд
        home_xg = (
            average(home_scored) + average(away_conceded)
        ) / 2

        away_xg = (
            average(away_scored) + average(home_conceded)
        ) / 2

        # Вероятности количества голов: от 0 до 10
        max_goals = 10

        ph = [poisson(i, home_xg) for i in range(max_goals + 1)]
        pa = [poisson(i, away_xg) for i in range(max_goals + 1)]

        # Матрица вероятностей счёта
        p_home = 0
        p_draw = 0
        p_away = 0
        p_over15 = 0
        p_over25 = 0
        p_btts = 0
        p_btts_over25 = 0

        for h in range(max_goals + 1):
            for a in range(max_goals + 1):
                p = ph[h] * pa[a]

                if h > a:
                    p_home += p
                elif h == a:
                    p_draw += p
                else:
                    p_away += p

                if h + a >= 2:
                    p_over15 += p

                if h + a >= 3:
                    p_over25 += p

                if h > 0 and a > 0:
                    p_btts += p

                if h > 0 and a > 0 and h + a >= 3:
                    p_btts_over25 += p

        markets = [
            ("Победа хозяев", p_home),
            ("Ничья", p_draw),
            ("Победа гостей", p_away),
            ("Тотал больше 1.5", p_over15),
            ("Тотал больше 2.5", p_over25),
            ("Обе команды забьют", p_btts),
            ("Обе забьют + тотал больше 2.5", p_btts_over25)
        ]

        st.header("4. Результат анализа")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                f"Ожидаемые голы: {home}",
                f"{home_xg:.2f}"
            )

        with c2:
            st.metric(
                f"Ожидаемые голы: {away}",
                f"{away_xg:.2f}"
            )

        st.subheader("Вероятности рынков")

        results = []

        for name, probability in markets:
            # Вероятность округляется только для отображения
            fair_odds = (
                1 / probability
                if probability > 0
                else float("inf")
            )

            results.append({
                "Рынок": name,
                "Вероятность": f"{probability * 100:.1f}%",
                "Расчётный коэффициент": (
                    f"{fair_odds:.2f}"
                    if math.isfinite(fair_odds)
                    else "—"
                ),
                "Отбор": (
                    "Подходит по порогу"
                    if fair_odds >= minimum_odds
                    else "Ниже порога"
                )
            })

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Наиболее вероятные исходы")

        ranked = sorted(
            markets,
            key=lambda item: item[1],
            reverse=True
        )

        for name, probability in ranked[:3]:
            st.write(f"**{name}** — {probability * 100:.1f}%")

        st.warning(
            "Это математическая оценка по введённым результатам, "
            "а не гарантированный прогноз. Модель пока не учитывает "
            "составы, травмы, силу соперников и актуальные коэффициенты."
        )

    except (ValueError, ZeroDivisionError) as error:
        st.error(
            f"Ошибка во введённых данных: {error}. "
            "Вводи только целые числа через запятую."
        )

st.divider()

st.caption(
    "Football Analyzer — предварительная версия. "
    "Расчёты не гарантируют выигрыш."
)
