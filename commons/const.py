import sys


class Const(object):
    """
    常量类实现机制
    """

    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


sys.modules[__name__] = Const()
