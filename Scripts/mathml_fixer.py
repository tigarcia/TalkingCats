# This function takes a string of broken xml as input and outputs its best guess for a fixed version of the mathml
def str_to_mathml(s):
    r = ''
    stack = []
    while s:
        if s.startswith('<'):
            tag = s[:s.find('>') + 1]
            s = s[s.find('>') + 1:]

            if tag[1] != '/':
                r += tag
                stack.insert(0, tag)
            else:
                open = '<' + tag[2:]
                if open in stack:
                    while stack[0] != open:
                        r += '</' + stack.pop(0)[1:]
                    r += '</' + stack.pop(0)[1:]
        else:
            r += s[:1]
            s = s[1:]
    while stack:
        r += '</' + stack.pop(0)[1:]
    return "<math display='block' xmlns='http://www.w3.org/1998/Math/MathML'>" + r + "</math>"


# A couple of examples of the function running on broken xml
if __name__ == '__main__':
    print(str_to_mathml('<a>b'))
    print(str_to_mathml('<mi></mi><mn></mn></mn><mfrac><mo>â </mo><mo>&gt;</mo></msqrt>'))
    print(str_to_mathml('<mn>18</mn><msup><mi>x</mi><mn>2</mn></msup><msup><mi>b</mi><mn>5</mn></msup><mo>,</mo><mo>-</mo><mn>2</mn><msup><mi>x</mi><msup><mi>b</mi><mn>4</mn></msup></msup></mrow></mroot><mo>]</mo><mo>$</mo>'))
    print(str_to_mathml("<mn>3</mn><mi>x</mi><mn>2</mn></msup><mo>-</mo><mn>5</mn><mi>x</mi><mi>y</mi><mo>-</mo><mn>2</mn><mi>y</mi><mn>2</mn></msup></msup></mn><mo>=</mo>"))
