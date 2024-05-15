from Foundation.SystemManager import SystemManager


sys_types = [

]

for sys_type in sys_types:
    SystemManager.addSystemType(sys_type.__name__, sys_type)
    pass
