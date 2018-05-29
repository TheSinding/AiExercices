class Node:
    def __init__(self, state, hFunction, cost, parent=None):
        self.state = state
        self.hFunction = hFunction
        self.cost = cost
        self.parentNode = parent

    def path(self):
        currentNode = self
        path = [self]
        while currentNode.parentNode:
            currentNode = currentNode.parentNode
            path.append(currentNode)
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State ' + str(self.state) + ' - H Func ' + str(self.hFunction) + ' - Cost ' + str(self.cost)


def treeSearch():
    currentNode = Node(INITIAL_STATE, INITIAL_HEURISTIC_FUNCTION, 0)
    for _ in range(0, 21):
        for goal in goals:
            if currentNode.state is goal:
                return currentNode.path()
        nodes = expand(currentNode)

        if not nodes:
            currentNode = currentNode.parentNode
        else:
            count = len(nodes)
            for i in range(0, count - 1):
                if i is 0:
                    currentNode = nodes[0]
                else:
                    currentNode = compareNodes(nodes[i-1], nodes[i])

    return currentNode.path()


def expand(node):
    successors = []
    nodes = successor_fn(node.state)
    for _node in nodes:
        s = Node(_node[0], _node[1], _node[2], node)
        successors = INSERT(s, successors)
    return successors


def INSERT(node, queue):
    return INSERT_ALL([node], queue)


def INSERT_ALL(list, queue):
    # For depth first add the list to queue
    # queue = list + queue
    queue.extend(list)
    return queue


def REMOVE_FIRST(queue):
    return queue.pop(0)


def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]


def compareNodes(nodeA, nodeB):
    if (nodeA.cost + nodeA.hFunction * 1000000000000) < (nodeB.cost + nodeB.hFunction * 1000000000000):
        return nodeA
    else:
        return nodeB


INITIAL_STATE = 'A'
INITIAL_HEURISTIC_FUNCTION = 6
goals = ['K', 'L']
STATE_SPACE = {'A': [['B', 5, 1], ['C', 5, 2], ['D', 2, 4]],
               'B': [['F', 5, 5], ['E', 4, 4]],
               'C': [['E', 4, 1]],
               'D': [['H', 2, 1], ['I', 2, 4], ['J', 1, 2]],
               'E': [['G', 4, 2], ['H', 2, 3]],
               'F': [['G', 4, 1]],
               'G': [['K', 0, 6]],
               'H': [['K', 0, 6], ['L', 0, 5]],
               'I': [['L', 0, 3]],
               'J': []
               }


def run():
    path = treeSearch()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
