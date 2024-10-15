# riscvflow/__init__.py

# Import key components of your package
from .cfg import ControlFlowGraph
from .RISCVControlFlowBuilder import RISCVControlFlowBuilder
from .traversals import dfsFunction, getFunctions, dfsVisited, listMacros, nestedFunctions, registerUsage
from .registers import all_registers
from .utils import build_trie

# You can also set up logging or configuration here if necessary
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("riscvflow package loaded successfully")
