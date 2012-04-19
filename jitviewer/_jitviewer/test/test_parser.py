from _jitviewer.parser import ParserWithHtmlRepr, cssclass
import py

def parse(input):
    return ParserWithHtmlRepr.parse_from_input(input)

def test_html_repr():
    ops = parse('''
    [i7]
    i9 = int_lt(i7, 1003)
    guard_true(i9, descr=<Guard2>) []
    i13 = getfield_raw(151937600, descr=<SignedFieldDescr pypysig_long_struct.c_value 0>)
    ''').operations
    assert '<' in ops[0].html_repr()
    assert 'pypysig_long_struct' in ops[2].html_repr()

def test_highlight_var():
    ops = parse('''
    [p0]
    guard_class(p0, 144264192, descr=<Guard0>)
    ''').operations
    assert len(ops) == 1
    op = ops[0]
    assert op.name == 'guard_class'
    html = op.html_repr()
    p0 = cssclass('p0', 'p0', onmouseover="highlight_var(this)", onmouseout="disable_var(this)")
    assert p0 in html

def test_cssclass():
    s = cssclass('asd$%', 'v')
    print s.__class__, s
    assert '$' not in s
