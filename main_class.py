import json

transition_table = set(["NamedValue", "BinaryOp", "ContinuousAssign", "ProceduralBlock", "ExpressionStatement"])  # 待师姐修改
AddString = "AddValue"


#   根据字符串名称赋值  #  待师姐修改
#   trans函数参数说明
#   kind_value 指的是一组属性里面的kind的值(如"Conversion")，若没有该属性为 ""
#   name_value 指的是一组属性里面的name的值(如"root")，若没有该属性为 ""
#   type_value 指的是一组属性里面的kind的值(如"logic[3:0]"，该处需自行处理字符串拿到权重)，若没有该属性为 ""
#   类型均是字符串
#   返回值会返回到该组属性的AddValue当中
def trans(kind_value, name_value, type_value):
    for i in transition_table:
        if i == kind_value:
            return 66
    return 0


class Node:
    def __init__(self, name: str = "", instance_name: str = "", value: int = 0, rank: int = -1, parent=None, children=None, others=None):
        self.name = name
        self.instance_name = instance_name
        self.value = value
        self.rank = rank
        self.parent = parent
        self.children = children
        self.others = others

    def show(self):
        print('%-35s' % 'Name is: {}'.format(self.name), end='')
        print('%-50s' % 'instance_name is: {}'.format(self.instance_name), end='')
        print('%-20s' % 'value is: {}'.format(self.value), end='')
        print('%-20s' % 'rank is: {}'.format(self.rank), end='')
        print('%-35s' % 'parent is: {}'.format(self.parent), end='')
        print('%-35s' % 'children is: {}'.format(self.children), end='')
        print('%-35s' % 'others is: {}'.format(self.others), end='')
        print()

    def getRankAndValue(self):
        return self.rank, self.value



#    存储Node结点的列表
nodelist = []
all_list = []

#   11.30 20:15
def travel_to_list(parent, data, str, rank_count):

    #   是个字典类型则输出
    name_value = ""
    AddString_value = 0
    kind_value = ""
    if isinstance(data, dict):
        for key in data.keys():
            if key == "name":
                name_value = data[key]
            elif key == AddString:
                AddString_value = data[key]
            elif key == "kind":
                kind_value = data[key]
                if kind_value == "Instance":
                    rank_count += 1
            #print("  " * rank_count, "In ", str, "; key:", key, "; value:", data[key], sep='')
            if isinstance(data[key], list) or isinstance(data[key], dict):
                travel_to_list(name_value, data[key], key, rank_count)
        Anode = Node(name_value, kind_value, AddString_value, rank_count, parent)
        all_list.append(Anode)
        if kind_value == "Instance":
            Anode = Node(name_value, data["body"]["name"], AddString_value, rank_count, parent)
            nodelist.append(Anode)


    #   是列表类型则遍历调用输出
    elif isinstance(data, list):
        #       print("             is list")
        for i in data:
            #   列表传上一层的parent
            travel_to_list(parent, i, str, rank_count)
    #   print(" ")


#   遍历
def travel(data, str, blank_count):
    #   是个字典类型则输出
    blank_count += 1
    if isinstance(data, dict):
        #   print("***************In ", str, "***************")
        #       print("             is dict")
        for key in data.keys():
            print("  " * blank_count, "In ", str, "; key:", key, "; value:", data[key], sep='')
            if isinstance(data[key], list) or isinstance(data[key], dict):
                travel(data[key], key, blank_count)

    #   是列表类型则遍历调用输出
    elif isinstance(data, list):
        #       print("             is list")
        for i in data:
            travel(i, str, blank_count)
    #   print(" ")


#   增加AddString属性
def travel_to_add(data, str):
    #   是个字典类型
    if isinstance(data, dict):
        for key in data.keys():
            #   print("key:", key, "; value:", json_in[key])
            if isinstance(data[key], list) or isinstance(data[key], dict):
                travel_to_change(data[key], key)
        #   AddString添加到最后面
        data.update({AddString: 0})
    #   是列表类型则遍历调用输出
    elif isinstance(data, list):
        #       print("             is list")
        for i in data:
            travel_to_add(i, str)


#   修改AddString属性
def travel_to_change(data, str):
    #   是个字典类型
    kind_value = ""
    sum_value = 0
    type_value = ""
    name_value = ""
    if isinstance(data, dict):
        #   遍历 一次循环遍历是我们认为的一次结点
        for key in data.keys():
            if key == "kind":
                kind_value = data[key]
            elif key == "type":
                type_value = data[key]
            elif key == "name":
                name_value = data[key]
            if key == AddString and kind_value != "":
                sum_value += trans(kind_value, name_value, type_value)
                kind_value = ""
            if isinstance(data[key], list) or isinstance(data[key], dict):
                sum_value += travel_to_change(data[key], key)
        #   遍历完孩子结点后更新AddString权重
        data[AddString] = sum_value
    #   是列表类型则遍历调用输出
    elif isinstance(data, list):
        #       print("             is list")
        for i in data:
            sum_value += travel_to_change(i, str)
    return sum_value


if __name__ == '__main__':
    with open('fortest1.json', 'r', encoding='utf-8') as f:
        json_in = json.load(f)
    #   print(data)

    #travel(json_in, "root", -1)
    travel_to_add(json_in, "root")
    all_value = travel_to_change(json_in, "root")
    print("############################")
    #travel(json_in, "root", -1)
    #print("总权重", all_value)
    #with open("Change.json", 'w', encoding='utf-8') as f1:
    #    f1.write(json.dumps(json_in, indent=4, ensure_ascii=False))
    travel_to_list("root_parent", json_in, "root", -1)
    for i in nodelist:
        i.show()

    level_value = []
    #   添加每一层存储权重的数组
    for index in range(1,len(nodelist)):
        level_value.append(0)

    for j in all_list:
        r, v = j.getRankAndValue()
        if r >= 0:
            level_value[r] = level_value[r] + v

    for j in all_list:
        j.show()

    for j in range(0,len(level_value)):
        print(j, level_value[j])