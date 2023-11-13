version 1.1

workflow simple_workflow {
    input {
        File fastq_0
        String docker_image_id
    }

    call RunSimpleTask {
        input:
        fastq_0 = fastq_0,
        docker_image_id = docker_image_id
    }

    output {
        File line_count = RunSimpleTask.line_count
    }
}

task RunSimpleTask {
    input {
        File fastq_0
        String docker_image_id
    }

    command <<<
        cat "~{fastq_0}" | wc -l > line_count.txt
    >>>

    output {
        File line_count = "line_count.txt"
    }

    runtime {
        docker: docker_image_id
    }
}
