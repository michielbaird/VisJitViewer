
from _jitviewer.display import CodeRepr

class MockLoop(object):
    inputargs = []

class MockCode(object):
    pass

class MockChunk(object):
    is_bytecode = True
    
    def __init__(self, operations, lineno):
        self.operations = operations
        self.lineno = lineno

class Op(object):
    bridge = None
    
    def __init__(self, a):
        self.a = a

SOURCE = """def f():
return a + b
"""

def test_code_repr():
    loop = MockLoop()
    loop.chunks = [MockChunk([], 3), MockChunk([Op('a'), Op('b'), Op('c')], 4),
                   MockChunk([Op('a'), Op('b')], 4)]
    MockLoop.linerange = (4, 5)
    MockLoop.lineset = set([4, 5])
    code = MockCode()
    code.co_firstlineno = 3
    repr = CodeRepr(SOURCE, code, loop)
    assert len(repr.lines) == 3
    assert repr.lines[1].in_loop
    assert not repr.lines[0].in_loop
    assert repr.lines[0].chunks == [loop.chunks[0]]
    assert repr.lines[1].chunks == [loop.chunks[1], loop.chunks[2]]

def test_code_repr_bridgestate():
    pass
