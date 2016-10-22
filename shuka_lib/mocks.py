import logging

_not_implemented_set  =set()

def not_implemented_log(what=''):
    global _not_implemented_set
    if what not in _not_implemented_set:
        logging.warning('not implemented:' + what)
        _not_implemented_set.add(what)
