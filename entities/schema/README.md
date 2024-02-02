```mermaid
erDiagram
Entity {
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
File {
    uuid id  
    string entity_field_name  
    FileStatus status  
    FileAccessProtocol protocol  
    string namespace  
    string path  
    string file_format  
    string compression_type  
    int size  
    FileUploadClient upload_client  
    string upload_error  
}
Sample {
    int rails_sample_id  
    string name  
    string sample_type  
    boolean water_control  
    date collection_date  
    string collection_location  
    string notes  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
SequencingRead {
    SequencingProtocol protocol  
    SequencingTechnology technology  
    NucleicAcid nucleic_acid  
    boolean clearlabs_export  
    string medaka_model  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
GenomicRange {
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
ReferenceGenome {
    string accession_id  
    string accession_name  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
HostOrganism {
    string name  
    string version  
    HostOrganismCategory category  
    boolean is_deuterostome  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
Metadatum {
    string field_name  
    string value  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
ConsensusGenome {
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
MetricConsensusGenome {
    float reference_genome_length  
    float percent_genome_called  
    float percent_identity  
    float gc_percent  
    int total_reads  
    int mapped_reads  
    int ref_snps  
    int n_actg  
    int n_missing  
    int n_ambiguous  
    float coverage_depth  
    float coverage_breadth  
    float coverage_bin_size  
    int coverage_total_length  
    2dArrayInt coverage_viz  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
Taxon {
    string wikipedia_id  
    string description  
    string common_name  
    string name  
    boolean is_phage  
    string upstream_database_identifier  
    TaxonLevel level  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
UpstreamDatabase {
    string name  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
IndexFile {
    IndexTypes name  
    string version  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
PhylogeneticTree {
    PhylogeneticTreeFormat format  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
BulkDownload {
    BulkDownloadType download_type  
    uuid entity_id  
    uuid id  
    int producing_run_id  
    int owner_user_id  
    int collection_id  
    date created_at  
    date updated_at  
    date deleted_at  
}
EntityMixin {
    uuid entity_id  
}

File ||--|| Entity : "entity"
Sample ||--|o HostOrganism : "host_organism"
Sample ||--}o SequencingRead : "sequencing_reads"
Sample ||--}o Metadatum : "metadatas"
SequencingRead ||--|o Sample : "sample"
SequencingRead ||--|o File : "r1_file"
SequencingRead ||--|o File : "r2_file"
SequencingRead ||--|o Taxon : "taxon"
SequencingRead ||--|o GenomicRange : "primer_file"
SequencingRead ||--|o ReferenceGenome : "reference_sequence"
SequencingRead ||--}o ConsensusGenome : "consensus_genomes"
GenomicRange ||--|o File : "file"
GenomicRange ||--}o SequencingRead : "sequencing_reads"
ReferenceGenome ||--|o File : "file"
ReferenceGenome ||--}o SequencingRead : "sequencing_reads"
HostOrganism ||--}o IndexFile : "indexes"
HostOrganism ||--|o File : "sequence"
HostOrganism ||--}o Sample : "samples"
Metadatum ||--|| Sample : "sample"
ConsensusGenome ||--|| Taxon : "taxon"
ConsensusGenome ||--|| SequencingRead : "sequence_read"
ConsensusGenome ||--|o File : "sequence"
ConsensusGenome ||--|o MetricConsensusGenome : "metrics"
ConsensusGenome ||--|o File : "intermediate_outputs"
MetricConsensusGenome ||--|| ConsensusGenome : "consensus_genome"
Taxon ||--|| UpstreamDatabase : "upstream_database"
Taxon ||--|o Taxon : "tax_parent"
Taxon ||--|o Taxon : "tax_subspecies"
Taxon ||--|o Taxon : "tax_species"
Taxon ||--|o Taxon : "tax_genus"
Taxon ||--|o Taxon : "tax_family"
Taxon ||--|o Taxon : "tax_order"
Taxon ||--|o Taxon : "tax_class"
Taxon ||--|o Taxon : "tax_phylum"
Taxon ||--|o Taxon : "tax_kingdom"
Taxon ||--|o Taxon : "tax_superkingdom"
Taxon ||--}o ConsensusGenome : "consensus_genomes"
Taxon ||--}o SequencingRead : "sequencing_reads"
UpstreamDatabase ||--}o Taxon : "taxa"
UpstreamDatabase ||--}o IndexFile : "indexes"
IndexFile ||--|| File : "file"
IndexFile ||--|o UpstreamDatabase : "upstream_database"
IndexFile ||--|o HostOrganism : "host_organism"
PhylogeneticTree ||--|o File : "tree"
BulkDownload ||--|o File : "file"

```

