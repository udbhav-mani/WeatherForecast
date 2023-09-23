import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import logging
from helpers.entry import Entry

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


entry = Entry()
entry.entry()
