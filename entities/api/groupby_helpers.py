import typing
from typing import TYPE_CHECKING, Annotated, Any, Optional, Sequence, Callable
import strawberry
import database.models as db

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.consensus_genome import ConsensusGenomeGroupByOptions
    from api.types.sequencing_read import SequencingReadGroupByOptions
    from api.types.sample import SampleGroupByOptions
    from api.types.host_organism import HostOrganismGroupByOptions
else:
    ConsensusGenomeGroupByOptions = strawberry.lazy("api.types.consensus_genome")
    SequencingReadGroupByOptions = strawberry.lazy("api.types.sequencing_read")
    SampleGroupByOptions = strawberry.lazy("api.types.sample")
    HostOrganismGroupByOptions = strawberry.lazy("api.types.host_organism")


@strawberry.type
class HostOrganismGroupByOptions:
    name: Optional[str] = None
    version: Optional[str] = None

def build_consensus_genome_group_by_output(group_object: Optional[ConsensusGenomeGroupByOptions], keys: list[str], value: Any) -> ConsensusGenomeGroupByOptions:
    """
    Given a list of group by keys, build a nested object to represent the group by clause
    """
    if not group_object:
        group_object = Annotated[ConsensusGenomeGroupByOptions, strawberry.type(name="ConsensusGenomeGroupByOptions")]
    
    key = keys.pop(0)
    if key == "sequence_read":
        value = build_sequencing_read_group_by_output(None, keys, value)
    # Add more cases for other nested 1:1 relationships
    
    setattr(group_object, key, value)
    return group_object

def build_sequencing_read_group_by_output(group_object: Optional[SequencingReadGroupByOptions], keys: list[str], value: Any) -> SequencingReadGroupByOptions:
    """
    Given a list of group by keys, build a nested object to represent the group by clause
    """
    if not group_object:
        group_object = Annotated[SequencingReadGroupByOptions, strawberry.type(name="SequencingReadGroupByOptions")]
    
    key = keys.pop(0)
    if key == "sample":
        value = build_sample_group_by_output(None, keys, value)
    
    setattr(group_object, key, value)
    return group_object

def build_sample_group_by_output(group_object: Optional[SampleGroupByOptions], keys: list[str], value: Any) -> SampleGroupByOptions:
    """
    Given a list of group by keys, build a nested object to represent the group by clause
    """
    if not group_object:
        group_object = Annotated[SampleGroupByOptions, strawberry.type(name="SampleGroupByOptions")]
    
    key = keys.pop(0)
    if key == "host_organism":
        value = build_host_organism_group_by_output(None, keys, value)
    
    setattr(group_object, key, value)
    return group_object

def build_host_organism_group_by_output(group_object: Optional[HostOrganismGroupByOptions], keys: list[str], value: Any) -> HostOrganismGroupByOptions:
    """
    Given a list of group by keys, build a nested object to represent the group by clause
    """
    if not group_object:
        # group_object = Annotated[HostOrganismGroupByOptions, strawberry.type(name="HostOrganismGroupByOptions")]
        group_object = HostOrganismGroupByOptions()
    
    key = keys.pop(0)
    
    setattr(group_object, key, value)
    return group_object