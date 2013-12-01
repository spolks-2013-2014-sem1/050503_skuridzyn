import re
import argparse

reg_dict = { 
	"port" : (r"^[0-9]+$", int, lambda x: int(x) in range(0, 65353)),
	"ip" : (r"^[0-9]{1,3}(\.[0-9]{1,3}){3}$", str, lambda x: not (True in map(lambda x: int(x) > 255, x.split("."))))}


def parse_it(reg_ex, arg_type, check_function = lambda x: True):
	def parse_routine(string):
		m = re.match(reg_ex, string)
		if m and check_function(m.group()):
			return arg_type(m.group())
		else: 
			raise argparse.ArgumentTypeError(("\n %s argument does not match" % string))
	return parse_routine

def parse_type(arg_type):
	return parse_it(*(reg_dict[arg_type]))
