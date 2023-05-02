import p25_timer

timer = p25_timer.counter2()
counter = 0

for k in range(1, 101):
    if k % 7 == 0:
        counter = timer()
print(f"result : {counter}")
