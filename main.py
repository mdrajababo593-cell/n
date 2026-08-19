#!/usr/bin/env python3
# ===================================================================
# 🔥 ARIYAN BOT - ULTRA LIGHTNING FAST RECONNECT (512MB OPTIMIZED) 🔥
# ===================================================================

import subprocess
import sys
import importlib
import os
import ssl
import json
import time
import random
import asyncio
import threading
from datetime import datetime

import aiohttp
import jwt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from cfonts import render

# Protobuf files
from xPARA import *
from xHeaders import *
from Pb2 import MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2

console = Console()

# ========== CONFIG ==========
login_url, ob, version = "https://loginbp.ggpolarbear.com/", "OB54", "1.126.7"

# 🚀 লাইটওয়েট + সুপার ফাস্ট রিকানেক্ট
TIMEOUT = aiohttp.ClientTimeout(total=10, connect=5)
MAX_CONCURRENT = 10
MAX_RETRIES = 999  # কখনো স্কিপ করবে না
RECONNECT_DELAY = 0.5  # মাত্র ০.৫ সেকেন্ড

# ========== গ্লোবাল কানেক্টর ==========
connector = None
semaphore = None

def get_connector():
    global connector
    if connector is None:
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=10,
            ttl_dns_cache=60,
            force_close=True,
            enable_cleanup_closed=True
        )
    return connector

def get_semaphore():
    global semaphore
    if semaphore is None:
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    return semaphore

# ---------- HELPERS ----------
def Uaa():
    versions = ['5.0.1B2','5.1.0P1','5.2.0B1']
    models = ['SM-A125F','Redmi 9A','POCO M3','SM-G998B']
    android = random.choice(['11','12','13'])
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {android};en-US;USA;)"

Hr = {
    'User-Agent': Uaa(),
    'Connection': "close",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': ob
}

def get_random_color():
    colors = ["[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]"]
    return random.choice(colors)

async def EnC_Vr(N):
    if N<0: return b''
    H = []
    while True:
        RedZed = N & 0x7F
        N >>= 7
        if N: RedZed |= 0x80
        H.append(RedZed)
        if not N: break
    return bytes(H)

async def CrEaTe_VarianT(fn, val):
    return await EnC_Vr((fn<<3)|0) + await EnC_Vr(val)

async def CrEaTe_LenGTh(fn, val):
    ev = val.encode() if isinstance(val,str) else val
    return await EnC_Vr((fn<<3)|2) + await EnC_Vr(len(ev)) + ev

async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for f,v in fields.items():
        if isinstance(v,list):
            for item in v:
                if isinstance(item, dict):
                    nested = await CrEaTe_ProTo(item)
                    packet.extend(await CrEaTe_LenGTh(f, nested))
        elif isinstance(v,dict):
            nested = await CrEaTe_ProTo(v)
            packet.extend(await CrEaTe_LenGTh(f, nested))
        elif isinstance(v,int):
            packet.extend(await CrEaTe_VarianT(f,v))
        elif isinstance(v,(str,bytes)):
            packet.extend(await CrEaTe_LenGTh(f,v))
    return bytes(packet)

async def DecodE_HeX(H):
    F = str(hex(H))[2:]
    return "0"+F if len(F)==1 else F

async def EnC_PacKeT(HeX, K, V):
    cipher = AES.new(K, AES.MODE_CBC, V)
    return cipher.encrypt(pad(bytes.fromhex(HeX),16)).hex()

async def GeneRaTePk(Pk, N, K, V):
    PkEnc = await EnC_PacKeT(Pk, K, V)
    _ = await DecodE_HeX(len(PkEnc)//2)
    HeadEr = N+"000000" if len(_)==2 else N+"00000" if len(_)==3 else N+"0000" if len(_)==4 else N+"000"
    return bytes.fromhex(HeadEr+_+PkEnc)


# ========== OB54 রুম প্যাকেট মেকার ==========
async def build_room_packet(room_name, key, iv):
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 3,
            4: room_name,
            6: 8,
            7: 30,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 36981056,
            15: [
                {
                    1: "IDC1",
                    2: 3000,
                    3: "BD"
                },
                {
                    1: "IDC2",
                    2: 3000,
                    3: "BD"
                }
            ]
        }
    }
    proto_data = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_data.hex(), '0e0b', key, iv)


# ========== LOGIN & AUTH ==========
async def GeNeRaTeAccAccess(uid, password, session):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host":"100067.connect.garena.com",
        "User-Agent":Uaa(),
        "Content-Type":"application/x-www-form-urlencoded",
        "Connection":"close"
    }
    data = {
        "uid":uid,
        "password":password,
        "response_type":"token",
        "client_type":"2",
        "client_secret":"2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id":"100067"
    }
    try:
        async with session.post(url, headers=headers, data=data, timeout=5) as resp:
            if resp.status != 200:
                return None, None
            data = await resp.json()
            return data.get("open_id"), data.get("access_token")
    except Exception:
        return None, None

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 2
    major_login.client_version = "1.126.7"
    major_login.client_version_code = "2024010012"
    major_login.system_software = "Android OS 11 / API-30 (RQ3A.210805.001)"
    major_login.system_hardware = "Handheld"    
    major_login.device_type = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1080
    major_login.screen_height = 2400
    major_login.screen_dpi = "440"
    major_login.processor_details = "ARMv8"
    major_login.memory = 6144
    major_login.gpu_renderer = "Adreno (TM) 650"
    major_login.gpu_version = "OpenGL ES 3.2 V@1.50"
    major_login.graphics_api = "OpenGLES3"
    major_login.supported_astc_bitset = 16383
    major_login.unique_device_id = f"Google|{random.randint(10000000,99999999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(100000000000,999999999999)}"
    major_login.client_ip = ""
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    
    major_login.memory_available.version = 55
    major_login.memory_available.hidden_value = 81
    
    major_login.access_token = access_token
    major_login.platform_sdk_id = 2
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = random.randint(120000, 130000)
    major_login.external_storage_available = random.randint(38000, 52000)
    major_login.internal_storage_total = random.randint(100000, 120000)
    major_login.internal_storage_available = random.randint(18000, 32000)
    major_login.game_disk_storage_available = random.randint(18000, 28080)
    major_login.external_sdcard_avail_storage = random.randint(28080, 60000)
    major_login.external_sdcard_total_storage = random.randint(110000, 130000)
    major_login.login_by = 3
    major_login.library_path = "/data/app/~~random/base.apk"
    major_login.reg_avatar = 1
    major_login.library_token = "hash|base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.login_open_id_type = 4
    major_login.loading_time = random.randint(9000, 18000)
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTy3KUhvha/qugOBot9Bf7gcwqrf2btWC5rnrKZxrHIxEFfgxmPVkTxN+2dHiSprlxvm2Kl6o8EEgBJy7FzLLpbARlcqc2f/GQz+6UsLSMGXd"
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 0
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    
    string = major_login.SerializeToString()
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(string, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def MajorLogin(payload, session):
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    try:
        async with session.post(login_url+"MajorLogin", data=payload, headers=Hr, ssl=ssl_ctx, timeout=5) as resp:
            if resp.status == 200:
                return await resp.read()
            return None
    except Exception:
        return None

async def GetLoginData(base_url, payload, token, session):
    headers = Hr.copy()
    headers['Authorization'] = f"Bearer {token}"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    try:
        async with session.post(f"{base_url}/GetLoginData", data=payload, headers=headers, ssl=ssl_ctx, timeout=5) as resp:
            if resp.status == 200:
                return await resp.read()
            return None
    except Exception:
        return None

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_packet = await EnC_PacKeT(token.encode().hex(), key, iv)
    encrypted_packet_length = hex(len(encrypted_packet)//2)[2:]
    headers = '0000000'
    if uid_length==8: headers = '00000000'
    elif uid_length==10: headers = '000000'
    elif uid_length==7: headers = '000000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"


# ========== LIGHTNING FAST BOT ==========
class FreeFireBot:
    def __init__(self, uid, password, server='bd'):
        self.uid = uid
        self.password = password
        self.server = server
        self.is_running = True
        self.online_writer = None
        self.reader = None
        self.key = None
        self.iv = None
        self.region = None
        self.tasks = []
        self.is_online = False
        self.Nm = "Unknown"
        self.session = None
        self.room_created = False
        self.reconnect_count = 0
        self.last_online_time = 0

    async def tcp_online(self, ip, port, auth_token):
        while self.is_running:
            try:
                # সুপার ফাস্ট কানেকশন
                reader, writer = await asyncio.open_connection(ip, int(port))
                writer.write(bytes.fromhex(auth_token))
                await writer.drain()
                self.reader = reader
                self.online_writer = writer
                self.is_online = True
                self.reconnect_count = 0
                self.last_online_time = time.time()
                
                # রুম তৈরি (শুধু একবার)
                if not self.room_created and self.key and self.iv:
                    selected_color = get_random_color()
                    room_name = f"—͞[B]{selected_color}Ⓥ"
                    room_pkt = await build_room_packet(room_name, self.key, self.iv)
                    writer.write(room_pkt)
                    await writer.drain()
                    self.room_created = True
                    
                    console.print(Panel(
                        f"[bold green]🆔 UID     ::[/bold green] {self.uid}\n"
                        f"[bold green]👤 নাম     ::[/bold green] {self.Nm}\n"
                        f"[bold green]🏠 রুম     ::[/bold green] {room_name}\n"
                        f"[bold green]🌐 IP      ::[/bold green] {ip}:{port}",
                        title="[bold bright_green]✅ অনলাইন[/bold bright_green]",
                        border_style="bright_green",
                        expand=False
                    ))
                
                # কানেকশন লাইভ রাখা - তাত্ক্ষণিক রিকানেক্টের জন্য
                while self.is_running and self.is_online:
                    try:
                        # দ্রুত ডেটা চেক
                        data = await asyncio.wait_for(self.reader.read(65536), timeout=2.0)
                        if data:
                            # ডেটা পেলে কিছু করা যায় না
                            pass
                    except asyncio.TimeoutError:
                        # টাইমআউট হলে কানেকশন চেক
                        if self.is_online:
                            # সব ঠিক আছে
                            continue
                    except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError, OSError):
                        # কানেকশন ড্রপ - সাথে সাথে রিকানেক্ট
                        break
                    except Exception:
                        break
                
                # কানেকশন ড্রপ হলে সাথে সাথে রিকানেক্ট
                if self.is_running:
                    console.print(f"[yellow]🔄 UID {self.uid} - রিকানেক্ট হচ্ছে...[/yellow]")
                
            except Exception as e:
                if self.is_running:
                    console.print(f"[red]⚠️ UID {self.uid} - রিকানেক্ট: {e}[/red]")
            
            # ক্লিনআপ
            self.online_writer = None
            self.reader = None
            self.is_online = False
            
            # তাত্ক্ষণিক রিকানেক্ট - মাত্র ০.৫ সেকেন্ড
            await asyncio.sleep(RECONNECT_DELAY)

    async def tcp_chat(self, ip, port, auth_token, key, iv, ready_event):
        while self.is_running:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                writer.write(bytes.fromhex(auth_token))
                await writer.drain()
                ready_event.set()
                
                while self.is_running:
                    try:
                        data = await asyncio.wait_for(reader.read(4096), timeout=2.0)
                        if not data:
                            break
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        break
                        
            except Exception:
                pass
            await asyncio.sleep(RECONNECT_DELAY)

    async def try_login(self, session):
        try:
            # ফাস্ট লগইন
            open_id, access_token = await GeNeRaTeAccAccess(self.uid, self.password, session)
            if not open_id:
                return False
                
            payload = await EncRypTMajoRLoGin(open_id, access_token)
            response = await MajorLogin(payload, session)
            if not response:
                return False
                
            auth_data = MajoRLoGinrEs_pb2.MajorLoginRes()
            auth_data.ParseFromString(response)
            
            login_data = await GetLoginData(auth_data.url, payload, auth_data.token, session)
            if not login_data:
                return False
                
            port_data = PorTs_pb2.GetLoginData()
            port_data.ParseFromString(login_data)
            
            self.key = auth_data.key
            self.iv = auth_data.iv
            self.region = auth_data.region
            
            try:
                dec_jwt = jwt.decode(auth_data.token, options={"verify_signature": False})
                self.Nm = dec_jwt.get('nickname') or "Unknown"
            except Exception:
                self.Nm = "Unknown"
            
            online_ip, online_port = port_data.Online_IP_Port.split(":")
            chat_ip, chat_port = port_data.AccountIP_Port.split(":")
            
            auth_token = await xAuThSTarTuP(
                auth_data.account_uid, 
                auth_data.token, 
                auth_data.timestamp, 
                auth_data.key, 
                auth_data.iv
            )
            
            ready = asyncio.Event()
            t1 = asyncio.create_task(
                self.tcp_chat(chat_ip, chat_port, auth_token, auth_data.key, auth_data.iv, ready)
            )
            self.tasks.append(t1)
            await ready.wait()
            
            t2 = asyncio.create_task(
                self.tcp_online(online_ip, online_port, auth_token)
            )
            self.tasks.append(t2)
            
            await asyncio.gather(t1, t2, return_exceptions=True)
            
            return True
            
        except Exception:
            return False

    async def keep_online_forever(self):
        connector = get_connector()
        semaphore = get_semaphore()
        
        async with semaphore:
            async with aiohttp.ClientSession(timeout=TIMEOUT, connector=connector) as session:
                self.session = session
                
                while self.is_running:
                    try:
                        # লগইন চেষ্টা
                        login_success = await self.try_login(session)
                        
                        if login_success:
                            console.print(f"[green]✅ UID {self.uid} - অনলাইন[/green]")
                            # অনলাইন থাকা অবস্থায় প্রতি ২ সেকেন্ড পর চেক
                            await asyncio.sleep(2)
                        else:
                            # ব্যর্থ হলে সাথে সাথে পুনরায় চেষ্টা
                            console.print(f"[yellow]⚠️ UID {self.uid} - পুনরায় চেষ্টা...[/yellow]")
                            await asyncio.sleep(RECONNECT_DELAY)
                            
                    except Exception as e:
                        console.print(f"[red]❌ UID {self.uid} - এরর: {e}[/red]")
                        await asyncio.sleep(RECONNECT_DELAY)


# ========== ACCOUNT LOADER ==========
async def load_and_start():
    accounts = []
    
    filename = "bd.txt"
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and ":" in line:
                        uid, pwd = line.split(":")[:2]
                        accounts.append((int(uid.strip()), pwd.strip(), "bd"))
        except Exception as e:
            console.print(f"[bold red]⚠️ {filename} লোড এরর: {e}[/bold red]")
    else:
        console.print(f"[bold yellow]⚠️ {filename} ফাইল পাওয়া যায়নি![/bold yellow]")
    
    return accounts


# ========== STARTUP ==========
async def main_async():
    print(render('ARIYAN', colors=['white', 'red'], align='center'))
    
    accounts = await load_and_start()
    if not accounts:
        console.print(Panel(
            "[bold red]কোনো আইডি পাওয়া যায়নি![/bold red]\n"
            "bd.txt ফাইলে UID:PASSWORD যোগ করুন",
            title="[bold red]❌ NO ACCOUNTS[/bold red]",
            border_style="red",
            expand=False
        ))
        return

    total_accounts = len(accounts)
    
    startup_text = (
        f"[bold cyan]👥 মোট আইডি        ::[/bold cyan] {total_accounts} টি\n"
        f"[bold cyan]🔢 কনকারেন্ট       ::[/bold cyan] {MAX_CONCURRENT} টি\n"
        f"[bold cyan]⚡ রিকানেক্ট       ::[/bold cyan] {RECONNECT_DELAY} সেকেন্ড\n"
        f"[bold cyan]💾 RAM প্রয়োজন    ::[/bold cyan] ~512MB\n"
        f"[bold cyan]🏠 রুমের নাম       ::[/bold cyan] ARIYAN"
    )
    console.print(Panel(
        Align.center(startup_text), 
        title="[bold red]🛡️ ARIYAN LIGHTNING FAST 🛡️[/bold red]", 
        border_style="bright_red", 
        padding=(1, 2), 
        expand=False
    ))

    # সব আইডি একসাথে স্টার্ট
    tasks = []
    for uid, pwd, server in accounts:
        bot = FreeFireBot(uid=uid, password=pwd, server=server)
        task = asyncio.create_task(bot.keep_online_forever())
        tasks.append(task)
        await asyncio.sleep(0.1)
    
    await asyncio.gather(*tasks, return_exceptions=True)

def main():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main_async())
    except KeyboardInterrupt:
        console.print("\n[bold red]🛑 বন্ধ করা হচ্ছে...[/bold red]")
    finally:
        global connector
        if connector:
            loop.run_until_complete(connector.close())
        loop.close()

if __name__ == "__main__":
    main()
