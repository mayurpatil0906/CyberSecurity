from flask import Flask, render_template, jsonify
import psutil
import pandas as pd
import threading
import time

app = Flask(__name__)

# Global variables to store metrics
system_metrics_df = pd.DataFrame(columns=['CPU Usage (%)', 'Memory Usage (%)', 'Disk Usage (%)'])
network_stats = {'Bytes Sent': 0, 'Bytes Received': 0}
firewall_status = {'Firewall Active': True, 'Blocked Connections': 0, 'Allowed Connections': 0}

# Function to monitor system metrics
def get_system_metrics():
    global system_metrics_df
    while True:
        metrics = {
            'CPU Usage (%)': psutil.cpu_percent(interval=1),
            'Memory Usage (%)': psutil.virtual_memory().percent,
            'Disk Usage (%)': psutil.disk_usage('/').percent
        }
        new_metrics_df = pd.DataFrame({
            'CPU Usage (%)': [metrics['CPU Usage (%)']],
            'Memory Usage (%)': [metrics['Memory Usage (%)']],
            'Disk Usage (%)': [metrics['Disk Usage (%)']]
        })

        system_metrics_df = pd.concat([system_metrics_df, new_metrics_df], ignore_index=True)
        if len(system_metrics_df) > 10:
            system_metrics_df = system_metrics_df.tail(10)
        time.sleep(1)


# Function to get network statistics
def get_network_stats():
    global network_stats
    while True:
        net_stats = psutil.net_io_counters()
        network_stats['Bytes Sent'] = net_stats.bytes_sent
        network_stats['Bytes Received'] = net_stats.bytes_recv
        time.sleep(1)

# Function to simulate firewall health status (mock)
def get_firewall_health():
    global firewall_status
    while True:
        firewall_status['Blocked Connections'] += 1  # Mock increment
        firewall_status['Allowed Connections'] += 5  # Mock increment
        time.sleep(5)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Info route
@app.route('/info')
def info():
    return render_template('info.html')

# Network stats page
@app.route('/network')
def network():
    return render_template('network.html', network_stats=network_stats)

# API endpoint to fetch network stats data
@app.route('/api/network_stats')
def network_stats_api():
    return jsonify(network_stats)

# Firewall health page
@app.route('/firewall')
def firewall():
    return render_template('firewall.html', firewall_status=firewall_status)

# API endpoint to fetch firewall health data
@app.route('/api/firewall_status')
def firewall_status_api():
    return jsonify(firewall_status)

if __name__ == '__main__':
    # Start monitoring threads
    threading.Thread(target=get_system_metrics, daemon=True).start()
    threading.Thread(target=get_network_stats, daemon=True).start()
    threading.Thread(target=get_firewall_health, daemon=True).start()

    app.run(debug=True)
