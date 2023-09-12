version 1.1

workflow contig_squared {
    input {
        String sequence
        Int n_contigs = 10
    }

    scatter(i in range(n_contigs)) {
        call repeat_sequence_contig {
            input:
            sequence=sequence,
            n = n_contigs,
        }
    }

    output {
        String contigs = repeat_sequence_contig.contig[0]
    }
}

task repeat_sequence_contig {
    input {
        String sequence
        Int n
    }

    command <<<
    for i in {1..~{n}}; do
        echo -n ~{sequence} >> contig.fa
    done

    >>>

    output {
        String contig = read_string("contig.fa")
    }

    runtime {
        docker: "ubuntu"
    }
}
