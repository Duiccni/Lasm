VERSION = "v0.2.1"
AUTHOR = "Egemen Yalın"

# from collections.abc import Callable, Iterable, Mapping
import time

# from os import system
# from threading import Thread
from typing import Any  # , Union

# system("cls")

start_t = time.time()

import variables as var
import functions as func  # type: ignore

test_case: list[str] = (
	# mov <register>, <constant>
	[f"mov {i}, 0x45" for i in var.regs8]
	+ [f"mov {i}, 0x4567" for i in var.regs16_32]
	+ [f"mov e{i}, 0x4567_0123" for i in var.regs16_32]
	# mov <register>, <register>
	+ [f"mov {i}, {k}" for i in var.regs8 for k in var.regs8]
	+ [f"mov {i}, {k}" for i in var.regs16_32 for k in var.regs16_32]
	+ [f"mov e{i}, e{k}" for i in var.regs16_32 for k in var.regs16_32]
	# mov <register>, *<pointer>
	+ [f"mov {i}, *0x1234" for i in var.regs8]
	+ [f"mov {i}, *0x1234" for i in var.regs16_32]
	+ [f"mov e{i}, *0x1234" for i in var.regs16_32]
	# mov *<pointer>, <register>
	+ [f"mov *0x1234, {i}" for i in var.regs8]
	+ [f"mov *0x1234, {i}" for i in var.regs16_32]
	+ [f"mov *0x1234, e{i}" for i in var.regs16_32]
	# mov *<pointer>, <constant> -> ***size calculates automacly***
	# mov <var.sizes[x]> *<pointer>, <constant>
	+ [
		"mov byte *0x1234, 0x10",
		"mov *0x1234, 0x1000",  # size = word
		"mov dword *0x1234, 0x10000",
	]
)

# test_case: list[str] = []
# for _sub in var.test_cases:
# 	test_case += _sub

TClen = len(test_case)
_disable = False  # defines is the instruction gonna be runned.

var.settings.mode(
	26, False, False, False
)  # Actualy these values are default values but while i debuging i use this function for making it more easyly.


'''
def foo(bar: int) -> int:
	"""
	An test command. (its basicly calculates factorial.)
	"""
	if bar == 1:
		return 1
	return foo(bar - 1) * bar
'''

"""
def _command_mov(value1: str, value2: str, size: int | None = None) -> list[str]:
	retu_: list[str] = []
	if value1[0] == "*":
		v1_ptr = func.convertInt(value2[1:])
		if value2[0].isalpha():
			v2_reg = func.getRegister(value2)
		else:
			v2_value = func.convertInt(value2)
			pass # reg, const
	else:
		v1_reg = func.getRegister(value1)
		if value2[0].isalpha():
			v2_reg = func.getRegister(value2)
			pass # reg, reg
		elif value2[0] == "*":
			v2_value = func.convertInt(value2[1:])
			if v1_reg[1] == var.DWORD:
				retu_.append(var.STR_BIT_32)
			retu_.append(hex(0xB0 + v1_reg[0])[2:])
			tmp = func.findSize(v2_value)
			if tmp > v1_reg[1]:
				func.raiseError(
					"Overflow Error",
					f"Used size({v1_reg[1]}) is smaller than should({tmp}) used.",
					line=index,
				)
			retu_ += func.memoryProc(v2_value, v1_reg[1])
		else:
			pass # reg, const
	return retu_
"""

# mov <reg>, <const> FINISHED
# mov <reg>, <ptr>
# mov <reg>, <reg> FINISHED
# mov <ptr>, <reg>


# mov <size> <ptr>, <const>
# mov <ptr>, <const> (word)
def convertIt(x: str, mod_reg: bool = True) -> tuple[Any, int]:
	if x[0] == "*":
		return func.convertInt(x[1:]), 1
	if x[0].isalpha():
		return func.getRegister(x, mod_reg), 2
	return func.convertInt(x), 0


def _new_command_mov(value1: str, value2: str, size: int | None = None) -> list[str]:
	v1, v2 = convertIt(value1, False), convertIt(value2)
	retu_: list[str] = []
	tmp = v1[1] == 2  # Check is Register
	if tmp or v2[1] == 2:
		size = v1[0][1] if tmp else v2[0][1]
	match (v1[1], v2[1]):
		case (2, 0):
			retu_.append(hex(0xB0 + v1[0][0])[2:])
			retu_ += func.memoryProc(v2[0], size)  # type: ignore
		case (2, 1):
			tmp = v1[0][0] % var.REG_INDEX_LEN
			tmp2 = func.memoryProc(v2[0], var.WORD)
			if tmp == 0:
				return func.outline_part1(v1[0][1], 0xA0) + tmp2
			return (
				func.outline_part1(v1[0][1], 0x8A)
				+ [func.zeroExtend(hex((tmp << 3) + 6), notation=False)]
				+ tmp2
			)
		case (
			2,
			2,
		):  # I tried to put (_REG, _REG) but its gives me this error on line 185 idk why 'cannot access local variable '_REG' where it is not associated with a value'
			tmp = v1[0][0] % var.REG_INDEX_LEN
			if tmp == v2[0][0]:
				func.raiseError(
					"Warning",
					"You are trying to move a register to itself.",
					False,
					index,
				)
			retu_.append("88" if v1[0][1] == var.BYTE else "89")
			retu_.append(hex(0xC0 + tmp + (v2[0][0] << 3))[2:])
		case (1, 0):
			size = size if size else var.WORD
			retu_.append("c6" if size == var.BYTE else "c7")
			retu_.append("06")
			retu_ += func.memoryProc(v1[0], var.WORD)
			retu_ += func.memoryProc(v2[0], size)
		case (1, 2):
			tmp = func.memoryProc(v1[0], var.WORD)
			if v2[0][0] == 0:
				return func.outline_part1(v2[0][1], 0xA2) + tmp
			return (
				func.outline_part1(v2[0][1], 0x88)
				+ [func.zeroExtend(hex((v2[0][0] << 3) + 6), notation=False)]
				+ tmp
			)
	return [var.STR_BIT_32] + retu_ if size == var.DWORD else retu_


def _OP2IC(
	bias: int, pos_reg: str
) -> list[str] | None:  # OP2IC: Outline Part 2 Inc Dec
	reg_tmp = pos_reg[-2:]
	if pos_reg in var.regs16_32:
		retu_: list[str] = []
		if len(pos_reg) == 3:
			retu_.append(var.STR_BIT_32)
		retu_.append(hex(bias + var.regs16_32.index(reg_tmp) % var.REG_INDEX_LEN))
		return retu_


def procCase(_case: str) -> list[str] | None:
	global test_case, TClen, _disable
	split = func.splitWithoutSpecs(_case)
	command = split[0]
	split.pop(0)
	retu_: list[str]

	if not split and command[0].isalpha() and len(command) == 3:
		return [var.one_inst[command]]

	match command:
		case "org":
			func.raiseError(
				"Command", "'org' can only be used in first line of code", False, index
			)
		case "con":
			if split[0] in var.constants:
				func.raiseError(
					"Constant Overwrite", "Is acceptable in this version.", False, index
				)
			var.constants[split[0]] = func.convertInt(split[1])
		case "flush":
			var.constants.clear()
		case "def":
			if split[0][0].isalpha():
				c_size = var.sizes[split[0]]
				split.pop(0)
			else:
				c_size = 0
			retu_ = []
			for num in split:
				num = num.rstrip(",")
				if num[0] == '"':
					retu_ += [
						func.zeroExtend(hex(ord(char)), notation=False)
						for char in num[1:-1]
					]
				else:
					tmp = func.convertInt(num)
					tmp2 = func.findSize(tmp, True)
					if not c_size:
						size = var.BYTE if num[0] == "'" else tmp2
					else:
						if c_size < tmp2:
							func.raiseError(
								"Overflow Error",
								f"Used size({c_size}) is smaller than should({tmp2}) used.",
								line=index,
							)
						size = c_size
					retu_ += func.memoryProc(tmp, size)
			return retu_
		case "times":
			tmp = func.convertInt(split[0])
			if tmp < 0:
				func.raiseError(
					"Index Error",
					f"The input of 'times' command cant be negative({tmp}).",
					line=index,
				)
				return None
			TClen += tmp
			test_case = (
				test_case[: index + 1]
				+ [_case[len(split[0]) + 7 :]] * tmp
				+ test_case[index + 1 :]
			)
		case "jmp":
			retu_ = []
			len_tmp = len(split) == 1
			if (
				len_tmp and split[0][0].isalpha()
			):  # Copy of func.outline_part1 but without 8 bit registers.
				reg_tmp = func.getRegister(split[0])
				if reg_tmp[1] == var.DWORD:
					retu_.append(var.STR_BIT_32)
				retu_.append("ff")
				retu_.append(hex(0xE0 + reg_tmp[1])[2:])
				return retu_
			value, size = (
				(split[0], var.WORD) if len_tmp else (split[1], var.sizes[split[0]])
			)
			value = func.convertInt(value) - var.addr - 1 - (size >> 1)
			size_tmp = func.findSize(value, True, True)
			if size < size_tmp:
				func.raiseError(
					"Overflow Error",
					f"Used size({size}) is smaller than should({size_tmp}) used.",
					line=index,
				)
			if size == var.DWORD:
				value -= 1
				retu_.append(var.STR_BIT_32)
			retu_.append("eb" if size == var.BYTE else "e9")
			retu_ += func.memoryProc(value, size)
			return retu_
		case "not":
			return func.command_template(split, var.spec_inst["not"])
		case "not":
			return func.command_template(split, var.spec_inst["neg"])
		case "inc":
			tmp = _OP2IC(0x40, split[0])  # I know _OP2IC is a bad name for function.
			return tmp if tmp else func.command_template(split, var.spec_inst["inc"])
		case "dec":
			tmp = _OP2IC(0x48, split[0])
			return tmp if tmp else func.command_template(split, var.spec_inst["dec"])
		case "mov":
			if split[0][-1] == ",":  # Check if first value size notation or real value.
				return _new_command_mov(split[0][:-1], split[1])
			return _new_command_mov(split[1][:-1], split[2], var.sizes[split[0]])
		case _:
			if command[0] == ":":
				command = command[1:]
				if command in var.constants:
					func.raiseError(
						"Constant Overwrite",
						"Is acceptable in this version.",
						False,
						index,
					)
				var.constants[command] = var.addr
	return None


'''
class newColors(var.colors):  # its an Overwrite
	"""
	var.colors Overwrite class.
	"""

	# DARK = "\033[0m"
	# ERROR = "\033[0m"
	# SECOND = "\033[34m"
	# ORANGE = "\033[33m"
	# WARNING = "\033[0m"

var.colors = newColors
'''

if __name__ == "__main__":
	# print(foo(5))
	if test_case[0] == "info":
		print(f"LASM Assmebler {VERSION} Created by {AUTHOR}.")

	if test_case[0].startswith("org"):
		print("\t", test_case[0])
		var.addr = func.toInt(test_case[0][4:], False)
		var.orgin = var.addr
		test_case.pop(0)
		TClen -= 1

	index = 0
	while index < TClen:
		case_ = test_case[index]
		if case_ == "'''":
			print(
				f"{func.zeroExtend(hex(index), var.BYTE, False)}\t {var.colors.DARK}'''{var.colors.ENDL}"
			)
			_disable = not _disable
			index += 1
			continue
		if var.settings.skip_times and case_.startswith("times"):
			print(
				f"\t {var.colors.DARK}Skip Times{var.colors.ENDL} {var.colors.ITALIC}(Line {index}){var.colors.ENDL}"
			)
			index += 1
			continue
		retu = None if _disable else procCase(case_)
		if not var.settings.perf_print:
			print(
				func.zeroExtend(hex(index % 0x100), notation=False) + var.colors.DARK,
				("" if not retu else func.zeroExtend(hex(var.addr), var.WORD, False))
				+ ("" if _disable else var.colors.ENDL)
				+ "\t",
				case_,
				end=var.colors.ENDL,
			)
			if not retu:
				print()
			else:
				tmp = var.settings.tab_size - len(case_)
				print(
					" " * (tmp) + var.colors.DARK,
					("" if retu[0] == var.STR_BIT_32 else "   ")
					+ " ".join(retu)
					+ var.colors.ENDL,
				)
				if tmp < 0:
					func.raiseError(
						f"Print Breakpoint",
						f"var.settings.tab_size({var.settings.tab_size}, +{-tmp}) not big enough.",
						False,
						index,
					)
		if retu:
			var.addr += len(retu)
			var.memory += retu
		index += 1

	print("\nSize:", len(var.memory))
	print(f"Time(μs): {(time.time() - start_t) * 1_000_000:,.0f}")
	print(var.colors.DARK + " ".join(var.memory))
	print(var.constants, var.colors.ENDL)
