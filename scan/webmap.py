# coding:GBK

# 形成站点地图信息
# author:wuwh

class WebsitrTree(object):
    def __init__(self,startValue):
        startNode=TreeNode(nodevalue=startValue,parentnode=None)
        self.startnode = startNode
    def addChild(self,childValue,paraentValue):
        startnode = self.startnode
        startnode.addChild(childValue,parentValue=paraentValue)

    def getDeep(self,nodeValue):
        # i=0;
        startNode = self.startnode
        # if startNode.value==nodeValue:
        #     return 0
        node = startNode.findNodeValue(nodevalue=nodeValue)
        if node!=None:
            return node.level
        return -1


#
# 树形节点
# author:wuwh
class TreeNode(object):
    def __init__(self,nodevalue,parentnode=None):
        #本节点上的数据
        self.value=nodevalue
        #此节点的子节点
        self.children = []
        if parentnode==None:
            self.level=0;
        else :
            self.level=parentnode.level+1
        self.parent=parentnode
    def addChildValue(self,childvalue):
        child =TreeNode(nodevalue=childvalue,parentnode=self)
        self.children.append(child)
    def addChild(self,chaildVlaue,parentValue):
        if self.value == parentValue:
            self.addChildValue(chaildVlaue)
            return
        for child in self.children:
            child.addChild(chaildVlaue,parentValue)
    def findNodeValue(self,nodevalue):
        if self.value ==nodevalue:
            return self
        for children in self.children:
            findNode =  children.findNodeValue(nodevalue)
            if findNode!=None:
                return findNode
        return None


    def printNode(self):
        # print "     "+self.value+"     "
        print self.value+" : children ------->[   "

        for node in self.children:
            node.printNode()
        print "  ]"
if __name__ == '__main__':
    tree = TreeNode(nodevalue="1",parentnode=None)
    tree.addChild("2","1")
    tree.addChild("3","1")
    tree.addChild("4","3")
    tree.printNode()
    print tree.findNodeValue("1").level