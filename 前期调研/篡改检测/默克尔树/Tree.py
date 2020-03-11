import hashlib

from Tree_node import *
#本函数实现功能：
#要求数据：将文章各段存入列表中
#构造树：creat_leaf_node(列表)
#检测篡改(存储源文件的列表) 返回值为段落标记signal

class Tree:
    def __init__(self):
        self.change_location=[]               #用于存储该默克尔树被篡改时的被篡改位
    def get_hash(self,item):       #传入内容计算哈希值
        m = hashlib.md5()  # 括号内也可以传值，类型也要求是bytes类型
        m.update(item.encode('utf-8')) #
        return m.hexdigest()
    def creat_leaf_node(self,artical):    #artical 为要存储的数据的列表，用于构造默克尔树叶子节点
        nodes=[]
        for i in range(len(artical)):     #构造叶子节点
            text=artical[i]
            node=Tree_node()
            node.data=text
            node.hash=self.get_hash(text)   #后续可添加自然段对signal赋值
            node.signal=i
            nodes.append(node)
        root=self.creat_tree(nodes)     #根据叶子节点构造上方节点
        self.root=root
        return root
    def creat_tree(self,nodes):
        if(len(nodes)==1):
            root=nodes[0]
            return root
        else:
            temp_store_nodes=[]
            while(len(nodes)>1):           #两个节点向上构造
                left=nodes[0]
                right=nodes[1]
                nodes.pop(1)
                nodes.pop(0)
                node=Tree_node()
                node.hash=left.hash+right.hash
                node.lchild=left
                node.rchild=right
                left.parent=node
                right.parent=node
                temp_store_nodes.append(node)
            if(len(nodes)==1):   #一个节点向上构造
                left = nodes[0]
                nodes = nodes.pop(0)
                node = Tree_node()
                node.hash = left.hash
                node.lchild = left
                left.parent = node
                temp_store_nodes.append(node)
            root=self.creat_tree(temp_store_nodes)    #递归调用分层构造
        return root

    def test_change(self,store_node,artical_node):
        if(store_node.hash==artical_node.hash):     #哈希值相等则该处的子树均正确不用检查
            return
        else:
            if(store_node.lchild==None and store_node.rchild==None):   #若为叶子节点则是被篡改处，记录位置
                self.change_location.append(store_node.signal)
            if(store_node.lchild!=None):         #检测左子树
                self.test_change(store_node.lchild,artical_node.lchild)
            if(store_node.rchild!=None):      #检测右子树
                self.test_change(store_node.rchild,artical_node.rchild)
    def is_change(self,artical):
        my_tree=Tree()
        artical_root = my_tree.creat_leaf_node(artical)  # 篡改数据的默克尔树
        self.test_change(self.root,artical_root)
        return self.change_location

tree=Tree()
list=['我',"喜","欢","你","啊","啊"]              #模拟原始数据
artical_list=['我',"喜","欢","我","啊","啊"]    #模拟数据被篡改
root=tree.creat_leaf_node(list)                #原始数据的默克尔树
print(tree.is_change(artical_list))             #打印出被篡改处
