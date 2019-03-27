class Graph():
    def __init__(self):
        self.nodes = set()
        self.edges = {}
    
    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, node1, node2):
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.edges.setdefault(node1, set()).add(node2)
        self.edges.setdefault(node2, set()).add(node1)

    def add_from_list(self, lst):
    	if not lst:
    		return
    	elif len(lst) == 1:
    		self.add_node(lst[0])
    	else:
	        for i in range(len(lst)-1):
	            self.add_edge(lst[i], lst[i+1])

    def get_connected_components(self):
        """Use DFS to get connected components
            Returns:
                list of list
        """
        unvisited = self.nodes
        res = []
        while unvisited:
            node = unvisited.pop()
            l = [node]
            candidates = self.edges.get(node, set())
            while candidates:
                node2 = candidates.pop()
                if node2 in unvisited:
                    l.append(node2)
                    unvisited.remove(node2)
                    candidates = candidates | self.edges.get(node2, set())
            res.append(l)

        return res

class CommonElements():
    def __init__(self):
        self.graph = Graph()
    
    def feed(self, data):
        for lst in data:
            self.graph.add_from_list(lst)

    def get_merged_list(self):
        return self.graph.get_connected_components()


if __name__ == '__main__':
    import pprint
    ce = CommonElements()
    X = [[1, 2, 3], [2, 3], [4, 5], [1, 6]]
    ce.feed(X)
    X2 = ce.get_merged_list()
    pprint.pprint(X2)

    X = [["a","b","d"],["e","h"],["c","b","d"],["g"],["d","e"]]
    ce = CommonElements()
    ce.feed(X)
    X2 = ce.get_merged_list()
    pprint.pprint(X2)
    
    X = [("4", "3"),("3", "8"), ("6", "5"),("9", "4"),("2", "1"),("8", "9"),("5", "0"),("7", "2"),("6", "1"),("1", "0"), ("6", "7")]
    ce = CommonElements()
    ce.feed(X)
    X2 = ce.get_merged_list()
    pprint.pprint(X2)
