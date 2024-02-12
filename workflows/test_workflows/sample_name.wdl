version 1.1

workflow simple_workflow {
    input {
        String sample_name
    }

    call RunSimpleTask {
        input:
        sample_name = sample_name
    }

    output {
        File new_sample_name = RunSimpleTask.new_sample_name
    }
}

task RunSimpleTask {
    input {
        String sample_name
    }

    command <<<
        echo ~{sample_name}1 > output.txt
    >>>

    output {
        File new_sample_name = "output.txt"
    }

    runtime {
        docker: "ubuntu:latest"
    }
}
