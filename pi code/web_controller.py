from flask import Flask, render_template_string, request, redirect, url_for
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import socket

# ---- PubNub Setup ----
pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-ffddd65a-1f76-4585-b52b-60f82d85110e"      
pnconfig.subscribe_key = "sub-c-42eb0741-66d6-49ba-b964-445def243839"    
pnconfig.uuid = "web-controller"

pubnub = PubNub(pnconfig)

# ---- Flask App ----
app = Flask(__name__)

# ---- HTML Template ----
HTML_PAGE = '''
    <h1>Traffic Light Controller</h1>
    <form action="/set" method="POST">
        <button name="color" value="RED">RED</button>
        <button name="color" value="YELLOW">YELLOW</button>
        <button name="color" value="GREEN">GREEN</button>
    </form>
'''

# ---- Publish Function ----
def send_message(color):
    pubnub.publish().channel("traffic-light/control").message({"color": color}).sync()

# ---- Routes ----
@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/set', methods=['POST'])
def set_color():
    color = request.form['color']
    send_message(color)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Get local IP address so you can access it from another device
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Traffic Light Web App is running!")
    print(f"Open in your browser: http://{local_ip}:5000")

    # Start Flask server
    app.run(debug=True, host='0.0.0.0', port=5000)