import re
import cgi
from pypy.tool.jitlogparser import parser

def cssclass(cls, s, **kwds):
    cls = re.sub("[^\w]", "_", cls)
    attrs = ['%s="%s"' % (name, value) for name, value in kwds.iteritems()]
    return '<span class="%s" %s>%s</span>' % (cls, ' '.join(attrs),
                                              cgi.escape(s))


def _new_binop(name):
    name = cgi.escape(name)
    def f(self):
        return '%s = %s %s %s' % (self.wrap_html(self.res),
                                  self.wrap_html(self.args[0]),
                                  name, self.wrap_html(self.args[1]))
    return f

class Html(str):
    def __html__(self):
        return self

class OpHtml(parser.Op):
    """
    Subclass of Op with human-friendly html representation
    """

    def html_class(self):
        if self.is_guard():
            return "single-operation guard"
        elif 'call' in self.name:
            return "single-operation call"
        else:
            return "single-operation"

    def html_repr(self):
        s = getattr(self, 'repr_' + self.name, self.default_repr)()
        return Html(s)

    def wrap_html(self, v):
        return cssclass(v, v, onmouseover='highlight_var(this)', onmouseout='disable_var(this)')

    for bin_op, name in [('==', 'int_eq'),
                         ('!=', 'int_ne'),
                         ('==', 'float_eq'),
                         ('!=', 'float_ne'),
                         ('>', 'int_gt'),
                         ('<', 'int_lt'),
                         ('<=', 'int_le'),
                         ('>=', 'int_ge'),
                         ('+', 'int_add'),
                         ('+', 'float_add'),
                         ('-', 'int_sub'),
                         ('-', 'float_sub'),
                         ('*', 'int_mul'),
                         ('*', 'float_mul'),
                         ('&', 'int_and')]:
        locals()['repr_' + name] = _new_binop(bin_op)

    def repr_guard_true(self):
        return 'guard(%s is true)' % self.wrap_html(self.args[0])

    def repr_guard_false(self):
        return 'guard(%s is false)' % self.wrap_html(self.args[0])

    def repr_guard_value(self):
        return 'guard(%s == %s)' % (self.wrap_html(self.args[0]),
                                    self.wrap_html(self.args[1]))

    def repr_guard_isnull(self):
        return 'guard(%s is null)' % self.wrap_html(self.args[0])

    def repr_getfield_raw(self):
        name, field = self.descr.split(' ')[1].rsplit('.', 1)
        return '%s = ((%s)%s).%s' % (self.wrap_html(self.res), name,
                                     self.wrap_html(self.args[0]), field[2:])

    def repr_getfield_gc(self):
        fullname, field = self.descr.split(' ')[1].rsplit('.', 1)
        names = fullname.rsplit('.', 1)
        if len(names) == 2:
            namespace, classname = names
        else:
            namespace = ''
            classname = names[0]
        namespace = cssclass('namespace', namespace)
        classname = cssclass('classname', classname)
        field = cssclass('fieldname', field)
            
        obj = self.getarg(0)
        return '%s = ((%s.%s)%s).%s' % (self.wrap_html(self.res),
                                        namespace, classname, obj, field)

    def repr_getfield_gc_pure(self):
        return self.repr_getfield_gc() + " [pure]"

    def repr_setfield_raw(self):
        name, field = self.descr.split(' ')[1].rsplit('.', 1)
        return '((%s)%s).%s = %s' % (name, self.wrap_html(self.args[0]),
                                     field[2:], self.wrap_html(self.args[1]))

    def repr_setfield_gc(self):
        name, field = self.descr.split(' ')[1].rsplit('.', 1)
        return '((%s)%s).%s = %s' % (name, self.wrap_html(self.args[0]),
                                     field, self.wrap_html(self.args[1]))

    def repr_jump(self):
        return ("<a href='' onclick='show_loop(\"%s\");return false'>" % self.descr
                + self.default_repr() + "</a>")

    def default_repr(self):
        args = [self.wrap_html(arg) for arg in self.args]
        if self.descr is not None:
            args.append('descr=%s' % cgi.escape(self.descr))
        arglist = ', '.join(args)
        if self.res is not None:
            return '%s = %s(%s)' % (self.wrap_html(self.res), self.name,
                                    arglist)
        else:
            return '%s(%s)' % (self.name, arglist)

    repr_call_assembler = repr_jump
    repr_label = repr_jump

    #def repr_call_assembler(self):
    #    xxxx

class ParserWithHtmlRepr(parser.SimpleParser):
    Op = OpHtml


class TraceForOpcodeHtml(parser.TraceForOpcode):

    def html_repr(self):
        if self.filename is not None:
            code = self.getcode()
            if code is None:
                return self.bytecode_name
            opcode = self.code.map[self.bytecode_no]
            return '%s %s' % (self.bytecode_name, opcode.argstr)
        else:
            return self.bytecode_name

class FunctionHtml(parser.Function):
    TraceForOpcode = TraceForOpcodeHtml
    
    def html_repr(self):
        return "inlined call to %s in %s" % (self.name, self.filename)

