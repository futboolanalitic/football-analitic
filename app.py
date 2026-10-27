Football Analyzer

Базовая версия проекта

import streamlit as st

st.set_page_config(
page_title="Football Analyzer",
page_icon="⚽",
layout="wide"
)

st.title("⚽ Football Analyzer")
st.subheader("Анализ футбольных матчей")

st.info(
"Добро пожаловать! Это первая версия программы. "
"Следующим шагом мы подключим футбольную статистику."
)

st.header("Настройки анализа")

min_odds = st.number_input(
"Минимальный коэффициент",
min_value=1.01,
max_value=20.0,
value=1.70,
step=0.10
)

st.write(f"Минимальный коэффициент: {min_odds:.2f}")

markets = st.multiselect(
"Выбери рынки для анализа",
[
"Победа хозяев",
"Ничья",
"Победа гостей",
"Тотал больше 1.5",
"Тотал больше 2.5",
"Обе команды забьют",
"Обе забьют + тотал больше 2.5"
],
default=["Тотал больше 1.5", "Обе команды забьют"]
)

st.header("Выбранные рынки")
if markets:
for market in markets:
st.write("⚽", market)
else:
st.warning("Выбери хотя бы один рынок.")

st.caption(
"Важно: коэффициенты и прогнозы не гарантируют выигрыш. "
"Для реального анализа необходимо подключить актуальные данные матчей."
)
