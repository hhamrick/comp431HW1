def main():
    while True:
        user_in = input()
        print(user_in)
        result = mail_from_cmd(user_in)
        if (result == ''):
            print('Sender ok')
        else:
            print(result)


def parse(string):
    result = mail_from_cmd(string)
    if (result == ''):
        print('Sender ok')
    else:
        print(result)


def mail_from_cmd(string):
    ERROR = 'ERROR -- mail-from-cmd'

    # expected string in form
    # “MAIL” <whitespace> “FROM:” <nullspace> <reverse-path> <nullspace> <CRLF>
    tokens = mail_from_cmd_tokenizer(string)

    # tokens should be in form:
    # [<whitespace>, <nullspace>, <reverse-path>, <nullspace>, <CRLF>]
    if len(tokens) != 5:
        return ERROR
    
    # functions for each corresponding token
    token_functions = [whitespace, nullspace, reverse_path, nullspace, crlf]
    for token, funct in zip(tokens, token_functions):
        result = funct(token)
        if result != '':
            return result

    return ''


def mail_from_cmd_tokenizer(string):
    # expected string in form:
    # “MAIL” <whitespace> “FROM:” <nullspace> <reverse-path> <nullspace> <CRLF>
    tokens = [''] * 5

    # MAIL and anything before
    split1 = string.split('MAIL', 1)
    if len(split1) != 2 or split1[0] != '':
        return []
    _, tail = split1

    # <whitespace>
    split2 = tail.split('FROM:', 1)
    if len(split2) != 2:
        return []
    tokens[0], tail = split2

    # <nullspace>
    split3 = tail.split('<', 1)
    if len(split3) != 2:
        return []
    tokens[1], tail = split3
    tail = '<' + tail

    # <reverse-path>
    split4 = tail.split('>', 1)
    if len(split4) != 2:
        return []
    tokens[2], tail = split4
    tokens[2] = tokens[2] + '>'

    # <nullspace> <CRLF>
    split5 = tail.split('\n')
    if len(split5) != 2:
        # leaves the CRLF token blank if no newline
        tokens[3] = tail
        return tokens
    tokens[3], tokens[4] = split5
    tokens[4] = '\n' + tokens[4]

    return tokens


def whitespace(string):
    ERROR = 'ERROR -- whitespace'
    
    if len(string) == 0:
        return ERROR
    for char in string:
        if char != ' ':
            return ERROR
        
    return ''


def nullspace(string):
    ERROR = 'ERROR -- nullspace'
    
    if len(string) == 0 or whitespace(string) == '':
        return ''
    return ERROR


def reverse_path(string):
    return path(string)


def path(string):
    ERROR = 'ERROR -- path'
    
    if len(string) < 2:
        return ERROR
    
    first = string[0]
    last = string[-1]
    if first != '<' or last != '>':
        return ERROR

    middle = string[1:-1]
    return mailbox(middle)
    

def mailbox(string):
    ERROR = 'ERROR -- mailbox'

    tokens = string.split('@', 1)
    if len(tokens) != 2:
        return ERROR
    before_at, after_at = tokens
    
    lp_result = local_part(before_at)
    if lp_result != '':
        return lp_result
    
    d_result = domain(after_at)
    return d_result


def local_part(string):
    return string_(string)


def string_(string):
    ERROR = 'ERROR -- string'
    SPECIALSP = '<>()[]\\.,;:@" '

    if len(string) < 1:
        return ERROR
    
    for char in string:
        if char in SPECIALSP or not char.isprintable():
            return ERROR

    return ''


def domain(string):
    tokens = string.split('.')
    for e in tokens:
        e_result = element(e)
        if e_result != '':
            return e_result
        
    return ''


def element(string):
    ERROR = 'ERROR -- element'

    if len(string) < 1 or not string[0].isalpha():
        return ERROR
    
    for c in string[1:]:
        if not c.isalnum():
            return ERROR

    return ''


def crlf(string):
    ERROR = 'ERROR -- CRLF'

    if string != '\n':
        return ERROR
    
    return ''


if __name__ == '__main__':
    main()