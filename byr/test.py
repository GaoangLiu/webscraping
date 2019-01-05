

SESSION = 0

def f1():
	print(SESSION)


def f2():
	global SESSION
	SESSION = 9

f2()
f1()