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