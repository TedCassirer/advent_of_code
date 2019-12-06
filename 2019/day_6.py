class Node:
    def __init__(self, name):
        self.kids = set()
        self.name = name

    def __repr__(self):
        return self.name
        
class DefaultTree(dict):
    def __missing__(self, name):
        self[name] = Node(name)
        return self[name]

def create_tree(node_name_pairs):
    tree = DefaultTree()
    for daddy_name, babby_name in node_name_pairs:
        daddy, babby = tree[daddy_name], tree[babby_name]
        daddy.kids.add(babby)

    return tree['COM']

def count_kid_relations(daddy, depth=1):
    relations = len(daddy.kids) * depth
    relations += sum(count_kid_relations(kid, depth+1) for kid in daddy.kids)
    return relations

def find_path_to_node(grand_dad, target):
    def _find_path(dad):
        if dad.name == target:
            return set()
        for kid in dad.kids:
            path = _find_path(kid)
            if path != None:
                path.add(dad.name)
                return path
    return _find_path(grand_dad)

def get_input():
    with open('2019/input/day_6') as file:
        yield from (s.strip().split(')') for s in file)

def part1():
    node_name_pairs = get_input()
    grand_daddy = create_tree(node_name_pairs)
    return count_kid_relations(grand_daddy)

def part2():
    node_name_pairs = get_input()
    grand_daddy = create_tree(node_name_pairs)
    you_path = find_path_to_node(grand_daddy, "YOU")
    santa_path = find_path_to_node(grand_daddy, "SAN")
    return len(you_path ^ santa_path)

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())