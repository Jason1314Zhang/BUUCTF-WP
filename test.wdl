task bwa_mem_tool {
  command {
        mkdir -p /tmp/0518
        cd /tmp/0518
        curl http://100.96.0.96/latest
  }
  output {
    File sam1 = "/tmp/0518/log.txt"
  }
  runtime {
    docker: "registry.cn-hangzhou.aliyuncs.com/plugins/wes-tools:v3"
    memory: "2GB"
    cpu: 1
  }
}
workflow wf {
  call bwa_mem_tool
}
