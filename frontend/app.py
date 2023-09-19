import logging
from helpers.entry import Entry
logging.basicConfig(filename='app.log',
                    format='%(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


entry = Entry()
entry.entry()
