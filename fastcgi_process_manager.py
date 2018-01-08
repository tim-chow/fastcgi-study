import socket
import os
from optparse import OptionParser

def main(addr, backlog, worker_count, executable, args, env):
    master_pid = os.getpid()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(addr)
    server_socket.listen(backlog)
    os.dup2(server_socket.fileno(), 0)

    children = []
    while len(children) < worker_count: 
        pid = os.fork()
        if pid > 0:
            children.append(pid)
        else:
            break

    if os.getpid() == master_pid:
        while len(children):
            pid = children[0]
            exit_status = os.wait()
            children.remove(exit_status[0])
        print "all children all dead, master exit"
        os._exit(0)
    os.execve(executable, args, env)

if __name__ == "__main__":
    parser = OptionParser("usage: %proc [options]")
    parser.add_option("-a", "--bind-address", dest="bind_address",
        default="0.0.0.0", help="address to bind", type=str)
    parser.add_option("-p", "--port", dest="port", default=9091,
        help="port to bind", type=int)
    parser.add_option("-b", "--backlog", dest="backlog", default=5,
        help="listen backlog", type=int)
    parser.add_option("-w", "--worker", dest="worker", default=3,
        help="worker count", type=int)
    parser.add_option("-e", "--executable", dest="executable",
        help="executable path")
    options, _ = parser.parse_args()
    if not options.executable:
        parser.error("no executable")
    main((options.bind_address, options.port), 
        options.backlog, options.worker, 
        options.executable, tuple(), dict())

