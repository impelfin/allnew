def prime(n):
    for k in (2, n):
        if n % k == 0:
            break
    if k == n:
        return 1
    else:
        return 0
