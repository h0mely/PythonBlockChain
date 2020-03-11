class Tree_node:
    def __init__(self):
        self.data=None    #用于存储具体数据内容
        self.hash=None   #用于存储该节点哈希值
        self.lchild=None   #表示结点左儿子
        self.rchild=None   #结点右儿子
        self.parent=None
        self.signal=None  #用来表示所在自然段的关键词