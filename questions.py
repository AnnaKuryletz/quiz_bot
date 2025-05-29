import re
qaestions_dict = {}

with open("quiz-questions/1vs1200.txt", "r", encoding="KOI8-R") as my_file:
  file_contents = my_file.read()

qaestions_pairs = re.findall(
    r'Вопрос\s*\d*:\s*(.*?)\s*Ответ:\s*(.*?)\s*(?:Автор:|Источник:|$)',
    file_contents,
    re.DOTALL
)

qa_dict = {q.strip(): a.strip() for q, a in qaestions_pairs}

print(f"Найдено пар: {len(qa_dict)}")
for q, a in qa_dict.items():
    print(f"ВОПРОС: {q}\nОТВЕТ: {a}\n{'-'*40}")
