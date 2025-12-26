
def score_university(student, uni, weights):
    score = 0
    score += weights["acceptance_rate"]
    if uni["min_gpa"] <= student["gpa"]:
        score += weights["success_history"]
    if uni["scholarship_available"]:
        score += weights["scholarship_weight"]
    return score
