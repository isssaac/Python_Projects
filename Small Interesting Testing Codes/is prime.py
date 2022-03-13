def is_prime(num):
    if num > 1:
        for i in range(2,num):
           if (num % i) == 0:
               return False
    else:
       return true

def composite2(N):
    y=[]
    for x in range(3, N*10):
        if (is_prime(x) is False) and (x%2 != 0):
            y.append(x)
    return y[N-1]