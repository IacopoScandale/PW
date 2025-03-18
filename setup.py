from pw.data.strings import *
from setuptools import setup, find_packages


def get_requirements() -> list[str]:
  """
  Read from `requirements.txt` file and return the `install_requires` 
  list of setup() in setuptools
  """
  with open("requirements.txt", "r") as txt:
    lines: list[str] = txt.read().splitlines()
  # strip every line and remove commented ones:
  return [line.strip() for line in lines if not line.strip().startswith("#")]


setup(
  name=PACKAGE_NAME,
  author=AUTHOR,
  version=VERSION,
  license=LICENSE,
  description=DESCRIPTION,
  packages=find_packages(),
  install_requires=get_requirements(),
  entry_points={
    "console_scripts": [f"{MAIN_COMM_NAME}={PACKAGE_NAME}.cli:main"],
  },
)