from typing import List
from plugin_types import Loader
from workflows.entity_interface import Sequence
from workflows.plugin_types import LoaderInputConstraint

class SequenceLoader(Loader):
    def constraints(self) -> List[LoaderInputConstraint]:
        return [LoaderInputConstraint("type", "sequence", None, None)]

    def load(self, sequence: str) -> List[List[Sequence]]:
        return [[Sequence(sequence)]]