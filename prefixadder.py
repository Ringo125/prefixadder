import re

class Notation(object):
    def __init__(self):
        pass


class Prefix(object):
    def __init__(self, msb, lsb, r1_msb=-1, r1_lsb=-1):
        self.name = "%d_%d" % (msb, lsb)
        self.msb = msb
        self.lsb = lsb
        self.r0_msb = 0
        self.r0_lsb = 0
        self.r1_msb = r1_msb
        self.r1_lsb = r1_lsb
        self.related = ["", ""]
        if not (r1_lsb == -1 or r1_lsb == -1):
            self.parser_related(msb, r1_msb)

    def parser_related(self, msb, r1_msb):
        self.r0_msb = msb
        self.r0_lsb = r1_msb + 1
        self.related[0] = "%d_%d" % (self.r0_msb, self.r0_lsb)
        self.related[1] = "%d_%d" % (self.r1_msb, self.r1_lsb)


class PrefixMap(object):
    def __init__(self):
        self.import_file = ""
        self.nodes = []

    def set_file(self, file_path):
        self.import_file = file_path

    def node_check(self, line):
        if re.findall("^\d+_\d+\s*$", line):
            node = re.findall("^(\d+_\d+)\s*$", line)[0]
            self.nodes.append(node)
        elif re.findall("^\d+_\d+\s*\(\s*\d+_\d+\s*\)\s*$", line):
            node = re.findall("^(\d+_\d+)\s*\(\s*(\d+_\d+)\s*\)\s*$", line)[0]
            self.nodes.append("%s(%s)" % (node[0], node[1]))
        elif re.findall("^\s*$", line):
            # Drop empty line
            pass
        else:
            print("[Error  ] Incorrect node format:", line)
            exit()

    def read_file(self):
        if self.import_file == "":
            print("[Error  ] Please set the input file first.")
            exit()
        else:
            f = open(self.import_file, "r")
            for line in f:
                self.node_check(line.rstrip('\n'))
            f.close()

    @staticmethod
    def related_node(node):
        (target, related) = re.findall("(\S+_\S+)\((\S+_\S+)\)", node)[0]
        return target, related

    def add_zero(self, node):
        if re.findall("\S+\(\S+\)", node):
            (target, related) = self.related_node(node)
            (i, j) = re.findall("(\d+)_(\d+)", target)[0]
            out = "%02d_%02d(%s)" % (int(i), int(j), related)
        else:
            (i, j) = re.findall("(\d+)_(\d+)", node)[0]
            out = "%02d_%02d" % (int(i), int(j))
        return out

    def remove_zero(self, node):
        if re.findall("\S+\(\S+\)", node):
            (target, related) = self.related_node(node)
            (i, j) = re.findall("(\d+)_(\d+)", target)[0]
            out = "%d_%d(%s)" % (int(i), int(j), related)
        else:
            (i, j) = re.findall("(\d+)_(\d+)", node)[0]
            out = "%d_%d" % (int(i), int(j))
        return out

    def sort(self, lists):
        lists = [self.add_zero(x) for x in lists]
        lists.sort()
        lists = [self.remove_zero(x) for x in lists]
        return lists

    def reverse(self, lists):
        lists = [self.add_zero(x) for x in lists]
        lists.reverse()
        lists = [self.remove_zero(x) for x in lists]
        return lists

    def reorder(self):
        lists = self.sort(self.nodes)
        idx = 0
        tmp_list = []
        sublist = []
        for x in lists:
            check_idx = int(re.findall("^(\d+)_", x)[0][0])
            if not check_idx == idx:
                if not idx == 0:
                    tmp_list += self.reverse(sublist)
                idx = check_idx
                sublist: List[str] = [x]
            else:
                sublist.append(x)
        tmp_list += self.reverse(sublist)
        self.nodes = tmp_list

    def print_node(self):
        print(self.nodes)

    def parser_node(self, node):
        if re.findall("\S+\(\S+\)", node):
            (target, related) = self.related_node(node)
            (i, j) = re.findall("(\d+)_(\d+)", target)[0]
            (k, l) = re.findall("(\d+)_(\d+)", related)[0]
            return int(i), int(j), int(k), int(l)
        else:
            (i, j) = re.findall("(\d+)_(\d+)", node)[0]
            return int(i), int(j), -1, -1

    def parser(self):
        node_list = []
        for node in self.nodes:
            (msb, lsb, r1_msb, r1_lsb) = self.parser_node(node)
            p = Prefix(msb, lsb, r1_msb, r1_lsb)
            node_list.append(p)
        return node_list


if __name__ == "__main__":
    nm = PrefixMap()
    nm.set_file('C:/Users/Ringo/AppData/Roaming/JetBrains/PyCharmCE2020.1/scratches/scratch.txt')
    nm.read_file()
    nm.reorder()
    nm.print_node()

    print(len(nm.parser()))

    pass
