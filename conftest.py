import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth_module", "src"))

print(">>> CONFTEST LOADED, sys.path[0:3] =", __import__("sys").path[0:3])
