import streamlit as st
import pandas as pd
import random

# Загрузка Excel
@st.cache_data
def load_data():
    df = pd.read_excel("тест с ответами.xlsx", header=None)
    df = df.dropna(how='all').reset_index(drop=True)
    start_idx = df[df[0] == "№"].index[0] + 1
    df = df.iloc[start_idx:]
    df.columns = ["№", "Вопрос", "Вариант_1", "Вариант_2", "Вариант_3", "Вариант_4", "Ответ"]
    df = df.dropna(subset=["Вопрос", "Ответ"])
    return df

# Интерфейс
st.set_page_config(page_title="Тест Электромонтер", layout="centered")
st.title("🧐 Тест для электромонтеров")
st.markdown("Отвечайте на 25 случайных вопросов из базы")

data = load_data()
questions = data.sample(n=25, random_state=42).reset_index(drop=True)

score = 0
user_answers = []

with st.form("test_form"):
    for i, row in questions.iterrows():
        st.markdown(f"**{i+1}. {row['Вопрос']}**")
        options = [row["Вариант_1"], row["Вариант_2"], row["Вариант_3"], row["Вариант_4"]]
        user_choice = st.radio("", options, key=i)
        user_answers.append((user_choice, row["Ответ"]))

    submitted = st.form_submit_button("Проверить ответы")

if submitted:
    for user, correct in user_answers:
        if str(user).strip().lower() == str(correct).strip().lower():
            score += 1
    st.success(f"Ваш результат: {score} из 25 ({round(score / 25 * 100)}%)")
