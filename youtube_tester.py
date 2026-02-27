"""
YouTube Download Tester - يجرب كل الطرق ويكمل حتى لو نجحت
"""

import os
import subprocess
import json
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("youtube_test_results.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

TEST_URL = "https://www.youtube.com/shorts/P6oR9gaFL24"
OUTPUT_DIR = "test_downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []
successful_methods = []
failed_methods = []

def log_result(method_name, success, reason=""):
    status = "✅ نجح" if success else "❌ فشل"
    log.info(f"{status} | {method_name} | {reason}")
    results.append({"method": method_name, "success": success, "reason": reason})
    if success:
        successful_methods.append(method_name)
    else:
        failed_methods.append(method_name)

def try_method(name, func):
    log.info(f"\n{'='*60}")
    log.info(f"🔄 [{name}]")
    log.info(f"{'='*60}")
    try:
        result = func()
        if result and os.path.exists(result) and os.path.getsize(result) > 10000:
            size_mb = os.path.getsize(result) / (1024*1024)
            log_result(name, True, f"حجم: {size_mb:.2f} MB")
            try: os.remove(result)
            except: pass
        else:
            log_result(name, False, "الملف غير موجود أو فارغ")
    except Exception as e:
        log_result(name, False, str(e)[:300])
    time.sleep(1)

import yt_dlp

BASE = {'format': 'best[height<=480]/best', 'noplaylist': True, 'quiet': False}

def dl(num, extra=None):
    opts = {**BASE, 'outtmpl': f'{OUTPUT_DIR}/m{num}.%(ext)s'}
    if extra: opts.update(extra)
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(TEST_URL, download=True)
        return f"{OUTPUT_DIR}/m{num}.{info.get('ext','mp4')}"

# ===== Player Clients =====
def m01(): return dl(1)
def m02(): return dl(2,  {'extractor_args': {'youtube': {'player_client': ['android']}}})
def m03(): return dl(3,  {'extractor_args': {'youtube': {'player_client': ['ios']}}})
def m04(): return dl(4,  {'extractor_args': {'youtube': {'player_client': ['web']}}})
def m05(): return dl(5,  {'extractor_args': {'youtube': {'player_client': ['tv_embedded']}}})
def m06(): return dl(6,  {'extractor_args': {'youtube': {'player_client': ['mweb']}}})
def m07(): return dl(7,  {'extractor_args': {'youtube': {'player_client': ['android_embedded']}}})
def m08(): return dl(8,  {'extractor_args': {'youtube': {'player_client': ['android_music']}}})
def m09(): return dl(9,  {'extractor_args': {'youtube': {'player_client': ['web_embedded']}}})
def m10(): return dl(10, {'extractor_args': {'youtube': {'player_client': ['android_creator']}}})
def m11(): return dl(11, {'extractor_args': {'youtube': {'player_client': ['ios', 'android']}}})
def m12(): return dl(12, {'extractor_args': {'youtube': {'player_client': ['android', 'web']}}})
def m13(): return dl(13, {'extractor_args': {'youtube': {'player_client': ['ios', 'web']}}})
def m14(): return dl(14, {'extractor_args': {'youtube': {'player_client': ['tv_embedded', 'android']}}})
def m15(): return dl(15, {'extractor_args': {'youtube': {'player_client': ['web', 'android', 'ios']}}})
def m16(): return dl(16, {'extractor_args': {'youtube': {'player_client': ['android'], 'player_skip': ['webpage']}}})
def m17(): return dl(17, {'extractor_args': {'youtube': {'player_client': ['ios'], 'player_skip': ['webpage']}}})
def m18(): return dl(18, {'extractor_args': {'youtube': {'player_client': ['mweb', 'android']}}})
def m19(): return dl(19, {'extractor_args': {'youtube': {'player_client': ['android_embedded', 'ios']}}})
def m20(): return dl(20, {'extractor_args': {'youtube': {'player_client': ['android_music', 'ios']}}})

# ===== Formats =====
def m21(): return dl(21, {'format': 'worst'})
def m22(): return dl(22, {'format': 'best[height<=360]'})
def m23(): return dl(23, {'format': 'best[height<=240]'})
def m24(): return dl(24, {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'})
def m25(): return dl(25, {'format': '18'})
def m26(): return dl(26, {'format': '17'})
def m27(): return dl(27, {'format': 'best[ext=mp4]'})
def m28(): return dl(28, {'format': 'worst[ext=mp4]'})
def m29(): return dl(29, {'format': 'worst', 'extractor_args': {'youtube': {'player_client': ['android']}}})
def m30(): return dl(30, {'format': 'worst', 'extractor_args': {'youtube': {'player_client': ['ios']}}})

# ===== User Agents =====
UAS = [
    ("31", "Windows Chrome",  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"),
    ("32", "iPhone Safari",   "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"),
    ("33", "Android Chrome",  "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0"),
    ("34", "Mac Chrome",      "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/120.0.0.0"),
    ("35", "Android YT App",  "com.google.android.youtube/19.09.37 (Linux; U; Android 13; en_US) gzip"),
    ("36", "iOS YT App",      "com.google.ios.youtube/19.09.3 (iPhone16,2; U; CPU iOS 17_0 like Mac OS X)"),
    ("37", "Linux Chrome",    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"),
    ("38", "Firefox",         "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"),
    ("39", "iPad Safari",     "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15"),
    ("40", "Dalvik Android",  "Dalvik/2.1.0 (Linux; U; Android 13; Pixel 7 Build/TQ3A.230901.001)"),
]

ua_methods = []
for num, label, ua in UAS:
    def make_ua(n, u):
        def method(): return dl(int(n), {'http_headers': {'User-Agent': u}})
        return method
    ua_methods.append((f"{num} - UA {label}", make_ua(num, ua)))

# ===== Sleep & Retry =====
def m41(): return dl(41, {'sleep_interval': 2, 'extractor_args': {'youtube': {'player_client': ['android']}}})
def m42(): return dl(42, {'sleep_interval': 2, 'extractor_args': {'youtube': {'player_client': ['ios']}}})
def m43(): return dl(43, {'retries': 10, 'extractor_args': {'youtube': {'player_client': ['android']}}})
def m44(): return dl(44, {'retries': 10, 'extractor_args': {'youtube': {'player_client': ['ios']}}})
def m45(): return dl(45, {'ignoreerrors': True, 'extractor_args': {'youtube': {'player_client': ['android']}}})
def m46(): return dl(46, {'ignoreerrors': True, 'format': 'worst'})
def m47(): return dl(47, {'sleep_interval': 3, 'retries': 5, 'format': 'worst'})
def m48(): return dl(48, {'fragment_retries': 10, 'extractor_args': {'youtube': {'player_client': ['android']}}})
def m49(): return dl(49, {'no_check_certificates': True, 'extractor_args': {'youtube': {'player_client': ['android']}}})
def m50(): return dl(50, {'no_check_certificates': True, 'format': 'worst'})

# ===== Subprocess =====
def m_sub1():
    out = f"{OUTPUT_DIR}/msub1.mp4"
    subprocess.run(["yt-dlp", TEST_URL, "-o", out, "-f", "worst", "--no-playlist"], check=True)
    return out

def m_sub2():
    out = f"{OUTPUT_DIR}/msub2.mp4"
    subprocess.run(["yt-dlp", TEST_URL, "-o", out, "--extractor-args", "youtube:player_client=android", "-f", "worst"], check=True)
    return out

def m_sub3():
    out = f"{OUTPUT_DIR}/msub3.mp4"
    subprocess.run(["yt-dlp", TEST_URL, "-o", out, "--extractor-args", "youtube:player_client=ios", "-f", "worst"], check=True)
    return out

def m_sub4():
    out = f"{OUTPUT_DIR}/msub4.mp4"
    subprocess.run(["yt-dlp", TEST_URL, "-o", out, "--no-check-certificates", "-f", "worst"], check=True)
    return out

# ===== Invidious =====
INVIDIOUS = [
    "https://invidious.snopyta.org",
    "https://vid.puffyan.us",
    "https://invidious.kavin.rocks",
    "https://yt.artemislena.eu",
    "https://invidious.flokinet.to",
    "https://invidious.projectsegfau.lt",
    "https://inv.riverside.rocks",
    "https://invidious.tiekoetter.com",
    "https://yewtu.be",
    "https://invidious.privacyredirect.com",
]

def make_inv(instance, num):
    def method():
        url = f"{instance}/watch?v=P6oR9gaFL24"
        with yt_dlp.YoutubeDL({**BASE, 'outtmpl': f'{OUTPUT_DIR}/m{num}.%(ext)s'}) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{OUTPUT_DIR}/m{num}.{info.get('ext','mp4')}"
    return method

# ===== Piped =====
PIPED = [
    "https://piped.video",
    "https://piped.kavin.rocks",
    "https://piped.adminforge.de",
    "https://piped.privacyredirect.com",
    "https://piped.projectsegfau.lt",
]

def make_piped(instance, num):
    def method():
        url = f"{instance}/watch?v=P6oR9gaFL24"
        with yt_dlp.YoutubeDL({**BASE, 'outtmpl': f'{OUTPUT_DIR}/m{num}.%(ext)s'}) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{OUTPUT_DIR}/m{num}.{info.get('ext','mp4')}"
    return method

# ===== تجميع كل الطرق =====
ALL_METHODS = [
    ("01 - Default",              m01),
    ("02 - Android",              m02),
    ("03 - iOS",                  m03),
    ("04 - Web",                  m04),
    ("05 - TV Embedded",          m05),
    ("06 - Mobile Web",           m06),
    ("07 - Android Embedded",     m07),
    ("08 - Android Music",        m08),
    ("09 - Web Embedded",         m09),
    ("10 - Android Creator",      m10),
    ("11 - iOS+Android",          m11),
    ("12 - Android+Web",          m12),
    ("13 - iOS+Web",              m13),
    ("14 - TV+Android",           m14),
    ("15 - Web+Android+iOS",      m15),
    ("16 - Android SkipPage",     m16),
    ("17 - iOS SkipPage",         m17),
    ("18 - Mweb+Android",         m18),
    ("19 - AndroidEmbed+iOS",     m19),
    ("20 - AndroidMusic+iOS",     m20),
    ("21 - Format worst",         m21),
    ("22 - Format 360p",          m22),
    ("23 - Format 240p",          m23),
    ("24 - Format mp4+m4a",       m24),
    ("25 - Format ID 18",         m25),
    ("26 - Format ID 17",         m26),
    ("27 - Best mp4",             m27),
    ("28 - Worst mp4",            m28),
    ("29 - Worst+Android",        m29),
    ("30 - Worst+iOS",            m30),
    ("41 - Android+Sleep",        m41),
    ("42 - iOS+Sleep",            m42),
    ("43 - Android+Retry",        m43),
    ("44 - iOS+Retry",            m44),
    ("45 - Android+IgnoreErr",    m45),
    ("46 - Worst+IgnoreErr",      m46),
    ("47 - Worst+Sleep+Retry",    m47),
    ("48 - Android+FragRetry",    m48),
    ("49 - Android+NoCert",       m49),
    ("50 - Worst+NoCert",         m50),
    ("SUB1 - Subprocess Default", m_sub1),
    ("SUB2 - Subprocess Android", m_sub2),
    ("SUB3 - Subprocess iOS",     m_sub3),
    ("SUB4 - Subprocess NoCert",  m_sub4),
]

# إضافة User Agents
ALL_METHODS.extend(ua_methods)

# إضافة Invidious
for i, inst in enumerate(INVIDIOUS):
    ALL_METHODS.append((f"INV{i+1:02d} - {inst}", make_inv(inst, 100+i)))

# إضافة Piped
for i, inst in enumerate(PIPED):
    ALL_METHODS.append((f"PIP{i+1:02d} - {inst}", make_piped(inst, 110+i)))

# ===== التشغيل =====
def run_all():
    log.info("\n" + "🚀="*30)
    log.info(f"إجمالي الطرق للاختبار: {len(ALL_METHODS)}")
    log.info(f"الرابط: {TEST_URL}")
    log.info("🚀="*30 + "\n")

    for name, func in ALL_METHODS:
        try_method(name, func)

    log.info("\n" + "="*60)
    log.info("📊 التقرير النهائي")
    log.info("="*60)
    log.info(f"\n✅ ناجحة ({len(successful_methods)}/{len(ALL_METHODS)}):")
    for m in successful_methods:
        log.info(f"  ✅ {m}")
    log.info(f"\n❌ فاشلة ({len(failed_methods)}/{len(ALL_METHODS)}):")
    for m in failed_methods:
        log.info(f"  ❌ {m}")

    with open("youtube_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "total": len(ALL_METHODS),
            "successful_count": len(successful_methods),
            "failed_count": len(failed_methods),
            "successful": successful_methods,
            "failed": failed_methods,
            "details": results
        }, f, ensure_ascii=False, indent=2)

    log.info("\n💾 النتائج في: youtube_test_results.json + youtube_test_results.log")

if __name__ == "__main__":
    run_all()
    print(f"\n{'='*50}")
    print(f"✅ نجح: {len(successful_methods)} طريقة")
    print(f"❌ فشل: {len(failed_methods)} طريقة")
    if successful_methods:
        print("\n🏆 الطرق الناجحة:")
        for m in successful_methods:
            print(f"  ✅ {m}")
    else:
        print("\n😢 كل الطرق فشلت على هذا السيرفر")
