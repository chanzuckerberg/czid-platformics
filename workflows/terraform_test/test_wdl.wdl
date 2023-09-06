version 1.0
workflow swipe_test {
  input {
    File hello
    String docker_image_id
  }

  call add_world {
    input:
      input_file = hello,
      docker_image_id = docker_image_id
  }

  call add_goodbye {
    input:
      input_file = add_world.out_world,
      docker_image_id = docker_image_id
  }

  call add_farewell {
    input:
      input_file = add_goodbye.out_goodbye,
      docker_image_id = docker_image_id
  }

  output {
    File out_world = add_world.out_world
    File out_goodbye = add_goodbye.out_goodbye
    File out_farewell = add_farewell.out_farewell
  }
}

task add_world {
  input {
    File input_file
    String docker_image_id
  }

  command <<<
    cat ~{input_file} > out_world.txt
    echo world >> out_world.txt
  >>>

  output {
    File out_world = "out_world.txt"
  }

  runtime {
      docker: docker_image_id
  }
}

task add_goodbye {
  input {
    File input_file
    String docker_image_id
  }

  command <<<
    cat ~{input_file} > out_goodbye.txt
    echo goodbye >> out_goodbye.txt
  >>>

  output {
    File out_goodbye = "out_goodbye.txt"
  }

  runtime {
      docker: docker_image_id
  }
}

task add_farewell {
  input {
    File input_file
    String docker_image_id
  }

  command <<<
    cat ~{input_file} > out_farewell.txt
    echo farewell >> out_farewell.txt
  >>>

  output {
    File out_farewell = "out_farewell.txt"
  }

  runtime {
      docker: docker_image_id
  }
}
