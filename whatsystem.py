import subprocess
import platform
import re
import sys
from termcolor import colored

def get_the_ttl(ip):
    """Hace ping a la IP y devuelve el TTL como entero, o None si falla."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        proc = subprocess.Popen(
            f"ping {param} 1 {ip}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        out, _ = proc.communicate(timeout=3)
        out = out.decode('utf-8')

        # Regex para capturar TTL
        ttl_match = re.search(r"ttl[=|:]\s*(\d+)", out, re.IGNORECASE)
        if ttl_match:
            return int(ttl_match.group(1))
        return None
    except Exception:
        return None

def get_os(ttl):
    """Devuelve sistema operativo probable según TTL."""
    if ttl is None:
        return "No response"
    ttl = int(ttl)
    if 0 <= ttl <= 64:
        return "Linux"
    elif 65 <= ttl <= 182:
        return "Windows"
    else:
        return "Unknown"

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 whatsystem.py <IP>")
        sys.exit(1)

    ip = sys.argv[1]
    ttl = get_the_ttl(ip)
    os_guess = get_os(ttl)

    # Colorear según OS
    if os_guess == "Linux":
        os_colored = colored(os_guess, "yellow")  # naranja aproximado
    elif os_guess == "Windows":
        os_colored = colored(os_guess, "blue")
    else:
        os_colored = colored(os_guess, "red")

    print(f"[+] IP: {ip}")
    print(f"[+] TTL: {ttl}")
    print(f"[+] Sistema detectado: {os_colored}")

if __name__ == "__main__":
    main()
