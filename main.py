# from collections.abc import Callable, Iterable, Mapping
import time

# from os import system
# from threading import Thread
# from typing import Any, Union

# system("cls")

start_t = time.time()

import variables as var
import functions as func  # type: ignore

test_case: list[str] = (
	# mov <register>, <constant>
	[f"mov {i}, 0x45" for i in var.regs8]
	+ [f"mov {i}, 0x4567" for i in var.regs16_32]
	+ [f"mov e{i}, 0x45670123" for i in var.regs16_32]
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
		"mov 0x10000",  # size = dword
		"mov dword *0x1234, 0x10000",
	]
)

# for _sub in var.test_cases:
# 	test_case += _sub

TClen = len(test_case)
_disable = False  # defines is the instruction gonna be runned.

var.settings.mode(
	20, False, False, False
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
	retu: list[str] = []
	if value1[0] == "*":
		pass
	else:
		tmp = func.getRegister(value1)
		if value2[0].isalpha():
			pass # reg, reg
		else:
			pass # reg, const
	return retu
"""


def procCase(_case: str) -> list[str] | None:
	pass


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
	if test_case[0].startswith("0rg"):
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
				func.zeroExtend(hex(index), notation=False) + var.colors.DARK,
				("" if not retu else func.zeroExtend(hex(var.addr), var.WORD, False))
				+ ("" if _disable else var.colors.ENDL)
				+ "\t",
				case_,
				end=var.colors.ENDL,
			)
			if not retu:
				print()
			else:
				print(
					" " * (var.settings.tab_size - len(case_)) + var.colors.DARK,
					("" if retu[0] == var.STR_BIT_32 else "   ")
					+ " ".join(retu)
					+ var.colors.ENDL,
				)
		if retu:
			var.addr += len(retu)
			var.memory += retu
		index += 1

	print("\nSize:", len(var.memory))
	print(f"Time(μs): {(time.time() - start_t) * 1_000_000:,.0f}")
	print(var.colors.DARK + " ".join(var.memory))
	print(var.constants, var.colors.ENDL)
