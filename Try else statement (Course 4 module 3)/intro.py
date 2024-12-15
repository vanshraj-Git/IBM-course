def safe_divide(numerator,denominator):
    try:
        result = numerator / denominator
        return result
    except :
        print("Error: Cannot divide by zero.")
        return None
# Test case
numerator=int(input("Enter the numerator value:-"))
denominator=int(input("Enter the denominator value:-"))
print(safe_divide(numerator,denominator))