def classify_authorization(api_succeeded, error_code=None):
    if api_succeeded:
        return "FAIL"
    elif error_code in ("AccessDenied", "AccessDeniedException"):
        return "PASS"
    elif error_code == "NoSuchEntity":
        return "INCONCLUSIVE"
    else:
        return "ERROR"

if __name__ == "__main__":
    print(classify_authorization(True))
    print(classify_authorization(False, "AccessDenied"))
    print(classify_authorization(False, "NoSuchEntity"))
    print(classify_authorization(False, "Throttling"))
