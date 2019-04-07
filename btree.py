class Node():
    def __init__(self, size, keys=None, pointers=None):
        self.size = size
        self.minimum = size // 2
        if keys:
            self.keys = keys
        else:
            self.keys = []
        if pointers:
            self.pointers = pointers
        else:
            self.pointers = []
    
    def __str__(self):
        return '[' + ','.join(map(str, self.keys)) + ']'

    def is_full(self):
        return len(self.keys) == self.size
    
    def split(self):
        mid = self.size // 2
        parent = self.keys[mid]
        left = Node(self.size, self.keys[:mid], self.pointers[:mid+1])
        right = Node(self.size, self.keys[mid+1:], self.pointers[mid+1:])
        root = Node(self.size, [parent], [left, right])
        return root

    def add(self, key):
        i = 0
        while i < len(self.keys):
            if self.keys[i] <= key:
                i += 1
            else:
                break
        self.keys.insert(i, key)
        while len(self.pointers) < len(self.keys) + 1:
            self.pointers.append(None)
    
    def delete(self, key):
        i = 0
        while i < len(self.keys):
            if self.keys[i] == key:
                break
            i += 1
        if i != len(self.keys):
            self.keys.pop(i)
            if self.pointers and self.pointers[0]:
                left, right = self.pointers[i], self.pointers[i+1]
                if i == 0:
                    right.combine(left, False)
                    self.pointers.pop(i)
                else:
                    left.combine(right)
                    self.pointers.pop(i+1)
            elif self.pointers:    
                self.pointers.pop(i)
    
    def combine(self, node, inverse=True):
        if inverse:
            self.keys = node.keys.extend(self.keys)
            self.pointers = node.pointers.extend(self.pointers)
        else:
            self.keys.extend(node.keys)
            self.pointers.extend(node.pointers)

class BTree():
    def __init__(self, order):
        self.order = order
        self.root = Node(order)
        self.depth = 1

    def __str__(self):
        queue = [self.root]
        res = []
        string = ''
        while queue:
            tmp = []
            while queue:
                node = queue.pop(0)
                res.append(str(node))
                tmp += [x for x in node.pointers if x]
            queue = tmp
            string += ','.join(res) + '\n'
            res = []
        return string

    def insert(self, key):
        path = self.insert_find(key)
        node = path.pop()
        node.add(key)
        if node.is_full():
            head = node.split()
            while path:
                head, split_flag = self.merge(path.pop(), head)
                if split_flag:
                    continue
                else:
                    return 
            self.root = head
            self.depth += 1

    def insert_find(self, key):
        path = [self.root]
        if self.depth == 1:
            return path
        else:
            cnt = 1
            node = self.root
            while cnt < self.depth:
                i = 0
                while i < len(node.keys):
                    if node.keys[i] > key:
                        break
                    else:
                        i += 1
                node = node.pointers[i]
                cnt += 1
                path.append(node)
        
        return path

    def delete(self, key):
        node, state, path = self.delete_find(key)
        if state == 'not_found':
            return
        elif state == 'leaf':
            if len(node.keys) > node.minimum:
                node.delete(key)
            else:
                parent = path[-2]
                bro = self.rich_brother(parent)
                if bro:
                    pass    
                else:
                    pass
            
        else:
            i = node.keys.index(key)
            child = node.pointers[i+1]
            if len(child.keys) > child.minimum:
                v = child.keys[0]
                child.delete(v)
                node.keys[i] = v

    def delete_find(self, key):
        cnt = 0
        node = self.root
        path = [node]
        while cnt < self.depth - 1:
            i = 0
            while i < len(node.keys):
                if node.keys[i] == key:
                    return node, 'middle', path
                elif node.keys[i] > key:
                    break
                i += 1
            node = node.pointers[i]
            path.append(node)
            cnt += 1
        i = 0
        while i < len(node.keys):
            if node.keys[i] == key:
                return node, 'leaf', path
            i += 1

        return None, 'not_found', path


    
    def merge(self, node1, node2):
        keys1 = node1.keys
        key2 = node2.keys[0]
        i = 0
        while i < len(keys1):
            if keys1[i] > key2:
                break
            else:
                i += 1
        node1.keys.insert(i, key2)
        node1.pointers[i] = node2.pointers[0]
        node1.pointers.insert(i+1, node2.pointers[1])
        if len(node1.keys) >= node1.size:
            return node1.split(), True
        else:
            return node1, False

        return node1, split_flag

if __name__ == '__main__':
    node1 = Node(3)
    node1.add(12)
    node1.add(1)
    node1.add(3)
    node1.add(46)
    t = BTree(5)
    t.insert('C')
    t.insert('N')
    t.insert('G')
    t.insert('A')
    t.insert('H')
    print(t)
    t.insert('E')
    t.insert('K')
    t.insert('Q')
    print(t)
    t.insert('M')
    print(t)
    t.insert('F')
    t.insert('W')
    t.insert('L')
    t.insert('T')
    print(t)
    t.insert('Z')
    print(t)
    t.insert('D')
    t.insert('P')
    t.insert('R')
    t.insert('X')
    t.insert('Y')
    print(t)
    t.insert('S')
    print(t)
    print('delete testing.....')
    t.delete('H')
    t.delete('T')
    print(t)
