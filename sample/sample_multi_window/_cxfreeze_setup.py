from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'gui'

executables = [
    Executable('main.py', base=base, target_name = 'sample_multi_window.exe')
]

setup(name='sample_multi_window',
      version = '1.0',
      description = 'sample_multi_window',
      options = {'build_exe': build_options},
      executables = executables)
