import psutil
import streamlit as st
import pandas as pd
import time

# Function to monitor system metrics
def get_system_metrics():
    metrics = {
        'CPU Usage (%)': psutil.cpu_percent(interval=1),
        'Memory Usage (%)': psutil.virtual_memory().percent,
        'Disk Usage (%)': psutil.disk_usage('/').percent
    }
    return metrics

# Function to get network statistics
def get_network_stats():
    net_stats = psutil.net_io_counters()
    return {
        'Bytes Sent': net_stats.bytes_sent,
        'Bytes Received': net_stats.bytes_recv
    }

# Function to detect suspicious processes
def detect_suspicious_process():
    suspicious_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        if proc.info['cpu_percent'] > 80 or proc.info['memory_percent'] > 50:
            suspicious_processes.append(proc.info)
    return suspicious_processes

# Function to terminate a process
def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        st.success(f"Terminated process with PID: {pid}")
    except Exception as e:
        st.error(f"Failed to terminate process {pid}: {e}")

# Function to simulate firewall health status (mock)
def get_firewall_health():
    firewall_status = {
        'Firewall Active': True,
        'Blocked Connections': 10,
        'Allowed Connections': 500
    }
    return firewall_status

# Function to display log file data (mocked for now)
def display_log_data():
    logs = [
        {'Time': '2024-10-01 10:23:45', 'Event': 'Login Attempt', 'Status': 'Success'},
        {'Time': '2024-10-01 11:10:15', 'Event': 'Suspicious File Download', 'Status': 'Blocked'},
        {'Time': '2024-10-01 12:45:30', 'Event': 'Firewall Breach Attempt', 'Status': 'Prevented'},
    ]
    log_df = pd.DataFrame(logs)
    st.table(log_df)

# Main function to handle navigation
def main():
    # Navigation sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Network Stats", "Firewall Health", "Logs"])

    # Home page with real-time system metrics, suspicious process detection, and termination
    if page == "Home":
        st.title("Cybersecurity Monitoring System")
        st.header("Real-time System Monitoring")

        chart_placeholder = st.empty()  
        suspicious_placeholder = st.empty()  

        # Initialize a DataFrame for storing system metrics
        system_metrics_df = pd.DataFrame(columns=['CPU Usage (%)', 'Memory Usage (%)', 'Disk Usage (%)'])

        # Loop for real-time updating
        while True:
            # Fetch system metrics
            metrics = get_system_metrics()

            # Create a new DataFrame for the latest metrics
            new_metrics_df = pd.DataFrame({
                'CPU Usage (%)': [metrics['CPU Usage (%)']],
                'Memory Usage (%)': [metrics['Memory Usage (%)']],
                'Disk Usage (%)': [metrics['Disk Usage (%)']]
            })

            # Concatenate the new metrics DataFrame with the existing one
            system_metrics_df = pd.concat([system_metrics_df, new_metrics_df], ignore_index=True)

            # Limit the chart to the last 10 data points
            if len(system_metrics_df) > 10:
                system_metrics_df = system_metrics_df.tail(10)

            # Update the chart dynamically in the same placeholder
            with chart_placeholder.container():
                st.subheader("Real-time System Metrics")
                st.line_chart(system_metrics_df)

            # Detect suspicious processes and display them with termination options
            suspicious_processes = detect_suspicious_process()

            with suspicious_placeholder.container():
                if suspicious_processes:
                    st.warning("Suspicious Process Detected:")
                    suspicious_df = pd.DataFrame(suspicious_processes)
                    st.table(suspicious_df)

                    # Generate unique keys for buttons and allow process termination
                    for idx, row in suspicious_df.iterrows():
                        unique_key = f"terminate_button_{row['pid']}_{int(time.time())}"
                        if st.button(f"Terminate PID {row['pid']}", key=unique_key):
                            terminate_process(row['pid'])

            # Update every second
            time.sleep(1)

    # Network stats page
    elif page == "Network Stats":
        st.title("Network Statistics")
        network_stats = get_network_stats()
        st.write("Bytes Sent: ", network_stats['Bytes Sent'])
        st.write("Bytes Received: ", network_stats['Bytes Received'])

    # Firewall health page
    elif page == "Firewall Health":
        st.title("Firewall Health Status")
        firewall_status = get_firewall_health()
        st.write(f"Firewall Active: {firewall_status['Firewall Active']}")
        st.write(f"Blocked Connections: {firewall_status['Blocked Connections']}")
        st.write(f"Allowed Connections: {firewall_status['Allowed Connections']}")

    # Logs page
    elif page == "Logs":
        st.title("Logs")
        st.subheader("System Events and Security Logs")
        display_log_data()

if __name__ == "__main__":
    main()
