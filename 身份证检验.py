num = input('输入身份证,X请大写：')
s = 0
l = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
result = ['1','0','X','9','8','7','6','5','4','3','2']
if len(num) != 18:
    print('BAD NUM!')
else:
    for i in range(17):
        s += int(num[i]) * l[i]
    if result[s%11] == num[17]:
        print('GOOD')
    else:
        print('BAD')
