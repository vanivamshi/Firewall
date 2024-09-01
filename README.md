# Firewall

A basic firewall program containing 3 files,

Client
1) Creates a TCP socket connection
2) Uses SSL/TLS for secure communication
3) Retry Mechanism - Attempts to connect to the proxy server up to a specified number of retries (MAX_RETRIES)
4) Signal Handling - handles SIGINT (Ctrl+C) to close the socket and exit
5) Communication - Sends a message to the proxy server and receives a response from the proxy server
6) Exception Handling - Catches and reports socket errors.

Proxy Server
1) Rate Limiting - Implements rate limiting to restrict the number of requests per second from a single IP address. Uses a sliding window approach to track request times
2) Logging - Logs connection details, data exchanged between client and server, rate limit violations and errors
3) Threaded Server - Uses threading to handle multiple connections simultaneously
4) Resource Management - Ensures sockets are properly closed after communication

Main Server
1) Logging - Logs connection details, data exchanged between client and server, rate limit violations and errors
2) Resource Management - Ensures the request socket is closed after communication
3) Server Monitoring - Provides basic server monitoring functionality (CPU and memory usage)

To run thr program,
1) python firewall_main_server1.py
2) python firewall_proxy_server1.py
3) python firewall_clint.py
