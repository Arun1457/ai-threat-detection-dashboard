def assign_severity(row):
    score = row['confidence']

    if score > 0.65:
        return 'Critical'
    elif score > 0.6:
        return 'High'
    elif score > 0.5:
        return 'Medium'
    elif score > 0.3:
        return 'Low'
    else:
        return 'Normal'