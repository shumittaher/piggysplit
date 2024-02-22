


def get_suggestions(current_state):

    transactions = []
    record_transactions(current_state, transactions)

    return transactions

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

def record_transactions(current_state, transactions):
    
    largest_party = find_edge(current_state, True)
    smallest_party =  find_edge(current_state, False)

    if largest_party["outstanding_amount"] == smallest_party["outstanding_amount"]:
        return transactions
    
    if largest_party["outstanding_amount"] > smallest_party["outstanding_amount"] * -1 :
        amount = smallest_party["outstanding_amount"] * -1
    else:
        amount = largest_party["outstanding_amount"] 
    
    transaction = {"payer": largest_party["party"], "payer_name": largest_party["partyname"], "payee": smallest_party["party"],"payee_name": smallest_party["partyname"], "amount": amount}
    current_state = update_current_state(current_state, transaction)
    transactions.append(transaction)
    
    record_transactions(current_state, transactions)

def update_current_state(current_state, transaction):

    for item in current_state:
        if item["party"] == transaction["payer"]:
            print(item["party"])
            item["outstanding_amount"] = item["outstanding_amount"] - transaction["amount"]
        elif item["party"] == transaction["payee"]:
            print(item["party"])
            item["outstanding_amount"] = item["outstanding_amount"] + transaction["amount"]
    for idx, item in enumerate(current_state):
        if item["outstanding_amount"] == 0:
            current_state.pop(idx)
    return current_state
