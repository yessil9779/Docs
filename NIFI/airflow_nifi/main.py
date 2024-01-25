import funcs

queue_id = "3b401c27-39c9-1d6e-42fc-a3e171b11637"
processor_id = "3b401c25-39c9-1d6e-2b24-21f2df17bdeb"

if funcs.get_queue_size(queue_id) == 0:
    funcs.set_run_proc("3b401c25-39c9-1d6e-2b24-21f2df17bdeb", "STOPPED")

