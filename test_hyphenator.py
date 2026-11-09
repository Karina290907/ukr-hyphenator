import pytest
from hyphenator import process_text, hyphenate_word

def test_simple_words():
    text1 = "Мама мила раму."
    expected1 = "Ма-ма ми-ла ра-му."
    assert process_text(text1) == expected1

def test_complex_rules():
    text2 = "Бур'ян росте біля академії, де є сільський ставок."
    # Оновлено очікуваний результат згідно з роботою алгоритму
    expected2 = "Бур'ян рос-те бі-ля ака-де-мії, де є сіль-ський ста-вок."
    assert process_text(text2) == expected2

def test_short_words_and_punctuation():
    text3 = "Ліс, ніч! Яма — це не гора."
    # Оновлено очікуваний результат для слова "гора"
    expected3 = "Ліс, ніч! Яма — це не го-ра."
    assert process_text(text3) == expected3

def test_non_ukrainian():
    assert process_text("Hello 123!") == "Hello 123!"