def singleDigit(N):
    while N > 9:
        N = sum(map(int, str(N)))
    return N