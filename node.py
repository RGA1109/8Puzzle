import collections

def node_swap_positon(passed_in_array, g_value, h_value):
    # takes in the current 8 puzzle layout, the depth of the node as g_value, and the heristic cost of the nodes
    # then returns a array of children nodes that could be picked from the passed_in_array layout
    children_nodes = []

    swapping_array = passed_in_array.copy()
    zero_index = passed_in_array.index(0)

    corner_index_dic = {0: ['1', '3'], 2: ['5', '1'], 6: ['3', '7'], 8: ['7', '5']}
    side_index_dic = {1: ['0', '4', '2'], 3: ['6', '4', '0'], 5: ['8', '4', '2'], 7: ['6', '4', '8']}
    middle_index_dic = {4: ['3', '1', '5', '7']}

    # section of code swaps the location of zero with the surrounding nodes making children nodes that is then returns
    if zero_index in corner_index_dic:
        # right then left
        for values in corner_index_dic[zero_index]:
            temp_node = swapping_array[zero_index]
            swapping_array[zero_index] = passed_in_array[int(values)]
            swapping_array[int(values)] = temp_node

            children_nodes.append(
                Node(passed_in_array, node_key(swapping_array), g_value + 1, (node_h_value(swapping_array)),
                     (g_value + 1 + node_h_value(swapping_array)), False, None))
            swapping_array = passed_in_array.copy()

        return children_nodes

    elif zero_index in side_index_dic:
        # right then left
        for values in side_index_dic[zero_index]:
            temp_node = swapping_array[zero_index]
            swapping_array[zero_index] = passed_in_array[int(values)]
            swapping_array[int(values)] = temp_node

            children_nodes.append(
                Node(passed_in_array, node_key(swapping_array), g_value + 1, (node_h_value(swapping_array)),
                     (g_value + 1 + node_h_value(swapping_array)), False, None))
            swapping_array = passed_in_array.copy()

        return children_nodes

    else:
        for values in middle_index_dic[zero_index]:
            temp_node = swapping_array[zero_index]
            swapping_array[zero_index] = passed_in_array[int(values)]
            swapping_array[int(values)] = temp_node

            children_nodes.append(
                Node(passed_in_array, node_key(swapping_array), g_value + 1, (node_h_value(swapping_array)),
                     (g_value + 1 + node_h_value(swapping_array)), False, None))
            swapping_array = passed_in_array.copy()
        return children_nodes


def node_h_value(array):
    # calculates the new value of the heristic cost and return it
    corrected_array = sorted(array)
    corrected_array.pop(0)
    corrected_array.append(0)
    h_counter = 0
    counter = 0

    for values in array:
        if (values == 0) and (corrected_array[counter] == 0):
            counter += 1
            pass

        elif values != corrected_array[counter]:
            h_counter += 1
            counter += 1
            
        else:
            counter += 1

    return (h_counter)


def node_key(array):
    # makes the parent key value out of the nodes 8 puzzle layout that are int numbers
    parent_key = ''

    for x in array:
        parent_key += str(x)

    return parent_key


class Node:
    def __init__(self, parent=None, child_id=None, g=0, h=0, f=0, used=False, children=None):
        self.parent = parent
        self.their_id = child_id
        self.g = g
        self.h = h
        self.f = f
        self.used = used
        self.children = []

    def get_parent(self):
        return self.parent

    def get_child_id(self):
        return self.their_id

    def get_g(self):
        return self.g

    def get_h(self):
        return self.h

    def get_f(self):
        return self.f

    def get_used(self):
        return self.used

    def get_children(self):
        return self.children

    def set_parent(self, parent_key):
        self.parent = parent_key

    def set_child_id(self, child_id):
        self.their_id = child_id

    def set_g(self, new_g):
        self.g = new_g

    def set_h(self, new_h):
        self.h = new_h

    def set_h(self, new_f):
        self.f = new_f

    def set_used(self, new_used):
        self.used = new_used

    def set_child(self, children):
        self.children = children

    def get_children_info(self):
        for x in self.children:
            return x.get_children()


def next_node(children_array, sorting_array, node_queue):
    last_child = None
    position = 0

    for child in children_array:
        for node in node_queue:
            if (node_key(sorting_array) != child.get_child_id()) and (node.get_child_id() != child.get_child_id()):

                if (last_child == None):
                    last_child = child.get_h()
                    position = children_array.index(child)

                elif (children_array[-1].get_h() < last_child):
                    last_child = child.get_h()
                    position = children_array.index(child)
                    
    return children_array[position]


def int_array(array):
    changed = []
    for x in array:
        changed.append(int(x))

    return changed


running = 'True'
while running == 'True':
    # This loop is to check all the imported puzzles to see if that are solvable or unsolvable
    # defined dictionaries
    a_star_tree = {}
    solvable = {}
    unsolvable = {}
    # defined arrays
    check_array = []
    puzzle = []
    solv = []
    unsolv = []
    # defined counters
    counter = 0
    odd_even_counter = 0
    puzzle_counter = 0
    solv_counter = 0
    unsolv_counter = 0

    counter_array = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    open_file = open("data.txt", "r")
    if open_file.mode == "r":
        contents = open_file.readlines()
        lines = [line.replace(' ', '').replace('\n', '') for line in contents]
        for x in lines:
            if x != '':
                puzzle.extend(x)
                puzzle_counter += 1
                if puzzle_counter == 3:
                    solv.append(puzzle)
                    puzzle = []
                    puzzle_counter = 0

        for array in solv:
            countered = 0
            for value in array:
                counter = array.index(value)
                add_up = 0
                if counter != 0:
                    while counter != 0:
                        counter -= 1
                        if value < array[counter]:
                            add_up += 1

            if add_up % 2 == 0:
                solvable[solv_counter] = array
                solv_counter += 1

            else:
                unsolvable[unsolv_counter] = array
                unsolv_counter += 1

            add_up = 0
            countered = 0

    open_file.close()
    running = False
print(solvable)

for key in solvable:
##    sorting_array = solvable[key]
##    sorting_array = [2,3,6,1,4,8,7,5,0]
    sorting_array = [6,0,2,3,4,7,1,5,8]
##    sorting_array = [3,6,1,4,8,5,7,2,0]
##    sorting_array = [3,1,4,6,0,7,5,2,8]
##    sorting_array = [5,2,4,8,3,7,1,6,0]
    correct = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    children_nodes = []
    node_queue = collections.deque()
    node_queue_parent_id = []
    node_queue.append(
        Node(None, node_key(sorting_array), 0, node_h_value(sorting_array), node_h_value(sorting_array), True, None))
    node_queue_parent_id.append(node_queue[0].get_child_id())
    
    while node_queue[-1].get_parent() != correct:
        children = node_swap_positon(int_array(sorting_array), node_queue[-1].get_g(), node_queue[-1].get_h())
        node_queue[-1].set_child(children)

        if len(node_queue) == 1:
            next_parent = next_node(children, node_key(node_queue[-1].get_child_id()), node_queue)
        else:
            next_parent = next_node(children, node_key(node_queue[-1].get_parent()), node_queue)

        if next_parent.get_g() > 1:
            for nodes in node_queue:
                nodes_children = nodes.get_children()
                for child in nodes_children:

                    if next_parent.get_f() > child.get_f():
                        if (child.get_used() == False) and (child.get_child_id() in node_queue_parent_id):
                            pass
                        elif (child.get_used() == False):
                            next_parent = child

        next_parent.set_used(True)

        node_queue.append(next_parent)
        node_queue_parent_id.append(next_parent.get_child_id())

        sting = next_parent.get_child_id()

        sorting_array = (int_array(next_parent.get_child_id()))

print('here')
        
parent = node_key(node_queue[-1].get_parent())      
while parent != None:
    for node in node_queue:
        if node.get_child_id() == parent:
            if node.get_parent() == None:
                parent = None
            else:
                parent = node_key(node.get_parent())
            print('parent_id:', node.get_parent())
            print('child_id:', node.get_child_id())
            print('g_value:', node.get_g())
            print('h_value:', node.get_h())
            print('f_value:', node.get_f())
