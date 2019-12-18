class bcolors:
    ERROR = '\033[91m'
    SUCCESS = '\033[92m'
    WARNING = '\033[33m'
    PROGRESS = '\033[34m'
    END = '\033[0m'

def printERR_MSG(msg):
    print(bcolors.ERROR+msg+bcolors.END)

def printWARN_MSG(msg):
    print(bcolors.WARNING+msg+bcolors.END)

def printSuccessMSG(msg):
    print(bcolors.SUCCESS+msg+bcolors.END)


def printProgressMSG(msg):
    print(bcolors.PROGRESS+msg+bcolors.END)
