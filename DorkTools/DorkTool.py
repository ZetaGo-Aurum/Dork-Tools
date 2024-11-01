"""
Advanced Dorking Tool
Created by: Rayhan Dzaky Al Mubarok
Github: https://github.com/ZetaGo-Aurum?tab=repositories
"""

import os
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import json
import sys
from tabulate import tabulate
import itertools
import threading

def show_credits():
    print("\n" + "="*50)
    print("\033[95mAdvanced Dorking Tool")
    print("Created by: Rayhan Dzaky Al Mubarok")
    print("Github: https://github.com/ZetaGo-Aurum?tab=repositories\033[0m")
    print("="*50)
    time.sleep(2)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation():
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for char in itertools.cycle(chars):
        sys.stdout.write('\r' + f'\033[93mScanning... {char}\033[0m')
        sys.stdout.flush()
        time.sleep(0.1)

class DorkingTool:
    def __init__(self):
        show_credits()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.dork_patterns = {
            'sql_injection': [
                'inurl:.php?id=',
                'inurl:index.php?id=',
                'inurl:product.php?id='
            ],
            'exposed_files': [
                'filetype:pdf',
                'filetype:xls', 
                'filetype:doc',
                'filetype:txt'
            ],
            'sensitive_dirs': [
                'intitle:index.of',
                'inurl:/admin',
                'inurl:/backup',
                'inurl:/wp-admin'
            ],
            'open_ports': [
                'port:22',
                'port:80',
                'port:443'
            ],
            'dork_url': [
                'inurl:login',
                'inurl:register', 
                'inurl:signin'
            ],
            'dork_website': [
                'inurl:www',
                'inurl:site',
                'inurl:home'
            ],
            'dork_password': [
                '"password" filetype:txt',
                '"password" filetype:doc',
                '"password" filetype:xls'
            ],
            'dork_personal_data': [
                '"phone number" filetype:pdf',
                '"email" filetype:docx',
                '"address" filetype:xls'
            ],
            'smart_dork': []
        }

    def search_google(self, query, max_results=50, num_pages=5, messages={}):
        results = []
        print("\n" + "="*50)
        print("\033[95m=== Search Results ===\033[0m")
        print("="*50)
        print("\033[96mQuery:", query, "\033[0m\n")
        
        headers = ["No", "URL", "Status", "Title"]
        table_data = []
        
        # Start loading animation
        stop_loading = False
        loading_thread = threading.Thread(target=lambda: self.animate_loading(lambda: stop_loading))
        loading_thread.start()
        
        for page in range(num_pages):
            try:
                url = f"https://www.google.com/search?q={quote_plus(query)}&start={page*10}"
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')

                for g in soup.find_all('div', class_='g'):
                    anchors = g.find_all('a')
                    if anchors:
                        link = anchors[0]['href']
                        if link.startswith('/url?q='):
                            link = link.split('/url?q=')[1].split('&')[0]
                        if link not in results:
                            try:
                                response = requests.head(link, timeout=5)
                                status = response.status_code
                                status_text = f"\033[92m{status}\033[0m" if status == 200 else f"\033[91m{status}\033[0m"
                                
                                # Get page title
                                title_response = requests.get(link, timeout=5)
                                title_soup = BeautifulSoup(title_response.text, 'html.parser')
                                title = title_soup.title.string if title_soup.title else "No Title"
                                title = title[:50] + "..." if len(title) > 50 else title
                                
                            except:
                                status_text = "\033[93mError\033[0m"
                                title = "Not Accessible"
                                
                            table_data.append([
                                f"\033[96m{len(results) + 1}\033[0m", 
                                f"\033[97m{link}\033[0m",
                                status_text,
                                f"\033[94m{title}\033[0m"
                            ])
                            results.append(link)
                            if len(results) >= max_results:
                                stop_loading = True
                                loading_thread.join()
                                print("\n" + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
                                return results
                time.sleep(2)
            except Exception as e:
                print(f"\n\033[91mError on page {page+1}: {str(e)}\033[0m")
                time.sleep(2)
                continue
        
        stop_loading = True
        loading_thread.join()
        print("\n" + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        return results

    def animate_loading(self, stop_condition):
        spinner = itertools.cycle(['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'])
        while not stop_condition():
            sys.stdout.write('\r\033[93mScanning... ' + next(spinner) + '\033[0m')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' '*20 + '\r')

    def analyze_vulnerability(self, url, messages={}):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            vulnerabilities = []

            security_headers = ['X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options']
            for header in security_headers:
                if header not in response.headers:
                    vulnerabilities.append(f"\033[91m{messages['missing_header'].format(header)}\033[0m")

            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            for form in forms:
                if form.get('action') and not form['action'].startswith('https'):
                    vulnerabilities.append(f"\033[91m{messages['unsecure_form']}\033[0m")

            return vulnerabilities
        except:
            return [f"\033[91m{messages['cannot_access_url']}\033[0m"]

    def advanced_dork_scan(self, target_domain="", scan_type="all", max_results=50, custom_content="", custom_subdomain="", smart_query="", messages={}):
        all_results = []
        
        print("\n" + "="*50)
        print("\033[95m=== Scanning Results ===\033[0m")
        print("="*50)
        print(f"\033[96mScan Type: {scan_type.replace('_', ' ').title()}")
        print(f"Target Domain: {target_domain if target_domain else 'Global'}\033[0m\n")
        
        # Start loading animation
        stop_loading = False
        loading_thread = threading.Thread(target=lambda: self.animate_loading(lambda: stop_loading))
        loading_thread.start()
        
        try:
            for category_key, category in self.dork_patterns.items():
                if scan_type != "all" and scan_type != category_key:
                    continue
                    
                print(f"\n\033[94m=== Category: {category_key.replace('_', ' ').title()} ===\033[0m")
                
                # Generate smart dorks if smart_query is provided
                dorks = []
                if smart_query:
                    dorks = self.generate_smart_dork(smart_query)
                else:
                    # If smart_query is empty, use global scanning
                    dorks = category if category else ['']
                    
                # Apply domain filters
                if target_domain:
                    if custom_subdomain:
                        dorks = [f"site:{custom_subdomain}.{target_domain} {dork}" for dork in dorks]
                    else:
                        dorks = [f"site:{target_domain} {dork}" for dork in dorks]
                        
                # Add custom content if provided
                if custom_content:
                    dorks = [f"{dork} {custom_content}" for dork in dorks]
                    
                for dork in dorks:
                    if len(all_results) >= max_results:
                        stop_loading = True
                        loading_thread.join()
                        return all_results
                        
                    print(f"\n\033[92mUsing dork: {dork}\033[0m")
                    results = self.search_google(dork, max_results=max_results - len(all_results), messages=messages)
                    all_results.extend(results)
                    
        except KeyboardInterrupt:
            stop_loading = True
            loading_thread.join()
            print("\n\033[91mSearch stopped by user\033[0m")
            time.sleep(2)
            return list(set(all_results))
        except Exception as e:
            stop_loading = True
            loading_thread.join()
            print(f"\n\033[91mAn error occurred: {str(e)}\033[0m")
            time.sleep(2)
            return list(set(all_results))
            
        stop_loading = True
        loading_thread.join()
        return list(set(all_results))

    def generate_smart_dork(self, query):
        smart_dorks = []
        smart_dorks.append(f'"{query}"')  
        smart_dorks.append(f'intitle:{query}')  
        smart_dorks.append(f'intext:{query}')  
        
        keywords = query.split()
        for keyword in keywords:
            smart_dorks.append(f'"{keyword}"')
            smart_dorks.append(f'intitle:{keyword}')
            smart_dorks.append(f'intext:{keyword}')
            
        self.dork_patterns['smart_dork'] = smart_dorks
        return smart_dorks

    def save_results(self, results, filename="dorking_results.json", messages={}):
        output = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_results": len(results),
            "results": results
        }

        with open(filename, 'w') as f:
            json.dump(output, f, indent=4)
            
        print("\n" + "="*50)
        print(f"\033[92mResults have been saved to {filename}")
        print(f"Total URLs found: {len(results)}\033[0m")
        print("="*50)

    def display_help(self, messages={}):
        clear_screen()
        print("\n" + "="*50)
        print("\033[95mAdvanced Dorking Tool - Help Menu\033[0m")
        print("="*50)
        print("\n\033[96mFeatures and Usage:\033[0m")
        
        help_content = """
1. SQL Injection Scanner
   - Searches for potential SQL injection vulnerabilities
   - Uses dorks like inurl:.php?id=, inurl:index.php?id=
   - Useful for finding vulnerable web applications

2. Exposed Files Scanner
   - Finds exposed documents and files
   - Searches for PDF, XLS, DOC, TXT files
   - Helps identify sensitive document leaks

3. Sensitive Directories Scanner
   - Discovers exposed directories and admin panels
   - Looks for /admin, /backup, /wp-admin paths
   - Useful for security assessment

4. Open Ports Scanner
   - Identifies systems with open ports
   - Scans for common ports (22, 80, 443)
   - Helps in network reconnaissance

5. All Scan Types
   - Runs all available scan types
   - Comprehensive scanning option
   - Most thorough but takes longer

6. Dork URL Scanner
   - Focuses on specific URL patterns
   - Finds login, register, signin pages
   - Useful for mapping web applications

7. Dork Website Scanner
   - General website structure scanning
   - Finds homepage and site structures
   - Good for initial reconnaissance

8. Dork Password Scanner
   - Searches for exposed passwords
   - Scans various file types
   - Critical for security assessment

9. Dork Personal Data Scanner
   - Finds exposed personal information
   - Searches for phone numbers, emails, addresses
   - Important for privacy assessment

10. Custom Search
    - Create your own custom dork
    - Add specific content and subdomains
    - Maximum flexibility in searching

11. Smart Dork
    - Intelligent dork generation
    - Creates multiple search variations
    - Enhanced search effectiveness

General Usage:
- Enter target domain (optional)
- Set maximum results limit
- Choose output filename
- Use Smart Dork query for better results
- Results are saved in JSON format

Tips:
- Leave domain empty for global search
- Use specific scan types for focused results
- Combine with Smart Dork for better coverage
- Check saved results file for complete data
"""
        print(help_content)
        print("="*50)

def select_language():
    while True:
        clear_screen()
        show_credits()
        print("\n\033[96mWelcome to Advanced Dorking Tool!\033[0m")
        print("\nPlease select your language / Silakan pilih bahasa:")
        print("\n1. English")
        print("2. Indonesia")
        print("\n" + "="*80 + "\n")

        language_choice = input("\033[92mEnter language choice / Masukkan pilihan bahasa (1-2): \033[0m")

        if language_choice == "1":
            return "english"
        elif language_choice == "2":
            return "indonesia"
        else:
            print("\033[91mInvalid choice. Please try again.\033[0m")
            time.sleep(1)

def show_dork_menu(dorker, selected_messages):
    messages = {
        "help_title": "Help Menu",
        "help_content": "This is the help content"
    }
    
    while True:
        clear_screen()
        show_credits()

        print("\n\033[96m=== Main Menu ===\033[0m" if selected_messages == "english" else "\n\033[96m=== Menu Utama ===\033[0m")
        print("\n\033[92m0. Help\033[0m")
        print("\033[92m1. SQL Injection\033[0m")
        print("\033[92m2. Exposed Files\033[0m")
        print("\033[92m3. Sensitive Directories\033[0m")
        print("\033[92m4. Open Ports\033[0m")
        print("\033[92m5. All Scan Types\033[0m" if selected_messages == "english" else "\033[92m5. Semua Jenis Scan\033[0m")
        print("\033[92m6. Dork URL\033[0m")
        print("\033[92m7. Dork Website\033[0m")
        print("\033[92m8. Dork Password\033[0m")
        print("\033[92m9. Dork Personal Data\033[0m" if selected_messages == "english" else "\033[92m9. Dork Data Pribadi\033[0m")
        print("\033[92m10. Custom Search\033[0m")
        print("\033[92m11. Smart Dork\033[0m")
        print("\033[92m12. Exit\033[0m" if selected_messages == "english" else "\033[92m12. Keluar\033[0m")
        print("\n" + "="*80 + "\n")

        while True:
            choice = input("\033[96mEnter choice (0-12): \033[0m" if selected_messages == "english" else "\033[96mMasukkan pilihan (0-12): \033[0m")
            if choice in [str(i) for i in range(0, 13)]:
                break
            else:
                print("\n\033[91mInvalid choice\033[0m" if selected_messages == "english" else "\n\033[91mPilihan tidak valid\033[0m")
                time.sleep(1)

        if choice == '12':
            print("\n\033[95mThank you for using Advanced Dorking Tool.\033[0m" if selected_messages == "english" else "\n\033[95mTerima kasih telah menggunakan Tool Dorking Kompleks.\033[0m")
            sys.exit(0)

        scan_types = {
            '0': 'help',
            '1': 'sql_injection',
            '2': 'exposed_files',
            '3': 'sensitive_dirs',
            '4': 'open_ports',
            '5': 'all',
            '6': 'dork_url',
            '7': 'dork_website',
            '8': 'dork_password',
            '9': 'dork_personal_data',
            '10': 'custom_search',
            '11': 'smart_dork'
        }

        scan_type = scan_types.get(choice, 'all')

        if scan_type == 'help':
            dorker.display_help(messages)
            input("\n\033[96mPress Enter to return to main menu...\033[0m" if selected_messages == "english" else "\n\033[96mTekan Enter untuk kembali ke menu utama...\033[0m")
            continue

        print("\n\033[95m=== Scan Configuration ===\033[0m" if selected_messages == "english" else "\n\033[95m=== Konfigurasi Scan ===\033[0m\n")
        target = input("\033[96mEnter target domain (leave empty for global scan): \033[0m" if selected_messages == "english" else "\033[96mMasukkan target domain (kosongkan untuk scan global): \033[0m").strip()
        custom_subdomain = ""
        custom_content = ""
        smart_query = ""

        # Add smart query input for all scan types
        smart_query = input("\n\033[96mEnter Smart Dork query (leave empty for global scan): \033[0m" if selected_messages == "english" else "\n\033[96mMasukkan query Smart Dork (kosongkan untuk scan global): \033[0m").strip()

        if scan_type == 'custom_search':
            print("\n\033[95m=== Custom Search Configuration ===\033[0m")
            custom_content = input("\n\033[96mEnter custom content (example: intext:'admin'): \033[0m" if selected_messages == "english" else "\n\033[96mMasukkan konten khusus (contoh: intext:'admin'): \033[0m").strip()
            custom_subdomain = input("\033[96mEnter custom subdomain: \033[0m" if selected_messages == "english" else "\033[96mMasukkan subdomain khusus: \033[0m").strip()

        print("\n\033[95m=== Output Configuration ===\033[0m")
        output = input("\n\033[96mEnter output filename (default: dorking_results.json): \033[0m" if selected_messages == "english" else "\n\033[96mMasukkan nama file output (default: dorking_results.json): \033[0m").strip()
        if not output:
            output = "dorking_results.json"

        while True:
            try:
                max_results_input = input("\n\033[96mEnter maximum number of results (default: 50): \033[0m" if selected_messages == "english" else "\n\033[96mMasukkan jumlah maksimum hasil dork (default: 50): \033[0m").strip()
                max_results = int(max_results_input) if max_results_input else 50
                if max_results > 0:
                    break
                else:
                    print("\n\033[91mNumber must be greater than 0\033[0m" if selected_messages == "english" else "\n\033[91mJumlah harus lebih dari 0\033[0m")
            except ValueError:
                print("\n\033[91mPlease enter a valid number\033[0m" if selected_messages == "english" else "\n\033[91mMasukkan angka yang valid\033[0m")

        print("\n\033[95m=== Configuration Summary ===\033[0m" if selected_messages == "english" else "\n\033[95m=== Ringkasan Konfigurasi ===\033[0m\n")
        print(f"\033[96mScan Type        : {scan_type.replace('_', ' ').title()}")
        print(f"Target Domain     : {target if target else 'Global'}")
        print(f"Smart Dork Query  : {smart_query if smart_query else 'Global Scan'}" if selected_messages == "english" else f"Query Smart Dork  : {smart_query if smart_query else 'Scan Global'}")
        if scan_type == 'custom_search':
            print(f"Custom Content    : {custom_content if custom_content else 'None'}" if selected_messages == "english" else f"Konten Khusus     : {custom_content if custom_content else 'Tidak ada'}")
            print(f"Custom Subdomain  : {custom_subdomain if custom_subdomain else 'None'}" if selected_messages == "english" else f"Subdomain Khusus  : {custom_subdomain if custom_subdomain else 'Tidak ada'}")
        print(f"Output File       : {output}")
        print(f"Maximum Results   : {max_results}\033[0m" if selected_messages == "english" else f"Maksimum Hasil    : {max_results}\033[0m")
        print("\n\033[93mStarting scan...\033[0m" if selected_messages == "english" else "\n\033[93mMemulai scanning...\033[0m")

        # Start loading animation
        stop_loading = False
        loading_thread = threading.Thread(target=lambda: dorker.animate_loading(lambda: stop_loading))
        loading_thread.start()

        try:
            results = dorker.advanced_dork_scan(target, scan_type, max_results, custom_content, custom_subdomain, smart_query, messages)

            stop_loading = True
            loading_thread.join()

            if results:
                dorker.save_results(results, output)

                print("\n" + "="*50)
                while True:
                    print("\n\033[96m1. Return to main menu" if selected_messages == "english" else "\n\033[96m1. Kembali ke menu utama")
                    print("2. Exit\033[0m" if selected_messages == "english" else "2. Keluar\033[0m")
                    choice_exit = input("\n\033[92mEnter choice (1-2): \033[0m" if selected_messages == "english" else "\n\033[92mMasukkan pilihan (1-2): \033[0m")
                    if choice_exit == '1':
                        break
                    elif choice_exit == '2':
                        print("\n\033[95mThank you for using Advanced Dorking Tool.\033[0m" if selected_messages == "english" else "\n\033[95mTerima kasih telah menggunakan Tool Dorking Kompleks.\033[0m")
                        sys.exit(0)
                    else:
                        print("\n\033[91mInvalid choice\033[0m" if selected_messages == "english" else "\n\033[91mPilihan tidak valid\033[0m")
            else:
                print("\n\033[91mNo results found\033[0m" if selected_messages == "english" else "\n\033[91mTidak ada hasil yang ditemukan\033[0m")
                time.sleep(2)
        except KeyboardInterrupt:
            stop_loading = True
            loading_thread.join()
            print("\n\033[91mSearch stopped by user\033[0m" if selected_messages == "english" else "\n\033[91mPencarian dihentikan oleh pengguna\033[0m")
            time.sleep(2)
            continue

def main():
    dorker = DorkingTool()
    selected_language = select_language()
    show_dork_menu(dorker, selected_language)

if __name__ == "__main__":
    main()
