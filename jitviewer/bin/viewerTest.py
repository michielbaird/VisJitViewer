import sys
import runpy
import pypyjit
from pypy.tool.jitlogparser import parser
from pypy.tool.jitlogparser.storage import LoopStorage
pypyjit.set_param('default')
l = []
l2 = []
l3 = []
def hook(jitdriver_name, loop_type, greenkey, operations,
     assembler_addr, assembler_length): 
    l.append((jitdriver_name, loop_type, greenkey, operations,
     assembler_addr, assembler_length))
    print "Driver:",jitdriver_name
    print "Type: ", loop_type
    print "Operations:"
    for op in operations:
        print op.name
        print op.num
        if op.name == "debug_merge_point":
	     print dir(op.pycode)
             print op.pycode.co_code
        print dir(op)
        
def hook2(*args):
    l2.append(args)
    
def hook3(*args):
    l3.append(args)
    
pypyjit.set_compile_hook(hook)
pypyjit.set_optimize_hook(hook2)
pypyjit.set_abort_hook(hook3)
runpy.run_path(sys.argv[1])
pypyjit.set_compile_hook(None)
pypyjit.set_optimize_hook(None)
pypyjit.set_abort_hook(None)

for jitdriver_name, loop_type, greenkey, operations, assembler_addr, assembler_length in l:
    storage =  LoopStorage()
    try:
        code = storage.load_code(loop.filename)[(loop.startlineno,
                                                      loop.name)]
        if code.co_name == '<module>' and code.co_firstlineno == 1:
            with open(code.co_filename) as f:
                source = CodeRepr(f.read(), code, loop)
        else:
            source = CodeRepr(inspect.getsource(code), code, loop)
    except (IOError, OSError):
        source = CodeReprNoFile(loop)
    print source

    parse = parser.Function.from_operations(operations,storage)
    
    print "b" 
    print parse
print "l1: ",l
print "l2: ",l2
print "l3: ",l3
