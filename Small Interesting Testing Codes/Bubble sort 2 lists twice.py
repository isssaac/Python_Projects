def list_sorting(lst1,lst2):
    n = len(lst1)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if lst2[j]<lst2[j+1]:
                lst1[j], lst1[j+1] = lst1[j+1], lst1[j]
                lst2[j], lst2[j+1] = lst2[j+1], lst2[j]
    for i in range(n-1):
        for j in range(0, n-i-1):
            if lst2[j]==lst2[j+1]:
                if lst1[j]>lst1[j+1]:
                    lst1[j], lst1[j+1] = lst1[j+1], lst1[j]
    return lst1, lst2

print(list_sorting(['Chris','Amanda','Boris','Charlie'],[35,43,55,35]))
# will return (['Boris', 'Amanda', 'Charlie', 'Chris'], [55, 43, 35, 35])