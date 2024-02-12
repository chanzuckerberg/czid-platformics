"""
GraphQL enums

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/support/enums.py.j2 instead.
"""

import strawberry
import enum


@strawberry.enum
class FileStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"


@strawberry.enum
class FileAccessProtocol(enum.Enum):
    s3 = "s3"


@strawberry.enum
class FileUploadClient(enum.Enum):
    browser = "browser"
    cli = "cli"
    s3 = "s3"
    basespace = "basespace"


@strawberry.enum
class NucleicAcid(enum.Enum):
    RNA = "RNA"
    DNA = "DNA"


@strawberry.enum
class SequencingProtocol(enum.Enum):
    ampliseq = "ampliseq"
    artic = "artic"
    artic_v3 = "artic_v3"
    artic_v4 = "artic_v4"
    artic_v5 = "artic_v5"
    combined_msspe_artic = "combined_msspe_artic"
    covidseq = "covidseq"
    midnight = "midnight"
    msspe = "msspe"
    snap = "snap"
    varskip = "varskip"
    easyseq = "easyseq"


@strawberry.enum
class SequencingTechnology(enum.Enum):
    Illumina = "Illumina"
    Nanopore = "Nanopore"


@strawberry.enum
class TaxonLevel(enum.Enum):
    level_subspecies = "level_subspecies"
    level_species = "level_species"
    level_genus = "level_genus"
    level_family = "level_family"
    level_order = "level_order"
    level_class = "level_class"
    level_phylum = "level_phylum"
    level_kingdom = "level_kingdom"
    level_superkingdom = "level_superkingdom"


@strawberry.enum
class PhylogeneticTreeFormat(enum.Enum):
    newick = "newick"
    auspice_v1 = "auspice_v1"
    auspice_v2 = "auspice_v2"


@strawberry.enum
class BulkDownloadType(enum.Enum):
    concatenate = "concatenate"
    zip = "zip"


@strawberry.enum
class HostOrganismCategory(enum.Enum):
    human = "human"
    insect = "insect"
    non_human_animal = "non_human_animal"
    unknown = "unknown"


@strawberry.enum
class IndexTypes(enum.Enum):
    nt = "nt"
    nt_loc = "nt_loc"
    nt_info = "nt_info"
    nr = "nr"
    nr_loc = "nr_loc"
    lineage = "lineage"
    accession2taxid = "accession2taxid"
    deuterostome = "deuterostome"
    taxon_blacklist = "taxon_blacklist"
    minimap2_long = "minimap2_long"
    minimap2_short = "minimap2_short"
    diamond = "diamond"
    star = "star"
    bowtie2 = "bowtie2"
    bowtie2_v2 = "bowtie2_v2"
    minimap2_dna = "minimap2_dna"
    minimap2_rna = "minimap2_rna"
    hisat2 = "hisat2"
    kallisto = "kallisto"
    original_transcripts_gtf = "original_transcripts_gtf"
