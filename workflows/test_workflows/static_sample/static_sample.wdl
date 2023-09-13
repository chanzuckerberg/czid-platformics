version 1.1

workflow static_sample {
    input {}

    call echo as echo_name {
        input:
        str = "My Sample",
    }

    call echo as echo_locaton {
        input:
        str = "Mars",
    }

    output {
        String name = echo_name.out
        String location = echo_locaton.out
    }
}

task echo {
    input {
        String str
    }

    command <<<
        echo ~{str}
    >>>

    output {
        String out = stdout()
    }

    runtime {
        docker: "ubuntu"
    }
}
