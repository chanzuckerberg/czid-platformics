import typing
from typing import Annotated, Any, Optional
import strawberry







@strawberry.type
class HostOrganismGroupByOptions:
    name: Optional[str] = None
    version: Optional[str] = None

@strawberry.type
class SampleGroupByOptions:
    collection_id: Optional[int] = None
    collection_location: Optional[str] = None
    host_organism: Optional[HostOrganismGroupByOptions] = None

@strawberry.type
class SequencingReadGroupByOptions:
    collection_id: Optional[int] = None
    sample: Optional[SampleGroupByOptions] = None

@strawberry.type
class ConsensusGenomeGroupByOptions:
    collection_id: Optional[int] = None
    # created_at: Optional[datetime.datetime] = None
    sequence_read: Optional[SequencingReadGroupByOptions] = None

def build_consensus_genome_group_by_output(group_object: Optional[ConsensusGenomeGroupByOptions], keys: list[str], value: Any) -> ConsensusGenomeGroupByOptions:
    """
    Given a list of group by keys, build a nested object to represent the group by clause
    """
    if not group_object:
        group_object = ConsensusGenomeGroupByOptions()
    
    key = keys.pop(0)
    if key == "sequence_read":
        if getattr(group_object, key):
            value = build_sequencing_read_group_by_output(getattr(group_object, key), keys, value)
        else:
            value = build_sequencing_read_group_by_output(None, keys, value)
    # Add more cases for other nested 1:1 relationships
    
    setattr(group_object, key, value)
    return group_object

def build_sequencing_read_group_by_output(group_object: Optional[SequencingReadGroupByOptions], keys: list[str], value: Any) -> SequencingReadGroupByOptions:
    """
    Given a list of group by keys, build a nested object to represent the group by clause
    """
    if not group_object:
        group_object = SequencingReadGroupByOptions()
    
    key = keys.pop(0)
    if key == "sample":
        if getattr(group_object, key):
            value = build_sample_group_by_output(getattr(group_object, key), keys, value)
        else:
            value = build_sample_group_by_output(None, keys, value)
    
    setattr(group_object, key, value)
    return group_object

def build_sample_group_by_output(group_object: Optional[SampleGroupByOptions], keys: list[str], value: Any) -> SampleGroupByOptions:
    """
    Given a list of group by keys, build a nested object to represent the group by clause
    """
    if not group_object:
        group_object = SampleGroupByOptions()
    
    key = keys.pop(0)
    if key == "host_organism":
        if getattr(group_object, key):
            value = build_host_organism_group_by_output(getattr(group_object, key), keys, value)
        else:
            value = build_host_organism_group_by_output(None, keys, value)
    
    setattr(group_object, key, value)
    return group_object

def build_host_organism_group_by_output(group_object: Optional[HostOrganismGroupByOptions], keys: list[str], value: Any) -> HostOrganismGroupByOptions:
    """
    Given a list of group by keys, build a nested object to represent the group by clause
    """
    if not group_object:
        group_object = HostOrganismGroupByOptions()
    
    key = keys.pop(0)
    
    setattr(group_object, key, value)
    return group_object