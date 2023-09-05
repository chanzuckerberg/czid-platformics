version 1.1

workflow first_sequence {
    input {
        File sequences
    }

    call get_first_id {
        input:
        sequences = sequences,
    }

    call get_first_sequence {
        input:
        sequences = sequences,
    }

    output {
        String id = get_first_id.id
        String sequence = get_first_sequence.sequence
    }
}

task get_first_id {
    input {
        File sequences
    }

    command <<<
        head -n 1 ~{sequences}
    >>>

    output {
        String id = stdout()
    }

    runtime {
        docker: "ubuntu"
    }
}


task get_first_sequence {
    input {
        File sequences
    }

    command <<<
        head -n 2 ~{sequences} | tail -n 1
    >>>

    output {
        String sequence = stdout()
    }

    runtime {
        docker: "ubuntu"
    }
}

