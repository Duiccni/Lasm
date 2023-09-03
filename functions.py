from typing import Any
import variables as var


def toInt(x: str, spec: bool = True) -> int:
	"""
	Converts string value to intager value.
	Like int(x) function but specilized for LASM.
	"""
	if spec:
		if x[0] == "$":
			if len(x) == 1:
				return var.addr
			return var.orgin
		if x[0] == "&":
			return var.constants[x[1:]]
	if x[0] == "?":
		return 0
	if x[0] == "'":
		return ord(x[1])
	if x[0] == "^":
		return 1 << toInt(x[1:])
	return int(x, 0)


def _calculate(x: str, spec: bool = True) -> int:
	"""
	Calculates input value of string.
	>>> _calculate("3 + 5 - 3")
	5
	"""
	tmp = ""
	retu = 0
	sign = x[0] == "-"
	if sign or x[0] == "+":
		x = x[1:]
	for char in x:
		tmp2 = char == "-"
		if tmp2 or char == "+":
			retu += toInt(tmp, spec) * (-1 if sign else 1)
			tmp = ""
			sign = tmp2
		elif char != " ":
			tmp += char
	return retu + toInt(tmp, spec) * (-1 if sign else 1)


def convertInt(x: str, spec: bool = True) -> int:
	"""
	This converts to int like toInt(x) function but this checks input is calculateble value.
	"""
	if x[0] == "(":
		return _calculate(x[1:-1], spec)
	return toInt(x, spec)


def splitBytes(x: str) -> list[str]:
	"""
	Splits string to 2 character parts.
	"""
	if x.startswith("0x"):
		x = x[2:]
	return [x[i : i + var.BYTE] for i in range(0, len(x), var.BYTE)]


def zeroExtend(x: str, size: int = var.BYTE, notation: bool = True) -> str:
	"""
	Extends string with zeros.
	"""
	if x.startswith("0x"):
		x = x[2:]
	tmp = "0" * (size - len(x)) + x
	return "0x" + tmp if notation else tmp


def toHex(x: int, size: int = var.BYTE) -> str:
	"""
	Convert intager value to Hex string even negative values.
	"""
	return hex(x % (1 << (size << 2)))


def raiseError(
	title: str, msg: str, error: bool = True, line: int | None = None
) -> None:
	"""
	Print an error message acording Assembler settings.
	"""
	print(
		var.colors.WARNING + title + ":",
		(var.colors.ERROR if error else var.colors.SECOND) + msg + var.colors.ENDL,
		f"{var.colors.ITALIC}(Line {line if line != None else '?'}.){var.colors.ENDL}",
	)
	if error and var.settings.exit_on_errors:
		exit()


def findSize(
	x: int, stay_align: bool = True, forge_signed: bool = False
) -> int:  # 255, -128, 127
	"""
	Finds size of an value.
	"""
	if not x:
		return var.BYTE
	tmp = 1
	if x < 0:
		x = (-x << 1) - 2
	elif forge_signed:
		x <<= 1
	if x > 0xFFFF_FFFF:
		raiseError("Overflow Error", "This assembler is created only for 32 bit mode.")
	while x:
		x >>= 8
		tmp <<= 1
	return var.DWORD if (tmp == 6 and stay_align) else tmp


def splitWithoutSpecs(x: str) -> list[str]:
	retu: list[str] = []
	tmp = ""
	include = True
	for char in x:
		if char in '"()':
			include = not include
			tmp += char
		elif char == " " and include:
			retu.append(tmp)
			tmp = ""
		else:
			tmp += char
	return retu


# $, $$, (<compution>), 0x<hex>, <decimal>, 0b<bin>, ?, &<name>, '<char>'
# process(v, s, n)	-> zeroExtend(toHex(v, s), s, n)
# memProc(v, s)		-> reverse(splitBytes(process(v, s, False)))
def memoryProc(x: int, size: int) -> list[str]:
	tmp = splitBytes(zeroExtend(toHex(x, size), size, False))
	tmp.reverse()
	return tmp


def getRegister(x: str) -> tuple[int, int]:
	"""
	Returns Register values -> (index, size).
	>>> getRegister("eax")
	(0, var.DWORD)
	"""

	tmp = var.str_regs.index(x[-2:])
	return (
		tmp % var.REG_INDEX_LEN,
		var.DWORD
		if len(x) == 3
		else (var.BYTE if tmp < var.REG_INDEX_LEN else var.WORD),
	)


def outline_part1(size: int, bias: int) -> list[str]:
	"""
	Returns one of basic instruction command part.
	>>> outline_part1(var.DWORD, 0xF0)
	["66", "F1"]
	>>> outline_part1(var.WORD, 0xF0)
	["F1"]
	>>> outline_part1(var.BYTE, 0xF0)
	["F0"]
	"""
	retu: list[str] = []
	# size = var.sizes[size] if type(size) == str else size
	if size == var.DWORD:
		retu.append(var.STR_BIT_32)
	retu.append(hex(bias + (size != var.BYTE))[2:])
	return retu


def command_template(split: list[str], *args: Any) -> list[str]:
	"""
	>>> command_template(["eax"], 0xD0, 0xF6, "16")
	[outline_part1(var.DWORD, 0xF6), 0xD0 + 0]
	"""
	tmp = len(split) == 1
	if tmp and split[0][0].isalpha():
		index_, size_ = getRegister(split[0])
		return outline_part1(size_, args[1]) + [hex(args[0] + index_)[2:]]
	value_, size_ = (split[0], var.WORD) if tmp else (split[1], var.sizes[split[0]])
	return (
		outline_part1(size_, args[1])
		+ [args[2]]
		+ memoryProc(convertInt(value_[1:]), var.WORD)
	)


if __name__ == "__main__":  # Test functions.
	var.orgin = 0x10
	var.addr = 0x20

	print(f"{var.colors.DARK}toInt\t\t{var.colors.ENDL}", toInt("0x7c00", False))
	print(f"{var.colors.DARK}_calculate\t\t{var.colors.ENDL}", _calculate("3 - 4 + 6"))
	print(
		f"{var.colors.DARK}convertInt\t\t{var.colors.ENDL}", convertInt("(20 - $ + $$)")
	)
	print(f"{var.colors.DARK}splitBytes\t\t{var.colors.ENDL}", splitBytes("012345"))
	print(
		f"{var.colors.DARK}zeroExtend\t\t{var.colors.ENDL}",
		zeroExtend("0x32", var.DWORD, False),
	)
	print(f"{var.colors.DARK}toHex\t\t{var.colors.ENDL}", toHex(-1))
	print(f"{var.colors.DARK}findSize\t\t{var.colors.ENDL}", findSize(-192))
	print(
		f"{var.colors.DARK}splitWithoutSpecs\t\t{var.colors.ENDL}",
		splitWithoutSpecs('a b c "a b c" (4 + 3)'),
	)
	print(
		f"{var.colors.DARK}memoryProc\t\t{var.colors.ENDL}", memoryProc(100, var.WORD)
	)
	print(f"{var.colors.DARK}getRegister\t\t{var.colors.ENDL}", getRegister("si"))
	print(
		f"{var.colors.DARK}outline_part1\t\t{var.colors.ENDL}",
		outline_part1(var.WORD, 0x40),
	)
	print(
		f"{var.colors.DARK}command_template\t\t{var.colors.ENDL}",
		command_template(["si"], 0xD0, 0xF6, "16"),
	)

	raiseError("Exit Error", "Hello, world! (This is an test error.)", line=None)
