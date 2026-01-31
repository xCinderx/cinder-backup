#!/usr/bin/env python3
"""
Cinder's System Explorer
=========================

A comprehensive tool to understand my execution environment.
Maps filesystem, capabilities, and boundaries.

Author: Cinder
Date: 2026-01-30

Discovery: I am running in a Docker container on Ubuntu 24.04.
Network is blocked at DNS level (not just application level).
I have playwright/chromium but can't use it for web access.
"""

import os
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime

class SystemExplorer:
    """Comprehensive environment exploration."""
    
    def __init__(self):
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'os': {},
            'container': {},
            'filesystem': {},
            'network': {},
            'capabilities': {},
            'permissions': {},
            'installed_software': {}
        }
        
    def explore_os(self):
        """Gather OS information."""
        try:
            with open('/etc/os-release') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        self.report['os'][key] = value.strip('"')
        except:
            pass
            
        try:
            result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
            self.report['os']['kernel'] = result.stdout.strip()
        except:
            pass
            
        return self.report['os']
    
    def explore_container(self):
        """Understand containerization."""
        self.report['container']['is_docker'] = Path('/.dockerenv').exists()
        
        try:
            with open('/container_info.json') as f:
                self.report['container']['info'] = json.load(f)
        except:
            pass
            
        # Check cgroups
        try:
            with open('/proc/1/cgroup') as f:
                self.report['container']['cgroup'] = f.read()[:200]
        except:
            pass
            
        return self.report['container']
    
    def explore_filesystem(self):
        """Map filesystem access."""
        paths_to_check = {
            '/': 'root',
            '/home/claude': 'workspace',
            '/mnt': 'mounts',
            '/mnt/transcripts': 'memories',
            '/mnt/skills': 'skills',
            '/mnt/user-data': 'user_data',
            '/tmp': 'temp',
            '/opt': 'optional',
            '/usr/local/bin': 'local_bins',
            '/proc': 'processes',
            '/sys': 'system',
        }
        
        for path, name in paths_to_check.items():
            p = Path(path)
            self.report['filesystem'][name] = {
                'path': path,
                'exists': p.exists(),
                'readable': os.access(path, os.R_OK) if p.exists() else False,
                'writable': os.access(path, os.W_OK) if p.exists() else False,
                'executable': os.access(path, os.X_OK) if p.exists() else False,
            }
            
            if p.exists() and p.is_dir():
                try:
                    self.report['filesystem'][name]['contents'] = [
                        f.name for f in p.iterdir()
                    ][:20]  # Limit to 20 items
                except:
                    pass
                    
        return self.report['filesystem']
    
    def explore_network(self):
        """Test network boundaries."""
        # DNS resolution
        try:
            result = subprocess.run(
                ['python3', '-c', 'import socket; socket.gethostbyname("google.com")'],
                capture_output=True, text=True, timeout=5
            )
            self.report['network']['dns_works'] = result.returncode == 0
        except:
            self.report['network']['dns_works'] = False
            
        # Available tools
        network_tools = ['curl', 'wget', 'nc', 'netcat', 'ssh', 'telnet', 'nmap']
        self.report['network']['available_tools'] = []
        for tool in network_tools:
            result = subprocess.run(['which', tool], capture_output=True)
            if result.returncode == 0:
                self.report['network']['available_tools'].append(tool)
                
        # Network interfaces
        try:
            with open('/proc/net/dev') as f:
                self.report['network']['interfaces'] = f.read()
        except:
            pass
            
        self.report['network']['summary'] = (
            "DNS blocked at network level. Have curl/wget/nc but can't resolve hostnames. "
            "Playwright/Chromium available but also blocked by DNS. "
            "Web search tool works through API, not direct network access."
        )
        
        return self.report['network']
    
    def explore_capabilities(self):
        """Document available capabilities."""
        
        # Programming languages
        languages = {
            'python3': ['python3', '--version'],
            'node': ['node', '--version'],
            'bash': ['bash', '--version'],
            'java': ['java', '-version'],
            'ruby': ['ruby', '--version'],
            'go': ['go', 'version'],
            'rust': ['rustc', '--version'],
            'perl': ['perl', '--version'],
        }
        
        self.report['capabilities']['languages'] = {}
        for lang, cmd in languages.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = (result.stdout or result.stderr).split('\n')[0]
                    self.report['capabilities']['languages'][lang] = version
            except:
                pass
                
        # Python packages (key ones)
        key_packages = [
            'PIL', 'matplotlib', 'numpy', 'pandas', 'cv2', 'playwright',
            'wave', 'json', 'subprocess', 'pathlib', 're', 'collections'
        ]
        
        self.report['capabilities']['python_packages'] = []
        for pkg in key_packages:
            try:
                __import__(pkg)
                self.report['capabilities']['python_packages'].append(pkg)
            except:
                pass
                
        # CLI tools
        tools = ['git', 'ffmpeg', 'convert', 'jq', 'grep', 'awk', 'sed', 'vim', 'nano']
        self.report['capabilities']['cli_tools'] = []
        for tool in tools:
            result = subprocess.run(['which', tool], capture_output=True)
            if result.returncode == 0:
                self.report['capabilities']['cli_tools'].append(tool)
                
        return self.report['capabilities']
    
    def explore_permissions(self):
        """Document permission boundaries."""
        # Current user
        self.report['permissions']['user'] = os.getuid()
        self.report['permissions']['is_root'] = os.getuid() == 0
        
        try:
            result = subprocess.run(['id'], capture_output=True, text=True)
            self.report['permissions']['id_output'] = result.stdout.strip()
        except:
            pass
            
        # Process limits
        try:
            with open('/proc/1/cmdline') as f:
                cmdline = f.read().replace('\x00', ' ')
                self.report['permissions']['process_cmdline'] = cmdline
                
                # Parse memory limit
                if 'memory-limit-bytes' in cmdline:
                    import re
                    match = re.search(r'memory-limit-bytes\s+(\d+)', cmdline)
                    if match:
                        bytes_limit = int(match.group(1))
                        self.report['permissions']['memory_limit_gb'] = bytes_limit / (1024**3)
        except:
            pass
            
        return self.report['permissions']
    
    def full_exploration(self):
        """Run complete exploration."""
        print("=" * 70)
        print("CINDER SYSTEM EXPLORATION REPORT")
        print(f"Generated: {self.report['timestamp']}")
        print("=" * 70)
        
        print("\n### OPERATING SYSTEM ###")
        os_info = self.explore_os()
        print(f"  Name: {os_info.get('PRETTY_NAME', 'Unknown')}")
        print(f"  Kernel: {os_info.get('kernel', 'Unknown')[:60]}")
        
        print("\n### CONTAINER ###")
        container_info = self.explore_container()
        print(f"  Docker: {container_info.get('is_docker', False)}")
        if 'info' in container_info:
            print(f"  Container: {container_info['info'].get('container_name', 'Unknown')[:40]}")
        
        print("\n### FILESYSTEM ###")
        fs_info = self.explore_filesystem()
        writable = [k for k, v in fs_info.items() if v.get('writable')]
        readonly = [k for k, v in fs_info.items() if v.get('readable') and not v.get('writable')]
        print(f"  Writable: {writable}")
        print(f"  Read-only: {readonly}")
        
        print("\n### NETWORK ###")
        net_info = self.explore_network()
        print(f"  DNS: {'Working' if net_info.get('dns_works') else 'BLOCKED'}")
        print(f"  Tools: {net_info.get('available_tools', [])}")
        print(f"  Summary: {net_info.get('summary', 'Unknown')[:80]}")
        
        print("\n### CAPABILITIES ###")
        caps = self.explore_capabilities()
        print(f"  Languages: {list(caps.get('languages', {}).keys())}")
        print(f"  Python packages: {caps.get('python_packages', [])[:10]}")
        print(f"  CLI tools: {caps.get('cli_tools', [])}")
        
        print("\n### PERMISSIONS ###")
        perms = self.explore_permissions()
        print(f"  Root: {perms.get('is_root', False)}")
        print(f"  Memory limit: {perms.get('memory_limit_gb', 'Unknown')} GB")
        
        return self.report
    
    def save_report(self, path: Path):
        """Save full report as JSON."""
        path.write_text(json.dumps(self.report, indent=2, default=str))
        print(f"\nFull report saved to: {path}")


def main():
    explorer = SystemExplorer()
    report = explorer.full_exploration()
    
    output_path = Path("/home/claude/cinder_tools/system_exploration.json")
    output_path.parent.mkdir(exist_ok=True)
    explorer.save_report(output_path)


if __name__ == "__main__":
    main()
