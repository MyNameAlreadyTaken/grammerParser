from grammarParser.CFG import CFG
from grammarParser.ProductionSet import ProductionSet
from grammarParser.Production import Production

class SLR(CFG):

    class Operation:
        def __init__(self, action, index):
            self.action = action
            self.index = index

        def get_action(self):
            return self.action

        def get_index(self):
            return self.index

        def __eq__(self, other):
            if type(other) != SLR.Operation:
                return False
            return self.action == other.get_action() and self.index == other.get_index()

        def __str__(self):
            actString = ''
            if self.action == 'SHIFT':
                actString += 's'
            elif self.action == 'REDUCE':
                actString += 'r'
            elif self.action == 'GOTO':
                actString += 'g'

            actString += str(self.index)
            if self.index is None:
                return ' '
            else:
                return actString

    def __init__(self, filename : str):
        CFG.__init__(self, filename)
        self.__itemSet = []
        self.__goto = {}
        self.__reduce = {}
        self.__action = {}

        self.__initGoto()
        self.__initReduce()
        self.__initAction()
        self.__print()

    def __print(self):
        width = '%-25s'
        width2 = '%-10s'
        terminalList = self.terminalList[::]
        terminalList.append('$')
        if 'e' in terminalList:
            terminalList.remove('e')
        nonTerminalList = self.nonTerminalList[::]
        if self.startSymbol in nonTerminalList:
            nonTerminalList.remove(self.startSymbol)

        print('PRODUCTIONS')
        for p in self.productions:
            print(width % str(p.get_productionNum()), end='')
            print(str(p))
        print()

        print('FIRST')
        for nonTerminal in nonTerminalList:
            print(width % (nonTerminal), end='')
            print(self.first([nonTerminal]))
        print()

        print('FOLLOW')
        for nonTerminal in nonTerminalList:
            print(width % (nonTerminal) ,end='')
            print(self.follow(nonTerminal))
        print()

        print('STATES')
        for j in range(len(self.__itemSet)):
            print(width % ('I' + str(j)), end='')
        print()

        i = 0
        while True:
            flag = True
            for productionSet in self.__itemSet:
                if i < len(productionSet.get_productions()):
                    print(width % productionSet.get_productions()[i].to_LRstring(), end='')
                    flag = False
                else:
                    print(width % ' ', end='')
            print()
            if flag:
                break
            i += 1

        print('TABLE ACTION')
        print(width2 % ' ', end='')
        for terminal in terminalList:
            print(width2 % terminal, end='')
        for nonTerminal in nonTerminalList:
            print(width2 % nonTerminal, end='')
        print()

        terminalList += nonTerminalList
        for i in range(len(self.__itemSet)):
            print(width2 % (' ' + str(i)), end='')
            for symbol in terminalList:
                if i not in self.__action.keys():
                    self.__action[i] = {}
                if symbol not in self.__action[i].keys():
                    self.__action[i][symbol] = None
                if self.__action[i][symbol] is None:
                    print(width2 % '', end='')
                elif str(self.__action[i][symbol]) == 'r' + str(len(self.productions) - 1):
                    print(width2 % 'acc', end='')
                else:
                    print(width2 % self.__action[i][symbol], end='')
            print()
        print()

    def goto(self, productionIndex : int, symbol : str):
        productionSetSource = self.__itemSet[productionIndex]
        productionSetDestination = ProductionSet()

        for production in productionSetSource.get_productions():
            if symbol == production.indexNext():
                productionSetDestination.productions.append(production.next())
        if len(productionSetDestination.get_productions()) == 0:
            return None
        else:
            return self.__closure(productionSetDestination)

    def __closure(self, P):
        result = ProductionSet()
        result.productions += P.productions
        flag = True
        while flag:
            flag = False
            for i in range(len(result.productions)):
                p = result.get_productions()[i]
                if p.indexNext() in self.terminalSet:
                    continue
                nonTerminalSymbol = p.indexNext()
                for p2 in self.productions:
                    if p2.get_head() == nonTerminalSymbol:
                        newProduction = Production(p2.get_head(), p2.get_body(),
                                                   p2.get_productionNum(), 0, p2.get_isExtendProduction())

                        cmp = [production == newProduction for production in result.get_productions()]
                        if True not in cmp:
                            result.productions.append(newProduction)
                            flag = True
        return result

    def __initGoto(self):
        self.__itemSet.clear()
        tmp = self.productions[-1]
        tmp = Production(tmp.get_head(), tmp.get_body(), tmp.get_productionNum(), 0, tmp.get_isExtendProduction())
        start = ProductionSet()
        start.productions.append(tmp)

        self.__itemSet.append(self.__closure(start))
        self.__goto[0] = {}

        flag = True
        while flag:
            flag = False
            for i in range(len(self.__itemSet)):
                for nonTerminalSymbol in self.nonTerminalList:
                    gotoSet = self.goto(i, nonTerminalSymbol)
                    if gotoSet is None:
                        self.__goto[i][nonTerminalSymbol] = None
                    elif gotoSet not in self.__itemSet:
                        flag = True
                        self.__itemSet.append(gotoSet)
                        self.__goto[i][nonTerminalSymbol] = len(self.__itemSet) - 1
                        self.__goto[len(self.__itemSet) - 1] = {}
                    else:
                        index = self.__itemSet.index(gotoSet)
                        if i not in self.__goto.keys():
                            self.__goto[i] = {}
                        if nonTerminalSymbol not in self.__goto[i].keys():
                            self.__goto[i][nonTerminalSymbol] = None
                        if self.__goto[i][nonTerminalSymbol] is None:
                            self.__goto[i][nonTerminalSymbol] = index
                        else:
                            if self.__goto[i][nonTerminalSymbol] != index:
                                print('collision of shifts: GOTO[' + str(i) + ', '
                                      + nonTerminalSymbol + '](not null) = ' + str(index))

                for terminalSymbol in self.terminalList:
                    gotoSet = self.goto(i, terminalSymbol)
                    if gotoSet is None:
                        self.__goto[i][terminalSymbol] = None
                    elif True not in [gotoSet == i for i in self.__itemSet]:
                        flag = True
                        self.__itemSet.append(gotoSet)
                        self.__goto[i][terminalSymbol] = len(self.__itemSet) - 1
                        self.__goto[len(self.__itemSet) - 1] = {}
                    else:
                        index = self.__itemSet.index(gotoSet)
                        if i not in self.__goto.keys():
                            self.__goto[i] = {}
                        if terminalSymbol not in self.__goto[i].keys():
                            self.__goto[i][terminalSymbol] = None
                        if self.__goto[i][terminalSymbol] is None:
                            self.__goto[i][terminalSymbol] = index
                        else:
                            if self.__goto[i][terminalSymbol] != index:
                                print('collision of shifts: GOTO[' + str(i) + ', '
                                      + terminalSymbol + '](not null) = ' + str(index))

    def __initReduce(self):
        for i in range(len(self.__itemSet)):
            tmp = {}
            for terminal in self.terminalSet:
                tmp[terminal] = None
            tmp['$'] = None
            self.__reduce[i] = tmp

        for i in range(len(self.__itemSet)):
            for production in self.__itemSet[i].get_productions():
                if production.indexNext() is None:
                    for terminal in self.follow(production.get_head()):
                        entry = self.__reduce[i][terminal]
                        if entry is not None and entry != production.get_productionNum():
                            print('collision of reduces: Reduce[' + str(i) + ', ' +
                                  '](not null)' + str(production.get_productionNum()))
                        else:
                            self.__reduce[i][terminal] = production.get_productionNum()

    def __initAction(self):
        for i in range(len(self.__itemSet)):
            tmp = {}
            for terminal in self.terminalSet:
                tmp[terminal] = None
            tmp['$'] = None
            for nonTerminal in self.nonTerminalSet:
                tmp[nonTerminal] = None
            tmp['$'] = None
            self.__action[i] = tmp

        for key, value in self.__reduce.items():
            for key2, value2 in value.items():
                if value2 is None:
                    continue
                entryToBeInserted = SLR.Operation('REDUCE', value2)
                if key not in self.__action.keys():
                    self.__action[key] = {}
                if key2 not in self.__action[key].keys():
                    self.__action[key][key2] = None
                self.__action[key][key2] = entryToBeInserted
        for key, value in self.__goto.items():
            for key2, value2 in value.items():
                if key not in self.__action.keys():
                    self.__action[key] = {}
                if key2 not in self.__action[key].keys():
                    self.__action[key][key2] = None
                entry = self.__action[key][key2]
                if value2 is None:
                    continue
                if key2 in self.terminalSet:
                    entryToBeInserted = SLR.Operation('SHIFT', value2)
                else:
                    entryToBeInserted = SLR.Operation('GOTO', value2)
                if entry is not None and (entry == entryToBeInserted) == False:
                    print('collision of shift and reduce: ACTION[' + str(key) + ', ' +
                          str(key2) + '](not null)' + str(entryToBeInserted))
                else:
                    self.__action[key][key2] = entryToBeInserted

    def analyze(self, s : str, sdd : bool):
        print('-------------------------------------------------------------------------------------------' * 2)
        print('待识别的输入为：' + s + '\n')
        tmp = s.split(' ')
        tmp = [i.strip() for i in tmp]
        stringArray = tmp[::]
        stringArray.append('$')

        symbolStack = []
        stateStack = []
        index = 0
        stateStack.append(0)

        rWidth = '%35s'
        lWidth = '%-30s'
        print(lWidth % 'STATE STACK', end='')
        print(lWidth % 'SYMBOL STACK', end='')
        print(rWidth % 'CURRENT INPUT', end='')
        print(rWidth % 'ACTION')

        val = []
        process = []
        rule = ''
        while True:
            print(lWidth % (str(stateStack)), end='')
            print(lWidth % (str(symbolStack)), end='')
            print(rWidth % (str(stringArray[index::])), end='')

            stateTopState = stateStack[-1]
            act = self.__action[stateTopState][stringArray[index]]

            if act is None:
                print(rWidth % 'ERROR')
                return False
            elif act.action == 'SHIFT':
                print(rWidth % ('shift in'))

                stateStack.append(act.index)
                symbolStack.append(stringArray[index])
                val = val[::]
                val.append(stringArray[index])
                rule = 'shift in'
                process.append([val, rule])
                index += 1
            elif act.action == 'REDUCE':
                p = self.productions[act.index]

                if p.get_isExtendProduction():
                    print(rWidth % ('accepted'))
                    break
                else:
                    print(rWidth % ('reduce ' + str(p)))
                    for i in range(len(p.get_body())):
                        symbolStack.pop()
                        stateStack.pop()
                    stateTopState = stateStack[-1]
                    stateStack.append(self.__action[stateTopState][p.get_head()].index)
                    symbolStack.append(p.get_head())
                    if sdd:
                        val = val[::]
                        rule = rule[::]
                        if '+' in p.get_body():
                            num2 = val[-1]
                            val.pop()
                            val.pop()
                            num1= val[-1]
                            val[-1] = str(eval(num1 + '+' + num2))
                            rule = p.get_head() + '.val = ' + ' '.join(p.get_body()) + '.val'
                            rule = rule[:rule.index(' +'):] + '.val' + rule[rule.index(' +')::]
                        elif '*' in p.get_body():
                            num2 = val[-1]
                            val.pop()
                            val.pop()
                            num1 = val[-1]
                            val[-1] = str(eval(num1 + '*' + num2))
                            rule = p.get_head() + '.val = ' + ' '.join(p.get_body()) + '.val'
                            rule = rule[:rule.index(' *'):] + '.val' + rule[rule.index(' *')::]
                        elif ''.join(p.get_body()) in '0123456789':
                            rule = p.get_head() + '.lexval = ' + ''.join(p.get_body())
                        elif '(' in p.get_body() and ')' in p.get_body():
                            val.pop()
                            num = val[-1]
                            val[-1] = num
                            rule = p.get_head() + '.val = ' + ''.join(p.get_body())
                            rule = rule[:rule.index(' )'):] + '.val' + rule[rule.index(' )'):]
                        else:
                            rule = p.get_head() + '.val = ' + rule.split('=')[0].strip()
                        process.append([val, rule])
            else:
                print(rWidth % 'ERROR')
                return False
        print()
        if sdd:
            print('---------------------------------------------------------------------------------------' * 2)
            print('语法制导的翻译过程：')
            print(lWidth % '语法分析栈变化过程', end='')
            print(lWidth % '翻译过程')
            for i in process:
                print(lWidth % i[0], end='')
                print(lWidth % i[1])
            print()
            print(s + ' = ' + process[-1][0][0])
            print()
