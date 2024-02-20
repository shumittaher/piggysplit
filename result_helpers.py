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
 