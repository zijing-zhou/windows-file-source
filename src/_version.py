__version__ = "0.0.1"

VERSION_INFO = {
    "major": 0,
    "minor": 0,
    "patch": 1,
    "release_level": "final",  # "alpha", "beta", "rc", "final"
    "serial": 0,  # serial number for releases
    "dev": None,  # development version number
}

VERSION_TUPLE = (
    VERSION_INFO["major"],
    VERSION_INFO["minor"],
    VERSION_INFO["patch"],
)

def get_version():
    version = "{}.{}.{}".format(*VERSION_TUPLE)
    
    if VERSION_INFO["release_level"] != "final":
        version += f"-{VERSION_INFO['release_level']}"
        if VERSION_INFO["serial"] > 0:
            version += str(VERSION_INFO["serial"])
    
    if VERSION_INFO["dev"]:
        version += f".dev{VERSION_INFO['dev']}"
    
    return version

def get_version_tuple():
    return VERSION_TUPLE

def get_version_info():
    return VERSION_INFO.copy()
