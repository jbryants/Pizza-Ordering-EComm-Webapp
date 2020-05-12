from django import template

register = template.Library()


@register.filter()
def diff(val):
    """
    Take the last number of the card deck for loop and 
    return str of length equal to number of iterations
    required to cover up extra card space.
    """
    # for eg:- val = 9
    # 9 % 4 = 1 so 4 - 1 = 3, 3 card spaces empty
    num = 4 - (val % 4)
    # range(3) -> ['0', '1', '2'] -> "012"
    rangeStr = ''.join([str(i) for i in range(num)])
    return rangeStr