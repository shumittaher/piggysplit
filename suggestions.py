


def get_suggestions(current_state):

    largest_party = find_edge(current_state, True)
    smallest_party =  find_edge(current_state, False)

    return

def find_edge(array, finding_large):

    def condition(x,y, finding_large):
        if finding_large:
            return x > y
        else: 
            return x < y 

    largest = {}
    for item in array:
        if not "outstanding_amount" in largest:
            largest = item
        if condition(item["outstanding_amount"], largest["outstanding_amount"], finding_large):
            largest = item
    return largest