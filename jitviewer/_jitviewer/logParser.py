import sys
import os.path
from pypy.tool.logparser import extract_category
from pypy.tool.jitlogparser.storage import LoopStorage
from pypy.tool.jitlogparser.parser import adjust_bridges, import_log,\
     parse_log_counts

def main():
    filename = sys.argv[1]
    extra_path = os.path.dirname(filename)
    storage = LoopStorage(extra_path)
    
    log, loops = import_log(filename, ParserWithHtmlRepr)
    parse_log_counts(extract_category(log, 'jit-backend-count'), loops)
    storage.loops = [loop for loop in loops
                     if not loop.descr.startswith('bridge')]
    storage.loop_dict = create_loop_dict(loops)
    print loops,log,storage
    server = Server(filename, storage)
    
   
main()
