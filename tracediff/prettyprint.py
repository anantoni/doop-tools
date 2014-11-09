# Pretty printing utilities

def rectprint(line):
    border = '+' + "".join('-' for i in range(len(line) + 2)) + '+';
    return "{0}\n| {1} |\n{0}".format(border, line)

