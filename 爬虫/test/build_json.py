#coding=utf-8
import json
class Node:
    def __init__(self, _name):
        self.name = _name
        self.val = 0
        self.childs = list()

    """
    题目：从当前节点开始，输出从当前节点开始的树结构转换成json格式后返回
    """
    def node2json(self):
        json_dict = {}
        json_dict["val"] = self.val
        json_dict["childs"] = []
        json_dict["name"] = self.name
        if len(self.childs) == 0:
            return json_dict
        for i in self.childs:
            json_dict["childs"].append(i.node2json())
        return json_dict

    """
    题目：更新当前node与下级node的val，val的值等于该node下一共有多少个子节点
    """
    def count_val(self):
        self.val = 0
        s_tree = len(self.childs)

        if len(self.childs) == 0:
            return self.val
        for i in self.childs:
            self.val += i.count_val()
        self.val += s_tree
        return self.val


class Solve:
    def __init__(self, root_name):
        #初始化根节点
        self.root_node = Node(root_name)
        #边
        self.relations = list()
        #节点list
        self.node_list = list()
        self.node_list.append(self.root_node)

    """
    题目：通过输入的各条边关系，创建出树结构，并返回根节点
    如：机器学习,线性模型。则线性模型node是机器学习node的child
    """
    def build(self):
        for i in set(self.relations):
            list_nodename = {i.name: i for i in self.node_list}
            if i[0] in list_nodename:
                if i[1] in list_nodename:
                    list_nodename[i[0]].childs.append(list_nodename[i[1]])
                else:
                    node_1 = Node(i[1])
                    list_nodename[i[0]].childs.append(node_1)
                    self.node_list.append(node_1)
            else:
                if i[1] in list_nodename:
                    node_2 = Node(i[0])
                    node_2.childs.append(list_nodename[i[1]])
                    self.node_list.append(node_2)
                else:
                    f_node = Node(i[0])
                    s_node = Node(i[1])
                    f_node.childs.append(s_node)
                    self.node_list.append(f_node)
                    self.node_list.append(s_node)
        return self.root_node

    def run(self, relations):
        self.relations = relations
        self.build()
        self.root_node.count_val()
        with open("ans.json", "w") as f:
            json.dump(self.root_node.node2json(), f, indent=4)
        print(json.dumps(self.root_node.node2json(), ensure_ascii=False, indent=4))

if __name__ == '__main__':
    #根节点名为机器学习
    ans = Solve("机器学习")
    #有如下的边
    relations = [('机器学习', '线性模型'), ('机器学习', '神经网络'), ('神经网络', '神经元模型'), ('机器学习', '强化学习'), ('线性回归', '最小二乘法'), ('线性模型', '线性回归'), ('神经网络', '神经元模型'), ('神经元模型', '激活函数'), ('多层网络', '感知机'), ('多层网络', '连接权'), ('神经网络', '多层网络'), ('强化学习', '有模型学习'), ('强化学习', '免模型学习'), ('强化学习', '模仿学习'), ('有模型学习', '策略评估'), ('有模型学习', '策略改进'), ('免模型学习', '蒙特卡洛方法'), ('免模型学习', '时序差分学习'), ('模仿学习', '直接模仿学习'), ('模仿学习', '逆强化学习')]
    #完成题目内要求的代码
    ans.run(relations)
