class Node:
    def __init__(self, state, hFunction, parent=None):
        self.state = state
        self.hFunction = hFunction
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
        return 'State ' + str(self.state) + ' - H Func ' + str(self.hFunction)


def treeSearch():
    currentNode = Node(INITIAL_STATE, INITIAL_HEURISTIC_FUNCTION)
    for _ in range(0, 21):
        for goal in goals:
            if currentNode.state is goal:
                return currentNode.path()
        nodes = expand(currentNode)

        if not nodes:
            currentNode = currentNode.parentNode
        else:
            for node in nodes:
                if node.hFunction < currentNode.hFunction:
                    currentNode = node

    return currentNode.path()


def expand(node):
    successors = []
    nodes = successor_fn(node.state)
    for _node in nodes:
        s = Node(_node[0], _node[1], node)
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


INITIAL_STATE = 'A'
INITIAL_HEURISTIC_FUNCTION = 6
goals = ['K', 'L']
STATE_SPACE = {'A': [['B', 5], ['C', 5], ['D', 2]],
               'B': [['F', 5], ['E', 4]],
               'C': [['E', 4]],
               'D': [['H', 2], ['I', 2], ['J', 1]],
               'E': [['G', 4], ['H', 2]],
               'F': [['G', 4]],
               'G': [['K', 0]],
               'H': [['K', 0], ['L', 0]],
               'I': [['L', 0]],
               'J': []
               }


def run():
    path = treeSearch()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
