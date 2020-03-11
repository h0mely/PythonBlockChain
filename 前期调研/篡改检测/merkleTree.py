# coding: utf-8
import math
import random
import hashlib
check = [0 for i in range(7)]
"""
1. 创建默克尔树（暂时用make_data生成随机数）
2. 检测被修改位置（test中修改了节点7，用函数check_data检查出3节点的子节点出错
"""
class Node:
    def __init__(self, item):
        self.item = item
        self.child1 = None
        self.child2 = None
        self.hash = None
        self.data = None

    def change_data(self, data):
        self.data = data
        # hexdigest()返回摘要，作为十六进制数据字符串值 [8:-8]将32位MD5转换为16进制
        self.hash = hashlib.md5(data.encode('utf-8')).hexdigest()[8:-8]
        print("make_hash", self.hash, "size", len(self.hash), end=" ")
        return self.hash

    @property
    def get_hash(self):
        return self.hash


class Tree:
    def __init__(self):
        self.root = None
        
    def add(self, item):                #逐层添加子节点
        node = Node(item)
        end_str = make_data(item)       #造数据 hash
        print("add node", item)
        if end_str !=None and end_str != -1:
            node.change_data(end_str)
            print("data= %s " % (node.data))
            print("hash= %s " % (node.hash))
        if self.root is None:
            self.root = node
        else:
            q = [self.root]
            while True:
                pop_node = q.pop(0)
                if pop_node.child1 is None:
                    pop_node.child1 = node
                    return
                elif pop_node.child2 is None:
                    pop_node.child2 = node
                    return
                else:
                    q.append(pop_node.child1)
                    q.append(pop_node.child2)

    def reload_hash(self):  # 层次遍历更新hash
        if self.root is None:
            return None
        q = [self.root]
        item = [(self.root.item, self.root.data, self.root.hash)]
        while q != []:
            pop_node = q.pop(0)
            if pop_node.child1 and pop_node.child2:
                if pop_node.child1.hash and pop_node.child2.hash:
                    print("更新基础节点", pop_node.item, end=" ")
                    end_str = pop_node.child1.hash+pop_node.child2.hash
                    end_hash = pop_node.change_data(end_str)
                    print("end_hash= %s " % (end_hash))

            if pop_node.child1 is not None:
                q.append(pop_node.child1)

            if pop_node.child2 is not None:
                q.append(pop_node.child2)
        return

    """
    测试函数，修改节点7的值
    """
    def test(self):
        print("change node")
        if self.root is None:
            return None
        q = [self.root]
        item = [(self.root.item, self.root.data, self.root.hash)]
        while q != []:
            pop_node = q.pop(0)
            if pop_node.child1 == None and pop_node.child2 == None:
                print("修改叶节点", pop_node.item, end=" ")
                end_str = "changed"
                end_hash = pop_node.change_data(end_str)
                print("end_hash= %s " % (end_hash))
                return

            if pop_node.child1 is not None:
                q.append(pop_node.child1)

            if pop_node.child2 is not None:
                q.append(pop_node.child2)

        return
    """
    找出出错的节点的父节点（基础节点）
    """
    def check_data(self):
        if self.root is None:
            return None
        # 层次遍历，找到hash和原来不一样的节点 只需检查基础节点
        q = [self.root]
        item = [(self.root.item, self.root.data, self.root.hash)]
        while q != []:
            pop_node = q.pop(0)
            if pop_node.child1 and pop_node.child2:  # 当它是基础节点时
                print("checking...")
                #重新计算一遍自己的hash
                end_str = pop_node.child1.hash + pop_node.child2.hash
                new_hash = hashlib.md5(end_str.encode('utf-8')).hexdigest()[8:-8]
                #current_hash = pop_node.change_data(end_str)
                print(new_hash)
                print(pop_node.get_hash)
                if new_hash == pop_node.get_hash:
                    check[pop_node.item] = 0
                else:
                    check[pop_node.item] = 1
                    print("the child of" , pop_node.item, "is wrong")

            if pop_node.child1 is not None:
                q.append(pop_node.child1)
                item.append((pop_node.child1.item, pop_node.child1.data, pop_node.child1.hash))

            if pop_node.child2 is not None:
                q.append(pop_node.child2)
                item.append((pop_node.child2.item, pop_node.child2.data, pop_node.child2.hash))
        return item

    def traverse(self):  # 层次遍历
        if self.root is None:
            return None
        q = [self.root]
        item = [(self.root.item, self.root.data, self.root.hash)]
        while q != []:
            pop_node = q.pop(0)
            if pop_node.child1 is not None:
                q.append(pop_node.child1)
                item.append((pop_node.child1.item, pop_node.child1.data, pop_node.child1.hash))

            if pop_node.child2 is not None:
                q.append(pop_node.child2)
                item.append((pop_node.child2.item, pop_node.child2.data, pop_node.child2.hash))
        return item

def make_data(i):
    if i>6 and i<15:
        raw_str = "randomdata15310120233"
        nums = math.floor(1e5 * random.random())
        nums = str(nums)
        nums = nums.zfill(5)
        end_str = raw_str + nums
        print("end_str", end_str)
        return end_str
    elif i>=0 and i<7:
        return None
    else:
        return -1

# t = Tree()
# for i in range(15):
#     t.add(i)


def main():
    t = Tree()
    for i in range(7):      # 基础节点
        t.add(i)

    for i in range(7, 15):  # 带数据的节点
        t.add(i)
    for i in range(3, 0, -1):    #刷新基础节点hash值
        print("第", i, '层节点hash刷新:')
        print(t.reload_hash())

    print('层次遍历:\n节点名:数据：hash值\n', t.traverse())
    print(check)
    t.test()

    print("\r节点hash检查:")
    t.check_data()
    print(check)        #当数值为1 说明其两个子节点中的一个出错

if __name__ == '__main__':
    main()
