import os, sys
from cx_Freeze import setup, Executable



addtional_mods = ['numpy.core._methods', 'numpy.lib.format']
setup (name = "csvProject1",
	version= "0.2",
	description = "Parse file for Irish users. Remove whitespace and convert delimiters",
	 options = {'build_exe': {'includes': addtional_mods}},
	executables =[Executable(script = "csvProject1.py")])