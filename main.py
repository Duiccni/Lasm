# from collections.abc import Callable, Iterable, Mapping
import time

# from os import system
# from threading import Thread
# from typing import Any, Union

# system("cls")

start_t = time.time()

import variables as var
import functions as func # type: ignore

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
