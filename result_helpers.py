from babel.numbers import format_decimal

def format_fixer(amount):
    return format_decimal(amount, format='#,##0.##;(#)', locale='en')



def format_fix_table(table, fix_key):
    lines = []
    for line in table:
        newline = line.copy()
        newline[f"{fix_key}"] = format_fixer(line[f"{fix_key}"])
        lines.append(newline)

    return lines
 