## it has to start with 1 !!!

def main():
    n = int(input("Please enter an integer: "))
    factorial = 1
    for fact in range(n,1,-1): 
       factorial = fact * factorial
    print("The factorial of", n, "is", factorial)
    return

main()
