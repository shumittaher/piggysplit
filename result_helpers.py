from babel.numbers import format_decimal

def format_fixer(amount):
    fixed_amount =  format_decimal(amount, format='#,##0.##;(#)', locale='en')
    if amount == 0:
        fixed_amount = "Nil"
    return fixed_amount



def format_fix_table(table):
    lines = []
    for line in table:
        newline = line.copy()
        for item in newline.items():
            if type(item[1]) in (int, float, complex):
                newline[item[0]] = format_fixer(item[1])
        lines.append(newline)
    return lines

def object_to_row(obj, vendor = -1):
    return {
                "party" : obj.party, 
                "receivable_amount": obj.receivable_amount, 
                "received_amount": obj.received_amount, 
                "payable_amounts":obj.payable_amounts, 
                "paid_amounts": obj.paid_amounts, 
                "outstanding_amount":obj.calculate_outstanding() * (vendor * -1)
            }

class outstandings_row:
    def __init__(self, party, receivable_amount, payable_amounts, received_amount, paid_amounts):
        self.party= party
        self.receivable_amount = receivable_amount
        self.received_amount = received_amount
        self.payable_amounts = payable_amounts
        self.paid_amounts = paid_amounts

    def calculate_outstanding(self):
        return (self.payable_amounts - self.paid_amounts + self.received_amount - self.receivable_amount)

