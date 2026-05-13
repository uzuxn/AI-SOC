def calculate_risk_score(probability, threat_reputation=0.0):
    return round((0.6 * probability)+(0.4 * probability), 2)

def classify_risk(score):
    if score >= 0.9:
        return "Critical"
    elif score >= 0.75:
        return "High Risk"
    elif score >= 0.5:
        return "Suspicious"
    else:
        return "Normal"