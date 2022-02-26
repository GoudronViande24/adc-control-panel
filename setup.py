from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'Console'

executables = [
    Executable('main.py', base=base, target_name = 'adccp')
]

setup(name='ADC Control Panel',
      version = '1.0',
      description = 'Simple terminal-based application to monitor some stuff',
      options = {'build_exe': build_options},
      executables = executables)
