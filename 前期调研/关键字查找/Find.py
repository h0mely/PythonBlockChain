from MinimalChain import MinimalChain


# 初始化所需列表（数组）
next = [0] * 100
sub_str = [0] * 100
string = [0] * 1000000
times = list()

def getNext():  # 得到next数组
    i = 0
    j = -1
    next[i] = j
    while sub_str[i]:
        if (j == -1) or sub_str[i] == sub_str[j]:
            i += 1
            j += 1
            if sub_str[i] == sub_str[j]:
                next[i] = next[j]
            else:
                next[i] = j
        else:
            j = next[j]

def count():   # 查找子串出现的次数
    getNext()
    i = 0
    j = 0
    ans = 0
    while string[i]:
        if (j == -1) or (string[i] ==sub_str[j]):
            i += 1
            j += 1
            if not sub_str[j]:
                ans += 1
                j = next[j]
        else:
            j = next[j]
    return ans

'''  # 等加上二叉树结构之后再细分查找数据块
def que_para():   # 在一个数据块中查找关键词出现次数
    for i in range(0, len(str1) -1):
        sub_str[i] = str1[i]
    for i in range(0, len(str2) -1):
        string[i] = str2[i]
    count()
    return count
'''

# def que_arti():   # 在一个区块体中查找关键词出现次数

#     return count()


def query(str2):   # 关键字查找函数(查出一片文章中出现关键词组的次数)
    key_words = input('input a list of key words ：').split(' ')
    while len(key_words) < 3:
        key_words = input('the number of key words should more than 2：').split(' ')
    
    one_arti_times = 0
    # 给出所要进行查找的母串（即区块体中的数据项）
    for i in range(0, len(str2) -1):
        string[i] = str2[i]
    # 针对每一个关键字进行查找并返回该区块中若干关键词出现的总次数
    for x in key_words:
        # 设置子串（即一次查询一个关键词出现次数）
        for i in range(0, len(x)):
            sub_str[i] = x[i]
        one_arti_times += count()
        print(one_arti_times)

    times.append(one_arti_times)
    print(times)


if __name__ == "__main__":

    str2 = list(input())  # 母串（压缩后的文章）
    
    query(str2)