import requests
from bs4 import BeautifulSoup
import argparse
import time
import sys

# ASCII Art for the tool
def print_banner():
    banner = r"""
░██╗░░░░░░░██╗██████╗░███████╗███╗░░██╗██╗░░░██╗███╗░░░███╗██╗░░██╗
░██║░░██╗░░██║██╔══██╗██╔════╝████╗░██║██║░░░██║████╗░████║╚██╗██╔╝
░╚██╗████╗██╔╝██████╔╝█████╗░░██╔██╗██║██║░░░██║██╔████╔██║░╚███╔╝░
░░████╔═████║░██╔═══╝░██╔══╝░░██║╚████║██║░░░██║██║╚██╔╝██║░██╔██╗░
░░╚██╔╝░╚██╔╝░██║░░░░░███████╗██║░╚███║╚██████╔╝██║░╚═╝░██║██╔╝╚██╗
░░░╚═╝░░░╚═╝░░╚═╝░░░░░╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝
           WordPress Plugin & Theme Enumerator 
           - By @rezydev
    """
    print(f"\033[92m{banner}\033[0m")

# Simulating scanning progress
def show_loading(message):
    sys.stdout.write(f"\033[93m{message}\033[0m")
    sys.stdout.flush()
    for _ in range(3):
        time.sleep(0.5)
        sys.stdout.write(".")
        sys.stdout.flush()
    time.sleep(0.5)
    print("\n")

def enumerate_items(url):
    show_loading("Scanning the website for plugins and themes")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all 'href' and 'src' attributes
    links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
    scripts = [script.get('src') for script in soup.find_all('script') if script.get('src')]

    all_links = links + scripts

    # Enumerating plugins and themes
    plugins = [link for link in all_links if 'wp-content/plugins/' in link]
    themes = [link for link in all_links if 'wp-content/themes/' in link]

    # Displaying plugins
    print("\n\033[92m[+] Plugins Enumerated:\033[0m")
    if plugins:
        for i, plugin in enumerate(plugins, 1):
            print(f" {i:02d}. {plugin}")
    else:
        print(" No plugins found.")

    # Displaying themes
    print("\n\033[94m[+] Themes Enumerated:\033[0m")
    if themes:
        for i, theme in enumerate(themes, 1):
            print(f" {i:02d}. {theme}")
    else:
        print(" No themes found.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WordPress Plugin and Theme Enumerator')
    parser.add_argument('--wp-url', required=True, help='URL of the WordPress site to enumerate')

    args = parser.parse_args()

    print_banner()
    enumerate_items(args.wp_url)
