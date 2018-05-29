from random import shuffle


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(variable, assignment):
            if self.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                del assignment[variable]

        return None

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue
                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_australia_csp():
    argentina, bolivia, brasil, chile, colombia, costaRica, ecuador, guyana, guyane,  panama, paraguay, peru, suriname, uruguay, venezuela = 'Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Guyana', 'Guyane', 'Panama', 'Paraguay', 'Peru', 'Suriname', 'Uruquay', 'Venezuela'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [argentina, bolivia, brasil, chile, colombia, costaRica, ecuador,
                 guyana, guyane,  panama, paraguay, peru, suriname, uruguay, venezuela]

    domains = {}
    for country in variables:
        domains[country] = values[:]

    neighbours = {
        argentina: [chile, bolivia, brasil, paraguay, uruguay],
        bolivia: [argentina, brasil, chile, paraguay, peru],
        brasil: [argentina, bolivia, colombia, guyane, guyana, venezuela, peru, paraguay, uruguay],
        chile: [bolivia, argentina, peru],
        costaRica: [panama],
        colombia: [brasil, ecuador, panama, peru, venezuela],
        ecuador: [colombia, peru],
        guyana: [brasil, suriname, venezuela],
        guyane: [brasil, suriname],
        panama: [costaRica, colombia],
        peru: [brasil, bolivia, chile, colombia, ecuador],
        paraguay: [argentina, bolivia, brasil],
        suriname: [brasil, guyana, guyane],
        uruguay: [argentina, brasil],
        venezuela: [brasil, colombia, guyane]

    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {}

    for contraint in variables:
        constraints[contraint] = constraint_function

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    australia = create_australia_csp()
    result = australia.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
