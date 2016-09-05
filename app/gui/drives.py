from kivy.utils import platform


def get_drives():

    def get_win_drives():
        import win32api

        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]

        return drives

    def get_linux_drives():
        return []

    def get_mac_drives():
        return []

    def switch(case):
        return {'win': get_win_drives(),
                'linux': get_linux_drives(),
                'macosx': get_mac_drives()}[case]

    return switch(platform)
