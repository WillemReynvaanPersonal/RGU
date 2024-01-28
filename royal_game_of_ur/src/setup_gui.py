from cx_Freeze import setup, Executable

base = None

executables = [Executable("rgu_gui.py", base=base)]

packages = ["idna"]

options = {'build_exe': {'packages':packages, 'includes':['numpy.core._methods',
                                                          'numpy.lib.format']}, }

setup(
    name="RGU_GUI_EXE",
    options = options,
    version = "0.1",
    description = "any description",
    executables = executables)