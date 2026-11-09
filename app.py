import streamlit as st
import re
from hyphenator import process_text, analyze_word_extra

st.set_page_config(page_title="Лінгвістичний аналізатор", page_icon="📚", layout="centered")
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 16px; border-radius: 8px; border: 1px solid #4CAF50;}
    .success-text { color: #2e7d32; font-size: 18px; font-weight: 500; padding: 15px; background-color: #e8f5e9; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

st.title("📚 Аналізатор українського тексту")
st.write("Цей застосунок розбиває слова на склади за правилами переносу та визначає частини мови.")

text_input = st.text_area(
    "Введіть текст українською мовою для аналізу:", 
    height=150, 
    placeholder="Наприклад: Комп'ютерна лінгвістика вивчає природні мови."
)

if st.button("Проаналізувати текст", type="primary"):
    if not text_input.strip():
        st.error("Помилка: Вхідний текст не може бути порожнім. Будь ласка, введіть текст.")
    elif not bool(re.search(r'[а-яА-ЯєЄіІїЇґҐ]', text_input)):
        st.error("Помилка: У тексті не знайдено літер українського алфавіту. Перевірте мову вводу.")
    else:
        st.subheader("Результат розбиття на склади (переноси):")
        result = process_text(text_input)
        st.markdown(f'<div class="success-text">{result}</div>', unsafe_allow_html=True)

        st.subheader("Додаткове завдання (Склади + Частина мови):")
        words = re.findall(r'[а-яА-ЯєЄіІїЇґҐ\'’ьЬ]+', text_input)
        unique_words = list(set(words))

        for w in unique_words[:10]:
            analysis = analyze_word_extra(w)
            if analysis:
                st.info(analysis)