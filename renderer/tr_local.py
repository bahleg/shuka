import numpy as np
class ViewEntity:
    def __init__(self):
        """
        id:
        a viewEntity is created whenever a idRenderEntityLocal is considered for inclusion
        in the current view, but it may still turn out to be culled.
        viewEntity are allocated on the frame temporary stack memory
        a viewEntity contains everything that the back end needs out of a idRenderEntityLocal,
        which the front end may be modifying simultaniously if running in SMP mode.
        A single entityDef can generate multiple viewEntity_t in a single frame, as when seen in a mirror
        :return:
        """
        #id : back end should NOT reference the entityDef, because it can change when running SMP
        self.next = None
        """
        id: for scissor clipping, local inside renderView viewport
        scissorRect.Empty() is true if the viewEntity_t was never actually
        seen through any portals, but was created for shadow casting.
        a viewEntity can have a non-empty scissorRect, meaning that an area
        that it is in is visible, and still not be visible.
        """
        self.scissor_rect = None
        self.weapon_depth_hack = False
        self.model_depth_hack = 0.0
        self.model_matrix = np.zeros(16)#id :local coords to global coords
        self.model_view_matrix = np.zeros(16)#id: local coords to eye coords