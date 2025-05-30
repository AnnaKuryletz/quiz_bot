def normalize_answer(answer: str) -> str:
    answer = answer.split('.')[0].split('(')[0]
    return answer.strip().lower()
