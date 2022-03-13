# Isaac Huang, SID: 23019722
def main(csvfile, year, type):
    if type == 'stats':
        mn1, mx1, avg1, std1 = des_stat(csvfile, year)
        return mn1, mx1, avg1, std1
    elif type == 'corr':
        mnr1, mxr1, avgr1, stdr1 = des_stat(csvfile, year[0])
        mnr2, mxr2, avgr2, stdr2 = des_stat(csvfile, year[1])
        mn2 = correlation(mnr1, mnr2)
        mx2 = correlation(mxr1, mxr2)
        avg2 = correlation(avgr1, avgr2)
        std2 = correlation(stdr1, stdr2)
        return mn2, mx2, avg2, std2

# for finding non-zero min   
def min_nz(month):
    target = []
    if sum(month) == 0:
        return 0.0
    else:
        for day in month:
            if day != 0:
                target.append(day)
        return min(target)

# for filling up empty data or data with negative sign with '0' 
def fill(w):
    if w < '0':
        return '0'
    else:
        return str(w)

# for calculating standard deviation of month data
def std_dev(month):
    suma = 0
    for day in month:
        suma += pow((day-sum(month)/len(month)), 2)
    dev = pow((suma/len(month)), 0.5)
    return dev

# for calculating correlation coefficient of two lists
def correlation(list1, list2):
    sum1 = 0
    sumx = 0
    sumy = 0
    for x, y in zip(list1, list2):
        xxm = float(x - sum(list1)/len(list1))
        yym = float(y - sum(list2)/len(list2))
        sum1 += xxm * yym
        sumx += pow(xxm, 2)
        sumy += pow(yym, 2)
    div = pow((sumx * sumy), 0.5)
    cor = round(sum1/div, 4)
    return cor

# for calculating basic descriptive statistics of whole year data
def des_stat(csvfile, year):
    yr = str(year)
    data = [[],[],[],[],[],[],[],[],[],[],[],[]]
    f = open(csvfile,"r")
    for line in f:
        a, b, c, d, e = list(line.strip().split(","))
        if b == yr:
            for i in range(1, 13):
                c = float(c)
                if c == i:
                    e = float(fill(e))
                    data[i-1].append(e)           
    f.close()
    mindata = [min_nz(data[0]),min_nz(data[1]),min_nz(data[2]),min_nz(data[3]),min_nz(data[4]),min_nz(data[5]),min_nz(data[6]),min_nz(data[7]),min_nz(data[8]),min_nz(data[9]),min_nz(data[10]),min_nz(data[11])]
    maxdata = [max(data[0]),max(data[1]),max(data[2]),max(data[3]),max(data[4]),max(data[5]),max(data[6]),max(data[7]),max(data[8]),max(data[9]),max(data[10]),max(data[11])]
    meandata = [sum(data[0])/len(data[0]),sum(data[1])/len(data[1]),sum(data[2])/len(data[2]),sum(data[3])/len(data[3]),sum(data[4])/len(data[4]),sum(data[5])/len(data[5]),sum(data[6])/len(data[6]),sum(data[7])/len(data[7]),sum(data[8])/len(data[8]),sum(data[9])/len(data[9]),sum(data[10])/len(data[10]),sum(data[11])/len(data[11])]
    meanround = [round(element, 4) for element in meandata]
    stddv = [std_dev(data[0]),std_dev(data[1]),std_dev(data[2]),std_dev(data[3]),std_dev(data[4]),std_dev(data[5]),std_dev(data[6]),std_dev(data[7]),std_dev(data[8]),std_dev(data[9]),std_dev(data[10]),std_dev(data[11])]
    stddvround = [round(element, 4) for element in stddv]
    return mindata, maxdata, meanround, stddvround
    