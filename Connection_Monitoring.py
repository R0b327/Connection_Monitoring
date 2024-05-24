import os
import curses
import time
import psutil

os.system('mode con: cols=60 lines=10')
os.system('title Connection Monitoring By R0b327')

def display_graph(value):
    hashes = "#" * int(value / 5)
    dots = "." * (20 - len(hashes))
    graph = f"[{hashes}{dots}]"
    return graph

def display_traffic(stdscr, incoming_kbps, outgoing_kbps):
    stdscr.clear()

    connections = psutil.net_connections(kind='tcp')
    num_connections = len(connections)

    disk_usage = psutil.disk_usage('/')
    used_space = disk_usage.used

    cpu_usage_percent = psutil.cpu_percent()
    ram_usage_percent = psutil.virtual_memory().percent

    incoming_mbps = incoming_kbps / 1000
    outgoing_mbps = outgoing_kbps / 1000

    incoming_graph = display_graph(incoming_mbps)
    outgoing_graph = display_graph(outgoing_mbps)

    stdscr.addstr(0, 0, f"CPU usage: {cpu_usage_percent}%")
    stdscr.addstr(1, 0, f"RAM usage: {ram_usage_percent}%")
    stdscr.addstr(2, 0, f"DISK usage: {psutil._common.bytes2human(used_space)}")
    stdscr.addstr(3, 0, f"TCP connections: {num_connections}")

    stdscr.addstr(6, 0, "Incoming:")
    stdscr.addstr(7, 0, f"{incoming_kbps:.2f} KBits/s")
    stdscr.addstr(8, 0, f"{incoming_mbps:.2f} MBits/s")
    stdscr.addstr(9, 0, f"{incoming_graph}")

    stdscr.addstr(6, 27, "Outgoing:")
    stdscr.addstr(7, 27, f"{outgoing_kbps:.2f} KBits/s")
    stdscr.addstr(8, 27, f"{outgoing_mbps:.2f} MBits/s")
    stdscr.addstr(9, 27, f"{outgoing_graph}")

    stdscr.refresh()

def main(stdscr):
    stdscr.nodelay(True)
    curses.curs_set(0)

    while True:
        net_io_counters_start = psutil.net_io_counters()

        time.sleep(1)

        net_io_counters_end = psutil.net_io_counters()

        bytes_sent = (net_io_counters_end.bytes_sent - net_io_counters_start.bytes_sent) / 2
        bytes_recv = (net_io_counters_end.bytes_recv - net_io_counters_start.bytes_recv) / 2

        outgoing_kbps = bytes_sent * 8 / 1000
        incoming_kbps = bytes_recv * 8 / 1000

        display_traffic(stdscr, incoming_kbps, outgoing_kbps)

        if stdscr.getch() == ord('q'):
            break

curses.wrapper(main)