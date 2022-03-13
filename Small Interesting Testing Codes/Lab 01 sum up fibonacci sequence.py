##calculates the summation of Fibonacci number with each number too.
##For instance, if input is provided as 7 (n=7) then the displayed value is 20.
##0+1+1+2+3+5+8=20

n = int(input())
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
x = int()
for n in range(n, -1, -1):
    x += fibonacci(n)
print(x)
    