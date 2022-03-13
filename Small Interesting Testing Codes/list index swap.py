def list_swap(lst):
    for i in range(len(lst)-1):
        if i % 2 != 1:
            lst[i], lst[i+1] = lst[i+1], lst[i]
            i += 1
    return lst
    
print(list_swap([12,32,54,24,51,23.54]))
##returns [32, 12, 24, 54, 23.54, 51]
    
