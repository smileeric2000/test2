from collections import defaultdict

def calculate_temperament(answers):
    score = defaultdict(int)
    for answer in answers:
        if answer:
            score[answer] += 1
    return dict(score)

def get_dominant_temperament(score_dict):
    return max(score_dict, key=score_dict.get) if score_dict else None
