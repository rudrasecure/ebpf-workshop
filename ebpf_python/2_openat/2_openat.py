#!/usr/bin/python3

from bcc import BPF
from time import sleep

bpf_source = '''

#include <linux/sched.h>

// see /sys/kernel/debug/tracing/events/syscalls/sys_enter_openat

BPF_PERF_OUTPUT(events);

struct data_t {
    u32 pid;
    char comm[TASK_COMM_LEN];
    char filename[256];
};

struct sys_enter_openat_args_t {
    uint64_t _unused;

    u32 _nr;
    u64 dfd;
    char *filename;
    u64 flags;
    u64 mode;
};

int sys_enter_openat_fn(struct sys_enter_openat_args_t *args) {

    struct data_t data = {};
    u32 pid = (u32)(bpf_get_current_pid_tgid() >> 32);
    bpf_trace_printk("openat was fired by process %d\\n", pid);
    data.pid = pid;
    bpf_probe_read_str(data.filename, sizeof(data.filename), args->filename);
    bpf_get_current_comm(data.comm, TASK_COMM_LEN);
    
    events.perf_submit(args, &data, sizeof(data));

    return 0;
}

'''

def handle_sys_enter_openat(cpu, data, size):
    event = bpf['events'].event(data)
    pid = event.pid
    filename = event.filename
    comm = event.comm
    print("The pid is {}, the filename is {} and the comm is {}".format(pid,filename,comm))

bpf = BPF(text=bpf_source,  cflags=["-Wno-macro-redefined"])
bpf.attach_tracepoint(tp="syscalls:sys_enter_openat", fn_name="sys_enter_openat_fn")
bpf['events'].open_perf_buffer(handle_sys_enter_openat)

while True:
    try:
        bpf.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()


