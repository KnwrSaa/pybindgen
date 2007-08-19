
from typehandlers.base import ReturnValue, Parameter
from module import Module
from function import Function
from typehandlers.codesink import CodeSink, FileCodeSink
from cppclass import CppMethod, CppClass, CppConstructor

def write_preamble(code_sink, min_python_version=(2, 3)):
    """
    Write a preamble, containing includes, #define's and typedef's
    necessary to correctly compile the code with the given minimum python
    version.
    """
    
    assert isinstance(code_sink, CodeSink)
    assert isinstance(min_python_version, tuple)

    code_sink.writeln('''
#define PY_SSIZE_T_CLEAN
#include <Python.h>
''')

    if min_python_version < (2, 4):
        code_sink.writeln(r'''
#if PY_VERSION_HEX < 0x02040000

#define Py_CLEAR(op)				\
        do {                            	\
                if (op) {			\
                        PyObject *tmp = (PyObject *)(op);	\
                        (op) = NULL;		\
                        Py_DECREF(tmp);		\
                }				\
        } while (0)

#endif
''')

    if min_python_version < (2, 5):
        code_sink.writeln(r'''
#if PY_VERSION_HEX < 0x02050000

typedef int Py_ssize_t;
# define PY_SSIZE_T_MAX INT_MAX
# define PY_SSIZE_T_MIN INT_MIN
typedef inquiry lenfunc;
typedef intargfunc ssizeargfunc;
typedef intobjargproc ssizeobjargproc;

#define Py_VISIT(op)							\
        do { 								\
                if (op) {						\
                        int vret = visit((PyObject *)(op), arg);	\
                        if (vret)					\
                                return vret;				\
                }							\
        } while (0)

#endif
''')

    code_sink.writeln(r'''
#if     __GNUC__ > 2
# define PYBINDGEN_UNUSED(param) param __attribute__((__unused__))
#elif     __GNUC__ > 2 || (__GNUC__ == 2 && __GNUC_MINOR__ > 4)
# define PYBINDGEN_UNUSED(param) __attribute__((__unused__)) param
#else
# define PYBINDGEN_UNUSED(param)
#endif  /* !__GNUC__ */
''')
    
