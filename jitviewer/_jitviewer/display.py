from _jitviewer.parser import cssclass

class LineRepr(object):
    """ A representation of a single line
    """
    def __init__(self, line, in_loop, chunks=None):
        self.line = line.decode("utf-8")
        self.in_loop = in_loop
        if chunks is None:
            self.chunks = []
        else:
            self.chunks = chunks

class CodeReprNoFile(object):
    firstlineno = 0
    
    def __init__(self, loop):
        self.lines = [LineRepr('', True, loop.chunks)]

class CodeRepr(object):
    """ A representation of a single code object suitable for display
    """
    def __init__(self, source, code, loop):
        lineset = loop.lineset
        self.lines = []
        html = []
        for v in loop.inputargs:
            html.append(cssclass(v, v, onmouseover='highlight_var(this)', onmouseout='disable_var(this)'))
        self.inputargs = " ".join(html)
        self.firstlineno = code.co_firstlineno
        for i, line in enumerate(source.split("\n")):
            no = i + code.co_firstlineno
            in_loop = no in lineset
            self.lines.append(LineRepr(line, in_loop))

        last_lineno = self.firstlineno
        for chunk in loop.chunks:
            if chunk.is_bytecode:
                chunk.cssclass = 'dmp '
                if len(chunk.operations) <= 1:
                    chunk.cssclass += 'empty'
                else:
                    chunk.cssclass += 'nonempty'
                no = chunk.lineno
                if no is None or no < last_lineno:
                    no = last_lineno
                else:
                    last_lineno = no
            else:
                no = last_lineno
            self.lines[no - self.firstlineno].chunks.append(chunk)
    
        

