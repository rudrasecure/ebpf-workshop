#!/usr/bin/python3

from bcc import BPF
from time import sleep

bpf_source = '''

#include <linux/sched.h>



int sys_enter_openat_fn() {
    u32 pid = (u32)(bpf_get_current_pid_tgid() >> 32);
    bpf_trace_printk("openat was fired by process %d\\n", pid);
    return 0;
}

'''

bpf = BPF(text=bpf_source,  cflags=["-Wno-macro-redefined"])
bpf.attach_tracepoint(tp="syscalls:sys_enter_openat", fn_name="sys_enter_openat_fn")

sleep(10)