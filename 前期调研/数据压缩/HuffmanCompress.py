class node(object):    #创建霍夫曼树结点类
    def __init__(self):
        self.name = None
        self.weight = None
        self.leftchild = None
        self.rightchild = None
        self.parent = None


class code_node(object):     #创建编码结点类
    def __init__(self, code, name, weight):
        self.code = code
        self.name = name
        self.weight = weight

# 哈夫曼类: HuffmanTree,
# 类内主要成员有：
# text: 本次压缩处理的文本，多行字符串，由外部text变量传过来。
# code_dict: 编码字典，key是字符，value是编码。
# final_01data: 编码后的文章列表， 每段的压缩码(01字符串)依次存放在列表里。
# final_byte: 压缩码转换成字节数据的文章列表，每段的字节数据依次存放在列表里
# decode_01data： 字节数据转换成的待解码的01串列表，与原压缩码相同，每段的待解码01串依次存放在列表里
# 类内主要方法有：
# buildtree: 建哈夫曼树
# make_code: 对字符编码（不含"\n"）
# compress & print_compress: 压缩文本，保存压缩码（01串）到final_01data
# data_to_byte: 压缩码经处理转换成字节数据，保存到final_byte
# byte_to_data: 字节数据转换成去处理的待解压码，保存到decode_01data
# data_to_text: 解压01串，返回分段后的文章列表

class HuffmanTree(object):    #哈夫曼树类
    def __init__(self):
        self.root = node()

    def buildtree(self, name_set, weight_set):    #创建哈夫曼树
        self.nodes = []                   #以降序存储新结点
        while len(name_set) > 0:
            max_weight = max(weight_set)
            max_pos = weight_set.index(max_weight)
            max_name = name_set[max_pos]
            newnode = node()
            newnode.name = max_name
            newnode.weight = int(max_weight)   #权值为整型
            self.nodes.append(newnode)
            name_set.remove(max_name)
            weight_set.remove(max_weight)    #创建新结点，填入name和weight属性，且按降序入列
        self.nodes_copy = self.nodes[:]
        #备份self.nodes，用于自底向上编码，不能使用self.nodes_copy = self.nodes，这会导致两者始终同步
        while len(self.nodes) > 2:
            l = self.nodes.pop()
            r = self.nodes.pop()
            newnode = node()
            newnode.weight = l.weight + r.weight
            newnode.leftchild = l
            newnode.rightchild = r
            l.parent = newnode
            r.parent = newnode
            self.insert(newnode)    #将新结点根据weight大小插入self.nodes
        left = self.nodes.pop()
        right = self.nodes.pop()
        self.root.weight = left.weight + right.weight
        self.root.leftchild = left
        self.root.rightchild = right
        left.parent = self.root
        right.parent = self.root   #列表中最后两个结点连接Haffuman树的根节点

    def insert(self, newnode):
        for i in range(len(self.nodes)):
            if self.nodes[i].weight < newnode.weight:
                self.nodes.insert(i, newnode)
                return
        self.nodes.append(newnode)

    def make_code(self):  # 对不同字符编码，编码字典存在code_dict
        codes = []
        while len(self.nodes_copy) > 0:
            code = ''
            precode_node = self.nodes_copy.pop()
            t = precode_node
            while t.parent != self.root:  # 自底向上编码
                p = t.parent
                if t == p.leftchild:
                    code = '0' + code
                elif t == p.rightchild:
                    code = '1' + code
                t = t.parent
            if t == self.root.leftchild:
                code = '0' + code
            elif t == self.root.rightchild:
                code = '1' + code
            codes.append(code_node(code, precode_node.name, precode_node.weight))  # 编码结点存入编码库self.nodes
        self.code_dict = {}
        for i in range(len(codes)):
            self.code_dict[codes[i].name] = codes[i].code
        print("编码表：")
        print(self.code_dict)

    def data_preprocessing(self, text):  # 文本预处理，统计文本内字符及频率（不含"\n"）
        self.text = text
        self.data = list(self.text)  # 数据转列表，单个字符存储
        dict = {}
        for i in set(self.data):
            dict[i] = self.data.count(i)
        dict.pop('\n')
        self.base_name = []
        self.base_num = []
        for i in dict.keys():
            self.base_name.append(i)
            self.base_num.append(dict[i])

    def data_make_code(self):  # 制作编码并输出编码表
        self.buildtree(self.base_name, self.base_num)
        self.make_code()

    def compress(self):  # 压缩
        self.compress_data_part = []
        compress_data = []
        self.text_part = self.text.split('\n')
        self.data_part = []
        for i in range(len(self.text_part)):
            self.data_part.append(list(self.text_part[i]))
        for i in range(len(self.data_part)):
            for j in range(len(self.data_part[i])):
                compress_data.append(self.code_dict[self.data_part[i][j]])
            cpd_copy = compress_data[:]
            self.compress_data_part.append(cpd_copy)
            compress_data.clear()

    def print_compress(self):  # 输出压缩码，分段存入final_01data
        print("分段后压缩码为：")
        self.final_01data = []
        for i in range(len(self.compress_data_part)):
            p = ''.join(self.compress_data_part[i])
            self.final_01data.append(p)
        print(self.final_01data)

    def pad_encoded_text(self, encoded_text):  # 对压缩码进行预处理，尾部补齐8的倍数，头部加信息头表示尾部补了多少0
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):  # 01串转byte
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def data_to_byte(self):  # 生成压缩完成且转码的分段的字节数据，存入final_byte列表
        self.final_byte = []
        for i in range(len(self.final_01data)):
            b = self.get_byte_array(self.pad_encoded_text(self.final_01data[i]))
            self.final_byte.append(b)

    def byte_to_data(self):  # 转码的字节数据转换成待解码的01串，并且去掉预处理补加的字符串，分段存入decode_01data
        self.decode_01data = []
        for i in range(len(self.final_byte)):
            bb0 = self.final_byte[i]
            num = bb0[0]
            bb = bb0[1:]
            str0 = str(bin(int(bb.hex(), 16))[2:])
            if len(str0) % 8 != 0:
                extra0 = 8 - len(str0) % 8
                for j in range(extra0):
                    str0 = '0' + str0
            str1 = str0[0: len(str0) - num]
            self.decode_01data.append(str1)
        print(self.decode_01data)

    def cmp_ok(self, a, b):   #从头比较，判断b是否为a的子字符串
        l = len(b)
        k = 0
        if len(a) < len(b):
            return False
        while k < l:
            if a[k] == b[k]:
                k += 1
            else:
                return False
        return True

    def data_to_text(self):  # 解压，01串转换成文本，分段存入result列表并返回
        result = []
        for i in range(len(self.decode_01data)):
            result_part = ""
            uncompress_code = self.decode_01data[i]
            while len(uncompress_code) > 0:
                for j in self.code_dict:
                    if self.cmp_ok(uncompress_code, self.code_dict[j]) == True:
                        h = len(self.code_dict[j])
                        uncompress_code = uncompress_code[h:]
                        result_part += j
            result.append(result_part)
        return result


text = """The Tokyo 2020 Olympics torch lighting ceremony in ancient Olympia will be the first in more than 35 years to be held without spectators after organizers on Monday introduced tighter measures to protect against the coronavirus.
Greece's Olympic Committee said spectators would be excluded from both the dress rehearsal at the ancient site on Wednesday and the widely broadcast ceremony on Thursday.
This is the first time since the 1984 Los Angeles Olympics that the ceremony will be held without any spectators lounging on the grassy slopes of the ancient stadium in the tiny Peloponesian hamlet. The ceremony — held both for summer and winter Games — usually attracts several thousand spectators, including Greeks and foreign visitors.
"The lighting ceremony of the Olympic flame will be done without the presence of spectators and only 100 invited and accredited guests," the Greek Olympic Committee said in a statement.
"The dress rehearsal on March 11 will be closed to spectators and media."
The Olympic torch will be lit in Olympia at a scaled-down ceremony on March 12 before a seven-day relay that culminates with a handover ceremony in Greece on March 19.
The number of people inside the ancient stadium will also be reduced with only a few dozen representatives of the Tokyo Games from a group of about 150 allowed access to the ceremony.
Organizers will also shut the press center following the ceremony to avoid the gathering of many people in an indoor area and will stage Wednesday's dress rehearsal without the presence of media. Tokyo had already stopped 340 children from attending.
Greece on Sunday announced a two-week ban on sporting events with spectators and on school field trips, as its number of coronavirus cases rose by seven to 73. The prefecture of Ilia, of which Olympia is part, is among areas of the country hardest hit by the coronavirus.
The Mayor of Olympia has written to International Olympic Committee President Thomas Bach, proposing the postponement of the ceremony until May.
"The danger of staging the torch lighting with only a handful of spectators, limited number of officials and delegations, and under a cloud of fear and concern will damage the greatness and prestige of this event," Olympia mayor Giorgos Georgiopoulos said in his letter."""


if __name__ == '__main__':

    htree = HuffmanTree()  #创建Huffman空树
    #压缩
    htree.data_preprocessing(text)   #输入序列信息并预处理
    htree.data_make_code()   #制作编码并输出编码表
    htree.compress()    #压缩
    htree.print_compress()   #输出分好段的压缩码，按顺序存在列表里
    htree.data_to_byte()     #压缩码分段转换成字节数据
    #解压
    htree.byte_to_data()    #字节数据分段转换成待解压码
    text_part = htree.data_to_text()    #保存经分段解压后的文章列表到text_part
    #输出解压后的文本
    final_text = ""
    for i in range(len(text_part)):
        final_text += text_part[i]
        final_text += "\n"
    print(final_text)
    #分段验证解压后的文章与原文是否一致
    origin_text = text.split("\n")
    for i in range(len(origin_text)):
        if origin_text[i] == text_part[i]:
            print("same")
        else:
            print("no")

