import random
'''计算A的数量，需要输入两个字符串一个是用户输入的，一个是随机生成的，他对
输入的连个字符串一样比对相应位置，找出A的个数并且会记录每一个A的位置（以数组形式存储）-数组长度，因为在后边会将
A对应位置的字符从两个字符串中

'''
def A_count(string_number,string_answer):
    A = 0
    right_opt=[]
    for i in range(0,4):
        if string_answer[i] == string_number[i]:
            A = A + 1
            right_opt.append(i-len(right_opt))
    return A,right_opt

'''计算B的数量，需要输入两个字符串，这两个字符串是剔除了A所在位置的字符的字符串
然后循环比对两个字符串，当发现当前位置用户答案在该位置与系统中随机数相同则B数量加1
'''
def B_count(string_number,string_answer):
    B = 0
    for i in range(0,len(string_number)):
        for j in range(0,len(string_answer)):
            if string_answer[j] == string_number[i]:
                B = B+1
                break
    return B
#检查输入的合法性
def check(answer):
    if answer == 'answer':
        return 'answer'
    elif answer == 'next':
        return 'next'
    elif answer == 'over':
        return 'over'
    elif answer == 'heartbeat':
        return 'heartbeat'
    else:
        try:
            answer = int(answer)
            answer = str(answer)
            if len(answer) != 4:
                return True
            else:
                return False
        except:
            return True
#随机生成一个四位数
number =str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9))

#设置的标志变量，当发现A的数量为4时，退出while循环，游戏结束
flag = True
if __name__ == '__main__':
    while flag:
        #用户输入
        answer = input('输入你的答案（输入answer获取答案huozhe输入next进入下一轮）：')
        
        ch = check(answer)
        
        if ch == 'next':
            number =str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9))

            continue
        elif ch == 'answer':
            print('答案为：',number)
        elif ch == True:
            while ch:
                print('输入不合法重新输入')
                answer = input('输入你的答案：')
                ch = check(answer)
    
        
        #将生成的数字和输入数字全部转化为字符串
        string_number = str(number)
        string_answer = str(answer)
        
        
        
        #调用A_count函数，计算A个数和要删除的序列right_opt
        A,right_opt = A_count(string_number, string_answer)
        #遍历right_count循环删除A的位置
        for i in right_opt:
            string_answer = string_answer[:i]+string_answer[i+1:]
            string_number = string_number[:i]+string_number[i+1:]
        
        B = B_count(string_number, string_answer)
        #print(A,right_opt,string_answer,string_number)
        print(str(A)+'A'+str(B)+'B')
        #判断结束条件
        if A==4:
            go_on = input('是否继续Y/N:')
            while go_on !='Y' and go_on != 'N':
                go_on = input('是否继续Y/N:')
            if go_on == 'Y':
                number =str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9))
            elif go_on == 'N':
                flag = False
        