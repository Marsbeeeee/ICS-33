from pathlib import Path
from collections import defaultdict

class Simulation:
    def __init__(self) -> None:
        self.sim_length = 0
        self.propagation = defaultdict(list)
        self.device_ids = set()
        self._events_by_time = defaultdict(list)
        self.canceled = defaultdict(set)
        self.cancel_time = defaultdict(dict)
        self.cancel_sources = defaultdict(set)

    def load_file(self, path: Path) -> None:
        try:
            with path.open('r') as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split()
                    cmd = parts[0]
                    if cmd == 'LENGTH':
                        self.sim_length = int(parts[1])
                    elif cmd == 'DEVICE':
                        dev = int(parts[1])
                        self.device_ids.add(dev)
                    elif cmd == 'PROPAGATE':
                        src, dst, delay = map(int, parts[1:])
                        self.propagation[src].append((dst, delay))
                    elif cmd == 'ALERT':
                        dev, msg, t = int(parts[1]), parts[2], int(parts[3])
                        self._add_event(t, 'send_alert', dev, msg)
                    elif cmd == 'CANCEL':
                        dev, msg, t = int(parts[1]), parts[2], int(parts[3])
                        self._add_event(t, 'send_cancel', dev, msg)
        except (FileNotFoundError, OSError, ValueError):
            print('FILE NOT FOUND')
            raise SystemExit(0)

    def _add_event(self, time: int, kind: str, sender: int, payload: object) -> None:
        self._events_by_time[time].append((kind, sender, payload))

    @staticmethod
    def _sort_key(event_tuple):
        kind = event_tuple[0]
        return 0 if kind.startswith('recv') else 1

    @staticmethod
    def _log_event(time, direction, msg_type, src, dest, msg):
        left_id = src if direction == 'send' else dest
        verb = 'SENT' if direction == 'send' else 'RECEIVED'
        right_phrase = (f'TO #{dest}') if direction == 'send' else (f'FROM #{src}')
        print(f"@{time}: #{left_id} {verb} {msg_type} {right_phrase}: {msg}")

    def run(self) -> None:
        times = sorted(self._events_by_time.keys())
        i = 0
        while i < len(times):
            t = times[i]
            events = sorted(self._events_by_time[t], key = self._sort_key)

            for kind, sender, payload in events:
                if kind == 'send_alert':
                    msg = payload
                    for target, delay in self.propagation.get(sender, []):
                        arrival = t + delay
                        if arrival < self.sim_length:
                            self._add_event(arrival, 'recv_alert', sender, (target, msg))
                            if arrival not in times:
                                times.append(arrival)
                        self._log_event(t, 'send', 'ALERT', sender, target, msg)

                elif kind == 'recv_alert':
                    receiver, msg = payload
                    cutoff = self.cancel_time[receiver].get(msg, -1)
                    self._log_event(t, 'receive', 'ALERT', sender, receiver, msg)
                    if msg in self.canceled[receiver] and t >= cutoff + 1:
                        continue
                    for target, delay in self.propagation.get(receiver, []):
                        arrival = t + delay
                        if arrival < self.sim_length:
                            self._add_event(arrival, 'recv_alert', receiver, (target, msg))
                            if arrival not in times:
                                times.append(arrival)
                        self._log_event(t, 'send', 'ALERT', receiver, target, msg)

                elif kind == 'send_cancel':
                    msg = payload
                    if msg not in self.canceled[sender]:
                        self.canceled[sender].add(msg)
                        self.cancel_time[sender][msg] = t
                    for target, delay in self.propagation.get(sender, []):
                        arrival = t + delay
                        if arrival < self.sim_length:
                            self._add_event(arrival, 'recv_cancel', sender, (target, msg))
                            if arrival not in times:
                                times.append(arrival)
                        self._log_event(t, 'send', 'CANCELLATION', sender, target, msg)

                elif kind == 'recv_cancel':
                    receiver, msg = payload
                    if msg in self.canceled[receiver] and t >= self.cancel_time[receiver].get(msg,
                                                                                              -1) + 1:
                        self._log_event(t, 'receive', 'CANCELLATION', sender, receiver, msg)
                        continue
                    if (sender, msg) in self.cancel_sources[receiver]:
                        continue
                    self.cancel_sources[receiver].add((sender, msg))
                    if msg not in self.canceled[receiver]:
                        self.canceled[receiver].add(msg)
                        self.cancel_time[receiver][msg] = t
                    self._log_event(t, 'receive', 'CANCELLATION', sender, receiver, msg)
                    for target, delay in self.propagation.get(receiver, []):
                        arrival = t + delay
                        if arrival < self.sim_length:
                            self._add_event(arrival, 'recv_cancel', receiver, (target, msg))
                            if arrival not in times:
                                times.append(arrival)
                        self._log_event(t, 'send', 'CANCELLATION', receiver, target, msg)

            i += 1
            times.sort()

        print(f"@{self.sim_length}: END")

def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    raw = input().strip()
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    return Path(raw)

def main() -> None:
    """Runs the simulation program in its entirety"""
    sim = Simulation()
    input_path = _read_input_file_path()
    sim.load_file(input_path)
    sim.run()

if __name__ == '__main__':
    main()
