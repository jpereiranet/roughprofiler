import pyqtgraph as pg
from pyqtgraph.Qt import QtCore


class GraphPolyLine(pg.PolyLineROI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def checkPointMove(self, handle, pos, modifiers):
        if self.maxBounds is not None:
            pt = self.getViewBox().mapSceneToView(pos)

            if not self.maxBounds.contains(pt.x(), pt.y()):
                return False

        return True