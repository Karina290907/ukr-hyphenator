import re
import pymorphy3

morph = pymorphy3.MorphAnalyzer(lang='uk')

def hyphenate_word(word):
    vowels = "аеєиіїоуюяАЕЄИІЇОУЮЯ"
    if len(word) <= 3 or not any(c in vowels for c in word):
        return word

    vowel_indices = [i for i, c in enumerate(word) if c in vowels]
    if len(vowel_indices) < 2:
        return word 

    points = []
    for i in range(len(vowel_indices) - 1):
        v1 = vowel_indices[i]
        v2 = vowel_indices[i+1]
        dist = v2 - v1
        split_point = v1 + 1 
        if dist > 2:
            split_point += 1
        if split_point == 1:
            continue
        if len(word) - split_point == 1:
            continue
        if split_point < len(word) and word[split_point].lower() in "ь'й’":
            split_point += 1
        points.append(split_point)

    if not points:
        return word

    res = ""
    prev = 0
    for p in points:
        res += word[prev:p] + "-"
        prev = p
    res += word[prev:]
    return res

def process_text(text):
    words_and_symbols = re.findall(r'\b\w+\b|\W+', text)
    result = []
    for item in words_and_symbols:
        if re.match(r'^[а-яА-ЯєЄіІїЇґҐ\'’ьЬ]+$', item): 
            result.append(hyphenate_word(item))
        else:
            result.append(item)
    return "".join(result)

def analyze_word_extra(word):
    clean_word = re.sub(r'[^а-яА-ЯєЄіІїЇґҐ\'’ьЬ]', '', word)
    if not clean_word:
        return None

    syllables = hyphenate_word(clean_word)
    parsed = morph.parse(clean_word)[0]

    pos_mapping = {
        'NOUN': 'Іменник', 'ADJF': 'Прикметник', 'ADJS': 'Короткий прикметник',
        'COMP': 'Компаратив', 'VERB': 'Дієслово', 'INFN': 'Інфінітив',
        'PRTF': 'Дієприкметник', 'PRTS': 'Короткий дієприкметник', 'GRND': 'Дієприслівник',
        'NUMR': 'Числівник', 'ADVB': 'Прислівник', 'NPRO': 'Займенник',
        'PREP': 'Прийменник', 'CONJ': 'Сполучник', 'PRCL': 'Частка', 'INTJ': 'Вигук'
    }
    pos_name = pos_mapping.get(parsed.tag.POS, "Невизначено")

    return f"**Слово:** {clean_word} | **Склади/Переноси:** {syllables} | **Частина мови:** {pos_name}"