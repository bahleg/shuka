from shuka_lib.mocks import not_implemented_log
class IdCmdSystem:
    def arg_completion_string(self, args, callback):
        raise NotImplementedError()

    def init(self):
        raise NotImplementedError()

    _instance = None

    @staticmethod
    def get_instance():
        return IdCmdSystem._instance

    def __init__(self):
        IdCmdSystem._instance = self

class IdCmdSystemLocal(IdCmdSystem):
    def init(self):
        not_implemented_log('Cmd System Init')
