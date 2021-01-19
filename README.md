编程环境：Windows 10
编程语言：Python 3.7

文件结构：
ten
（py文件）
----CFG.py
----Main.py
----Production.py
----ProductionSet.py
----SLR.py
（txt文件）
----productions1.txt
----productions2.txt
----test1.txt
----test2.txt

其中，
CFG.py定义了一个控制流程图（Control Flow Graph），
	能够生成终结符集合、FIRST集合和FOLLOW集合，
	用于被SLR分析器继承；
Main.py为用于运行测试用例的程序，有：
	test1方法：运行productions1.txt、test1.txt中的用例
	test2方法：运行productions2.txt、test2.txt中的用例
Production.py用于储存产生式的数据结构；
ProductionSet.py用于储存产生式集合的数据结构；
SLR.py定义了一个SLR语法分析器，可以生成项集族，构造语法分析表，从而构造SLR语法分析器。

productions1.txt包含了如下的内容：
	E -> E + T | T
	T -> T * F | F
	F -> ( E ) | id
	这是针对第一问的产生式集合；
productions2.txt包含了如下内容：
	E -> E + T | T
	T -> T * F | F
	F -> ( E ) | id
	id -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
	这是针对第二问的产生式集合；
test1.txt包含了对第一问的输入：
	id + id * id
	id * + id + id
test2.txt包含了对第二问的输入：
	8 + 5 * 2
