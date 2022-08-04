from distutils.core import setup, Extension

module = Extension("c_os", sources = ["c_os.c"])

setup(
    name = "c_os",
    version = "1.0",
    description = "Is true file and directory functions in c.",
    ext_modules = [module]
    )
