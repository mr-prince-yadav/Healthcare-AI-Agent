def generate_recommendations(p):
    rec = []

    bmi = round(p["weight"]/((p["height"]/100)**2),1)

    if bmi < 18.5:
        rec.append("Underweight: increase calories and protein.")
    elif bmi > 25:
        rec.append("Overweight: reduce carbs and sugar.")

    if p["sleep_hours"] < 6:
        rec.append("Sleep deficit detected.")

    if p["glucose"] > 140:
        rec.append("High glucose level.")

    if p["heart_rate"] < 50 or p["heart_rate"] > 100:
        rec.append("Abnormal heart rate.")

    if "diabetes" in p.get("disease","").lower():
        rec.append("Strict diabetic diet advised.")

    return rec
