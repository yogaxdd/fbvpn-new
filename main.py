import os
import requests
import random
import string
import time
import threading
from datetime import datetime
from threading import Barrier

# === 🧹 BERSIHIN TERMINAL DI AWAL (kayak clear) ===
os.system("cls" if os.name == "nt" else "clear")

def random_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@yogaxdmail.id"

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def random_otp():
    return ''.join(random.choices(string.digits, k=6))

def register(ref_code, use_proxy, use_random_ua, ua_list, proxy_list):
    try:
        session = requests.Session()
        # User-Agent
        if use_random_ua and ua_list:
            user_agent = random.choice(ua_list)
        else:
            user_agent = "Mozilla/5.0 (Linux; Android 11; Redmi Note 11) AppleWebKit/537.36 Chrome/137.0.0.0 Mobile Safari/537.36"
        session.headers.update({
            "User-Agent": user_agent,
            "X-Requested-With": "XMLHttpRequest"
        })
        # Proxy
        proxies = None
        if use_proxy and proxy_list:
            proxy = random.choice(proxy_list)
            proxies = {"http": proxy, "https": proxy}
        session.get(f"https://distribute.flashbacktochina.com/index.php?s=/wap/track/enter&code={ref_code}", proxies=proxies)
        email = random_email()
        password = random_password()
        otp = random_otp()
        register_url = "https://distribute.flashbacktochina.com/index.php?s=/wap/login/register"
        data = {
            "email": email,
            "captcha": otp,
            "password": password,
            "cfpassword": password
        }
        r = session.post(register_url, data=data, proxies=proxies)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "成功" in r.text or "memuat" in r.text or "应用" in r.text:
            print(f"✅ Sukses: {email} | {password}, Waktu Sekarang: {now}")
            with open("akun.txt", "a") as f:
                f.write(f"{email}:{password} | Daftar: {now} | Exp: 3 Hari\n")
        else:
            print(f"❌ Gagal: {email} | Respon: {r.text[:100]}")
    except Exception as e:
        print(f"🚫 ERROR: {e}")

def batch_akun(ref_code, use_proxy, use_random_ua, ua_list, proxy_list, jumlah_akun):
    akun_dibuat = 0
    while akun_dibuat < jumlah_akun:
        batch = min(5, jumlah_akun - akun_dibuat)
        threads = []
        for _ in range(batch):
            t = threading.Thread(target=register, args=(ref_code, use_proxy, use_random_ua, ua_list, proxy_list))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        akun_dibuat += batch
        if akun_dibuat < jumlah_akun:
            input("\nLimit IP, Silahkan Ganti IP Untuk Melanjutkan, Tekan Enter Jika Sudah Ganti IP...")

# === UI / HEADER ===
print("""
                                                        $$\ 
                                                        $$ |
$$\   $$\  $$$$$$\   $$$$$$\   $$$$$$\  $$\   $$\  $$$$$$$ |
$$ |  $$ |$$  __$$\ $$  __$$\  \____$$\ \$$\ $$  |$$  __$$ |
$$ |  $$ |$$ /  $$ |$$ /  $$ | $$$$$$$ | \$$$$  / $$ /  $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$  __$$ | $$  $$<  $$ |  $$ |
\$$$$$$$ |\$$$$$$  |\$$$$$$$ |\$$$$$$$ |$$  /\$$\ \$$$$$$$ |
\____$$ | \______/  \____$$ | \_______|\__/  \__| \_______|
$$\   $$ |          $$\   $$ |                              
\$$$$$$  |          \$$$$$$  |                              
\______/            \______/                               
""")
print("================== Bot Flashback ==========================")

# === INPUT ===
ref_code = input("Referral Code (tanpa link): ").strip()
jumlah_akun = int(input("Jumlah akun: "))
print("(Batch 5 akun paralel, lalu pause ganti IP)")

# User Agent dan Proxy
use_proxy = input("Apakah memakai proxy (y/n)? ").strip().lower() == 'y'
use_random_ua = input("Apakah random user agent? (y/n)? ").strip().lower() == 'y'
ua_list = []
proxy_list = []
if use_random_ua:
    if os.path.exists("ua.txt"):
        with open("ua.txt", "r") as f:
            ua_list = [line.strip() for line in f if line.strip()]
    else:
        print("File ua.txt tidak ditemukan! Random UA dinonaktifkan.")
        use_random_ua = False
if use_proxy:
    if os.path.exists("proxy.txt"):
        with open("proxy.txt", "r") as f:
            proxy_list = [line.strip() for line in f if line.strip()]
    else:
        print("File proxy.txt tidak ditemukan! Proxy dinonaktifkan.")
        use_proxy = False

# Jalankan batch_akun
batch_akun(ref_code, use_proxy, use_random_ua, ua_list, proxy_list, jumlah_akun)
print("\n🎉 Semua akun selesai dibuat.")
