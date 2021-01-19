from grammarParser.ProductionSet import ProductionSet
from grammarParser.Production import Production

class CFG(ProductionSet):

    def __init__(self, filename : str):
        ProductionSet.__init__(self)
        self.nonTerminalSet = set()
        self.terminalSet = set()
        self.nonTerminalList = []
        self.terminalList = []
        self.__first = {}
        self.__follow = {}
        self.filename = filename
        self.__read()
        self.startSymbol = self.productions[0].get_head()
        self.productions.append(Production(self.startSymbol + '\'', [self.startSymbol],
                                           len(self.productions), None, True))
        self.startSymbol += '\''

        self.__initTerminalSet()
        self.__initFirst()
        self.__initFollow()

    def __read(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            raw = [line.strip().split('->') for line in lines]
            while [''] in raw:
                raw.remove([''])
            raw_productions = []
            for i in raw:
                raw_productions.append([i[0], i[1].strip().split('|')])
            index = 0
            for i in range(len(raw_productions)):
                for j in range(len(raw_productions[i][1])):
                    rights = raw_productions[i][1][j].strip().split(' ')
                    self.productions.append(Production(raw_productions[i][0].strip(), rights, index, None, False))
                    index += 1

    def __initTerminalSet(self):
        # self.nonTerminalList = []
        # self.terminalList = []
        # self.nonTerminalSet = set()
        symbolTable = set()

        for production in self.productions:
            productionHead = production.get_head()
            productionBody = production.get_body()

            self.nonTerminalSet.add(productionHead)
            if productionHead not in self.nonTerminalList:
                self.nonTerminalList.append(productionHead)
            symbolTable.add(productionHead)
            for symbol in productionBody:
                if symbol not in self.terminalList:
                    self.terminalList.append(symbol)
                symbolTable.add(symbol)

        for nonTerminalSymbol in self.nonTerminalSet:
            if nonTerminalSymbol in symbolTable:
                symbolTable.remove(nonTerminalSymbol)
            if nonTerminalSymbol in self.terminalList:
                self.terminalList.remove(nonTerminalSymbol)

        self.terminalSet = symbolTable

    def __initFirst(self):
        # self.__first = {}
        for nonTerminal in self.nonTerminalSet:
            self.__first[nonTerminal] = set()
        for terminal in self.terminalSet:
            terminalFirstSet = set()
            terminalFirstSet.add(terminal)
            if terminal not in self.__first.keys():
                self.__first[terminal] = set()
            self.__first[terminal] |= terminalFirstSet

        isChanged = True
        while isChanged:
            isChanged = False
            for production in self.productions:
                head = production.get_head()
                productionBody = production.get_body()
                nonTerminalFirstBeforeSize = len(self.__first[head])

                i = 0
                for i in range(len(productionBody)):
                    symbolIFirst = set(self.__first[productionBody[i]])
                    containsEpsilon = False
                    if 'e' in symbolIFirst:
                        containsEpsilon = True
                        symbolIFirst.remove('e')
                    self.__first[head] |= symbolIFirst
                    if not containsEpsilon:
                        break

                if i == len(productionBody):
                    self.__first[head].add('e')

                nonTerminalFirstAfterSize = len(self.__first[head])
                if nonTerminalFirstAfterSize != nonTerminalFirstBeforeSize:
                    isChanged = True

    def __initFollow(self):
        # self.__follow = {}
        for nonTerminal in self.nonTerminalSet:
            self.__follow[nonTerminal] = set()
        self.__follow[self.startSymbol].add('$')

        isChanged = True
        while isChanged:
            isChanged = False
            for production in self.productions:
                head = production.get_head()
                productionBody = production.get_body()

                for symbolIndex in range(len(productionBody)):
                    if productionBody[symbolIndex] in self.nonTerminalSet:
                        nonTerminal = productionBody[symbolIndex]
                        nonTerminalFollowBeforeSize = len(self.__follow[nonTerminal])

                        nonTerminalFollow = self.first(productionBody[symbolIndex + 1: len(productionBody): ])
                        containsEpsilon = False
                        if 'e' in nonTerminalFollow:
                            nonTerminalFollow.remove('e')
                            containsEpsilon = True
                        self.__follow[nonTerminal] |= nonTerminalFollow
                        if containsEpsilon:
                            self.__follow[nonTerminal] |= self.__follow[head]

                        nonTerminalFollowAfterSize = len(self.__follow[nonTerminal])
                        if nonTerminalFollowAfterSize != nonTerminalFollowBeforeSize:
                            isChanged = True

    def first(self, s):
        sFirst = set()
        i = 0
        for i in range(len(s)):
            symbolIFirst = set(self.__first[s[i]])
            containsEpsilon = False
            if 'e' in symbolIFirst:
                containsEpsilon = True
                symbolIFirst.remove('e')
            sFirst |= symbolIFirst
            if not containsEpsilon:
                break

        if i == len(s):
            sFirst.add('e')
        return sFirst

    def follow(self, nonTerminal):
        # if nonTerminal not in self.__follow.keys():
        #     self.__follow[nonTerminal] = set()
        return self.__follow[nonTerminal]
    