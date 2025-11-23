class BTreeNode:
    def __init__(self, t, leaf=False):
        """
        Node pada B-Tree:
        t     : derajat (degree)
        leaf  : True jika node adalah daun
        """
        self.t = t
        self.keys = []         
        self.values = []       
        self.children = []     
        self.leaf = leaf       

    def is_full(self):
        """
        Mengecek apakah node sudah penuh.
        Node penuh jika jumlah key == 2t - 1
        """
        return len(self.keys) == (2 * self.t - 1)

    def __str__(self):
        """
        Representasi node untuk debugging
        """
        return (
            f"BTreeNode(leaf={self.leaf}, "
            f"keys={self.keys}, children={len(self.children)})"
        )
