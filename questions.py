import re


questions_dict = {}

with open("quiz-questions/1vs1200.txt", "r", encoding="KOI8-R") as my_file:
    file_contents = my_file.read()

questions_pairs = re.findall(
    r'Вопрос\s*\d*:\s*(.*?)\s*Ответ:\s*(.*?)\s*(?:Автор:|Источник:|$)',
    file_contents,
    re.DOTALL
)

qa_dict = {q.strip(): a.strip() for q, a in questions_pairs}
