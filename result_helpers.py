from babel.numbers import format_decimal

def format_fixer(amount):
    fixed_amount =  format_decimal(amount, format='#,##0.##;(#)', locale='en')
    if amount == 0:
        fixed_amount = "Nil"
    return fixed_amount



def format_fix_table(table, fix_key):
    lines = []
    for line in table:
        newline = line.copy()
        newline[f"{fix_key}"] = format_fixer(line[f"{fix_key}"])
        lines.append(newline)

    return lines

def object_to_row(obj):
    return {
                "party" : obj.party, 
                "received_amount": format_fixer(obj.received_amount), 
                "payable_amounts":format_fixer(obj.payable_amounts), 
                "paid_amounts": format_fixer(obj.paid_amounts), 
                "outstanding_amount":format_fixer(obj.calculate_outstanding())
            }
 
class outstandings_row:
    def __init__(self, party, payable_amounts, received_amount, paid_amounts):
        self.party= party
        self.received_amount = received_amount
        self.payable_amounts = payable_amounts
        self.paid_amounts = paid_amounts

    def calculate_outstanding(self):
        return (self.payable_amounts - self.paid_amounts + self.received_amount)