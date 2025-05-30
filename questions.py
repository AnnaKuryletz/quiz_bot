import re


def load_questions_from_file(file_path: str, encoding: str = "KOI8-R") -> dict:
    with open(file_path, "r", encoding=encoding) as file:
        content = file.read()

    question_answer_pairs = re.findall(
        r'Вопрос\s*\d*:\s*(.*?)\s*Ответ:\s*(.*?)\s*(?:Автор:|Источник:|$)',
        content,
        re.DOTALL
    )

    return {q.strip(): a.strip() for q, a in question_answer_pairs}
