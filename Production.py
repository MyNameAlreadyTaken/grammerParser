class Production():
    def __init__(self, head, body, productionNum, pointIndex, isExtendProduction):
        self.head = head
        self.body = body
        self.productionNum = productionNum
        self.pointIndex = pointIndex
        self.isExtendProduction = isExtendProduction

    def indexNext(self):
        if self.pointIndex is None:
            return ''
        if self.pointIndex == len(self.body):
            return None
        return self.body[self.pointIndex]

    def next(self):
        if self.indexNext() is None:
            return ''
        return Production(self.head, self.body, self.productionNum, self.pointIndex + 1, self.isExtendProduction)

    def get_head(self):
        return self.head

    def get_body(self):
        return self.body

    def get_productionNum(self):
        return self.productionNum

    def get_pointIndex(self):
        return self.pointIndex

    def get_isExtendProduction(self):
        return self.isExtendProduction

    def __eq__(self, other):
        if type(other) != Production:
            return False

        return self.head == other.get_head() and self.body == other.get_body() \
               and self.productionNum == other.get_productionNum() and self.pointIndex == other.get_pointIndex() \
               and self.isExtendProduction == other.get_isExtendProduction()

    def __str__(self):
        return self.head + '->' + str(self.body)

    def to_LRstring(self):
        Body = []
        for i in range(len(self.body)):
            if i == self.pointIndex:
                Body.append('.')
            Body.append(self.body[i])

        if self.pointIndex == len(self.body):
            Body.append('.')
        return self.head + '->' + str(Body)
    