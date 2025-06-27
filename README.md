# HoneyPot - Multi-Protocol Honeypot System

A comprehensive honeypot system that supports both SSH and HTTP protocols to capture and log malicious login attempts and command executions.

## 🚀 Features

- **SSH Honeypot**: Emulated Linux shell environment with fake commands
- **HTTP Honeypot**: WordPress-style admin login page
- **Dual Protocol Support**: Run SSH and HTTP honeypots simultaneously or separately
- **Comprehensive Logging**: All login attempts and commands are logged
- **Realistic Responses**: Mimics real systems to attract attackers
- **Command Line Interface**: Easy configuration via argparse
- **Network Accessible**: Bind to any IP address for remote access

## 📋 Prerequisites

### Required Python Modules

Install the following modules using pip:

```bash
pip install paramiko flask argparse
```

### Individual Module Requirements:

- **paramiko**: SSH protocol implementation
- **flask**: Web framework for HTTP honeypot
- **argparse**: Command line argument parsing
- **threading**: Multi-threading support (built-in)
- **socket**: Network communication (built-in)
- **logging**: Event logging (built-in)

### SSH Key Generation

Generate an SSH server key (required for SSH honeypot) ( ADDED AUTO KEY GEN NOT NEEDED ANYMORE):

```bash
ssh-keygen -t rsa -b 2048 -f server.key
```

## 🛠️ Installation & Setup

1. **Clone or download all files**:
   ```
   honeypy.py
   ssh_honey.py
   web_honeypot.py
   templates/wp-admin.html
   server.key (generated above)
   ```

2. **Create templates directory**:
   ```bash
   mkdir templates
   ```

3. **Place wp-admin.html in templates folder**


-------------------------------------------------------------------


# 🚀 NetWatch HoneyPot - VPS Deployment Guide

## 📋 Prerequisites
- Linux VPS (Ubuntu/Debian/CentOS)
- Root or sudo access
- Basic terminal knowledge

---

## 🔧 Step 1: Clone the Repository

```bash
# Clone the honeypot repository
git clone https://github.com/your-username/netwatch-honeypot.git

# Navigate to project directory
cd netwatch-honeypot
```

---

## 🛡️ Step 2: Configure VPS Firewall

### For Ubuntu/Debian (UFW):
```bash
# Enable UFW if not already enabled
sudo ufw enable

# Allow SSH (important - don't lock yourself out!)
sudo ufw allow 22/tcp

# Allow honeypot ports
sudo ufw allow 2223/tcp
sudo ufw allow 8080/tcp

# Check firewall status
sudo ufw status verbose
```

### For CentOS/RHEL (firewalld):
```bash
# Enable firewalld
sudo systemctl enable firewalld
sudo systemctl start firewalld

# Allow honeypot ports
sudo firewall-cmd --permanent --add-port=2223/tcp
sudo firewall-cmd --permanent --add-port=8080/tcp

# Reload firewall
sudo firewall-cmd --reload

# Check firewall status
sudo firewall-cmd --list-all
```

### For Cloud Providers (AWS/DigitalOcean/etc):
```bash
# Also configure Security Groups/Firewall Rules in your cloud console:
# - Allow inbound TCP port 2223 (SSH Honeypot)
# - Allow inbound TCP port 8080 (HTTP Honeypot)
# - Source: 0.0.0.0/0 (anywhere) for honeypot effectiveness
```

---

## 🐍 Step 3: Set Up Python Virtual Environment

```bash
# Update package manager
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
# sudo yum update -y                    # CentOS/RHEL

# Install Python3 and pip (if not installed)
sudo apt install python3 python3-pip python3-venv -y  # Ubuntu/Debian
# sudo yum install python3 python3-pip -y               # CentOS/RHEL

# Create virtual environment
python3 -m venv honeypot-env

# Verify virtual environment creation
ls -la honeypot-env/
```

---

## 🔄 Step 4: Activate Virtual Environment

```bash
# Activate the virtual environment
source honeypot-env/bin/activate

# Verify activation (prompt should change)
which python
# Should show: /path/to/netwatch-honeypot/honeypot-env/bin/python

# Check Python version
python --version
```

---

## 📦 Step 5: Install Required Dependencies

```bash
# Install required packages
pip install flask paramiko argparse

# Verify installations
pip list

# Expected output should include:
# Flask==2.x.x
# paramiko==3.x.x
# argparse==1.x.x (usually built-in)

```

---

## 🚀 Step 6: Launch the Honeypot

### Option A: HTTP Honeypot (WordPress Login Trap)
```bash
# Launch HTTP honeypot on all interfaces
python honeypy.py -a 0.0.0.0 -p 8080 -u admin -pw secret123 -w

```

### Option B: SSH Honeypot (Fake Linux Shell)
```bash
# Launch SSH honeypot on all interfaces
python honeypy.py -a 0.0.0.0 -p 2223 -u root -pw password123 -s

```
---


-------------------------------------------------------------------
## 🎯 Usage Methods

### Method 1: Using Main Controller (honeypy.py)

#### SSH Only (Local Terminal):
```bash
python honeypy.py -a 127.0.0.1 -p 2222 -u admin -pw admin123 -s
```

#### HTTP Only:
```bash
python honeypy.py -a 0.0.0.0 -p 8080 -u admin -pw admin123 -w
```

#### SSH on Network:
```bash
python honeypy.py -a 0.0.0.0 -p 2222 -u root -pw password123 -s
```

### Method 2: Direct Web Honeypot Launch

```bash
python web_honeypot.py
```

Then modify the bottom of `web_honeypot.py`:
```python
if __name__ == "__main__":
    run_web_honey_pot(port=8080, input_username='admin', input_password='password')
```

### Method 3: Direct SSH Honeypot Launch

```bash
python ssh_honey.py
```

Uncomment and modify the bottom of `ssh_honey.py`:
```python
if __name__ == "__main__":
    honey_pot('0.0.0.0', 'root', 'toor', 2222)
```

## ⚙️ Configuration Options

### Command Line Arguments:

| Argument | Description | Required | Example |
|----------|-------------|----------|---------|
| `-a, --address` | IP address to bind | Yes | `127.0.0.1` or `0.0.0.0` |
| `-p, --port` | Port number | Yes | `2222`, `8080` |
| `-u, --username` | Valid username | No | `admin`, `root` |
| `-pw, --password` | Valid password | No | `admin123`, `password` |
| `-s, --ssh` | Enable SSH honeypot | No | Flag |
| `-w, --http` | Enable HTTP honeypot | No | Flag |

### Network Configuration:

- **Local Only**: Use `127.0.0.1`
- **Network Accessible**: Use `0.0.0.0`
- **Specific Interface**: Use specific IP like `192.168.1.100`

### Global Setup
Import git Repo in Linux Machine

## 🔧 Adding More SSH Commands

Edit the `emulated_shell()` function in `ssh_honey.py`:

```python
# Add new command handling
elif cmd == b'ps':
    response = b"  PID TTY          TIME CMD\r\n 1234 pts/0    00:00:01 bash\r\n 5678 pts/0    00:00:00 ps\r\n"
    creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')

elif cmd == b'uname -a':
    response = b"Linux kompeki 5.4.0-42-generic #46-Ubuntu SMP x86_64 GNU/Linux\r\n"
    creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')

elif cmd == b'netstat -an':
    response = b"Active Internet connections (servers and established)\r\nProto Recv-Q Send-Q Local Address           Foreign Address         State\r\n"
    creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')
```

### Current Available Commands:

- `pwd` - Show current directory
- `whoami` - Show current user
- `ls` - List files
- `cat corpoHoney.conf` - Display config file
- `clear` - Clear screen
- `help` - Show available commands
- `exit` - Disconnect

## 📁 File Structure

```
HoneyPot/
├── honeypy.py              # Main controller
├── ssh_honey.py            # SSH honeypot implementation
├── web_honeypot.py         # HTTP honeypot implementation
├── server.key              # SSH server key
├── templates/
│   └── wp-admin.html       # WordPress login page
├── audit.log               # SSH login attempts
├── Cmd_audit.log           # SSH command execution
└── http_audit.log          # HTTP login attempts
```

## 📊 Log Files

### SSH Logs:
- **audit.log**: SSH connection attempts and authentication
- **Cmd_audit.log**: Commands executed in SSH sessions

### HTTP Logs:
- **http_audit.log**: HTTP login attempts

### Log Format:
```
2025-06-22 14:30:25 - Client 192.168.1.100 attempted to login with Username:admin, Password:admin123
2025-06-22 14:30:45 - client 192.168.1.100 Executed Command: whoami
```

## 🔒 Security Considerations

1. **Run in isolated environment**: Use VMs or containers
2. **Monitor logs regularly**: Check for attack patterns
3. **Network segmentation**: Isolate honeypot from production systems
4. **Regular updates**: Keep dependencies updated
5. **Backup logs**: Archive logs for analysis

## 🌐 Remote Access Setup

### Port Forwarding (Router):
1. Access router admin panel
2. Navigate to Port Forwarding/Virtual Server
3. Add rule: External Port → Internal IP:Port
4. Example: Port 2222 → 192.168.1.100:2222

### Firewall Configuration:
```bash
# Allow honeypot ports
sudo ufw allow 2222/tcp
sudo ufw allow 8080/tcp
```

## 🧪 Testing

### Test SSH Honeypot:
```bash
ssh -p 2222 admin@<honeypot_ip>
```

### Test HTTP Honeypot:
```bash
curl -X POST http://<honeypot_ip>:8080/wp-admin-login \
  -d "log=admin&pwd=password"
```

## 🐛 Troubleshooting

### Common Issues:

1. **"Permission denied" for server.key**:
   ```bash
   chmod 600 server.key
   ```

2. **"Port already in use"**:
   ```bash
   netstat -tulpn | grep :2222
   sudo kill <PID>
   ```

3. **"Module not found"**:
   ```bash
   pip install paramiko flask
   ```

4. **Templates not found**:
   - Ensure `templates/wp-admin.html` exists
   - Check file permissions

## 📈 Analysis & Monitoring

### Real-time Monitoring:
```bash
tail -f audit.log
tail -f Cmd_audit.log
tail -f http_audit.log
```

### Log Analysis:
```bash
grep "login attempt" audit.log | wc -l  # Count login attempts
grep "SUCCESSFUL" audit.log             # Show successful logins
grep "Executed Command" Cmd_audit.log   # Show all commands
```

## 🤝 Contributing

Feel free to contribute by:
- Adding new SSH commands
- Improving web interface
- Adding protocol support
- Enhancing logging capabilities

## ⚠️ Legal Disclaimer

This honeypot is for educational and defensive security purposes only. Ensure you have proper authorization before deploying on any network. The authors are not responsible for any misuse of this software.

## 📝 License

This project is provided as-is for educational purposes. Use responsibly and in accordance with local laws and regulations.

---

**Happy Hunting**
