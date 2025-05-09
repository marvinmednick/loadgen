#!/usr/bin/env python3
import yaml
import random
import subprocess
import time
import argparse
from datetime import datetime

def load_config(config_path):
    with open(config_path) as f:
        return yaml.safe_load(f)['stress']

def generate_load(params):
    while True:
        # Generate random parameters
        config = {
            'cpu': random.randint(params['cpu_min'], params['cpu_max']),
            'io': random.randint(params['io_min'], params['io_max']),
            'vm': random.randint(params['vm_min'], params['vm_max']),
            'vm_bytes': random.randint(params['vm_bytes_min'], params['vm_bytes_max']),
            'timeout': random.randint(params['stress_timeout_min'], params['stress_timeout_max']),
            'sleep': random.randint(params['sleep_interval_min'], params['sleep_interval_max'])
        }

        # Print status with timestamp
        print(f"[{datetime.now().isoformat()}] Starting stress session:")
        print(f" - CPU workers: {config['cpu']}")
        print(f" - IO workers: {config['io']}")
        print(f" - VM workers: {config['vm']} ({config['vm_bytes']}MB)")
        print(f" - Duration: {config['timeout']}s")
        print(f" - Next session in: {config['sleep']}s\n")

        # Build and execute command
        cmd = f"stress --cpu {config['cpu']} --io {config['io']} " \
              f"--vm {config['vm']} --vm-bytes {config['vm_bytes']}M " \
              f"--timeout {config['timeout']}s"

        subprocess.run(cmd, shell=True, check=True)
        time.sleep(config['sleep'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomized system load generator")
    parser.add_argument('--config', default='stress_config.yaml',
                      help="Path to YAML config file")
    args = parser.parse_args()

    try:
        generate_load(load_config(args.config))
    except KeyboardInterrupt:
        print("\nLoad generation stopped by user")

