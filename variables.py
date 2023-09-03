from typing import Any


class settings:
	"""
	Assembler settings like exit_on_errors.
	>>> settings.mode(int, bool, bool, bool)
	"""

	tab_size = 20
	exit_on_errors = False
	perf_print = False
	skip_times = False

	def mode(*args: Any) -> None:
		"""
		Change settings.
		"""

		settings.tab_size = args[0]
		settings.exit_on_errors = args[1]
		settings.perf_print = args[2]
		settings.skip_times = args[3]


class colors:
	"""
	Unicode color codes in a class.
	"""

	ITALIC =  "\033[3m"
	DARK =	  "\033[30m"
	SECOND =  "\033[34m"
	ERROR =	  "\033[31m"
	WARNING = "\033[93m"
	ENDL =	  "\033[0m"


BYTE = 2
WORD = 4
DWORD = 8

sizes = {
	"byte":	 BYTE,
	"short": BYTE,
	"x8":	 BYTE,
	"word":	 WORD,
	"x16":	 WORD,
	"dword": DWORD,
	"long":	 DWORD,
	"x32":	 DWORD,
}

constants: dict[str, int] = {}
addr = 0
orgin = 0

# BIT_32 = 0x66
STR_BIT_32 = "66"

regs8 = ["al", "cl", "bl", "dl", "ah", "bh", "ch", "dh"]
regs16_32 = ["ax", "cx", "dx", "bx", "sp", "bp", "si", "di"]

str_regs = regs8 + regs16_32

# REGS_LEN = 16
REG_INDEX_LEN = 8

one_inst = {
	"hlt": "f4",
	"nop": "90",
}

added: list[str] = []
memory: list[str] = []

_splitter = "---"

def _split_list(list_: list[str], sep: str = _splitter) -> list[list[str]]:
	retu: list[list[str]] = []
	tmp: list[str] = []
	for i in list_:
		i = i.strip()
		if i == sep:
			retu.append(tmp.copy())
			tmp.clear()
		else:
			tmp.append(i)
	retu.append(tmp)
	del tmp
	return retu


test_cases_file = open("test_cases.txt")
test_cases = _split_list(test_cases_file.readlines()) + [
	["not " + i for i in str_regs]
	+ ["not e" + i for i in regs16_32]
	+ ["not *0x4321", "not byte *0x4321"]
]
test_cases_file.close()

if __name__ == "__main__":
	print("\n\n".join(["\n".join(i) for i in test_cases]))
	input()
	for i in range(100):
		print(f"\033[{i}m{i} abc{colors.ENDL}")
