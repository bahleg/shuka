from tr_local import *

from shuka_lib.mocks import not_implemented_log


class IdRenderSystem:
    def init(self):
        raise NotImplementedError()

    _instance = None

    @staticmethod
    def get_instance():
        return IdRenderSystem._instance

    def __init__(self):
        IdRenderSystem._instance = self


class IdRenderSystemLocal(IdRenderSystem):
    """
    id:
    Most renderer globals are defined here.
    backend functions should never modify any of these fields,
    but may read fields that aren't dynamically modified
    by the frontend.
    */
    """

    def __init__(self):
        IdRenderSystem.__init__(self)
        # id: incremented every view (twice a scene if subviewed)
        self.view_count = 0
        self.ambient_light_vector = np.zeros(4)  # id: used for "ambient bump mapping"
        self.identity_space = ViewEntity()  # id: can use if we don't know viewDef->worldSpace is valid

    def init(self):
        # id : clear all our internal state
        self.view_count = 1  # id : so cleared structures never match viewCount
        # id: we used to memset tr, but now that it is a class, we can't, so
        # id: there may be other state we need to reset
        self.ambient_light_vector = np.array([0.5, 0.5 - 0.385, 0.8925, 1.0])
        # memset( &backEnd, 0, sizeof( backEnd ) );
        not_implemented_log('R_InitCVars(), R_InitCommands()')
        not_implemented_log('gui, cinematic, etc.')
        not_implemented_log('render Model Manager')
        # id: set the identity space
        self.identity_space.model_matrix[0 * 4] = 1.0
        self.identity_space.model_matrix[1 * 4 + 1] = 1.0
        self.identity_space.model_matrix[2 * 4 + 2] = 1.0
