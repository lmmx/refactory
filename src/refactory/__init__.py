r"""
:mod:`refactory` is a refactory utility with patterns composed of validated AST rules"""

from . import patterns
from .spec import load_spec

__all__ = ["spec", "patterns"]

__author__ = "Louis Maddox"
__license__ = "MIT"
__description__ = "Refactor utility with patterns composed of validated AST rules."
__url__ = "https://github.com/lmmx/refactory"
__uri__ = __url__
__email__ = "louismmx@gmail.com"
