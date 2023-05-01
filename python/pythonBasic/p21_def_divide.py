def divide(a, b):
    return (a / b, a % b)

a = input("Input first number : ")
b = input("Input Second number : ")

print(f"Input number {a} / {b}")
q, r = divide(int(a), int(b))
print("Quotient : ", int(q))
print("Remainder : ", r)
