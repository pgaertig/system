# Install

    asdf plugin-add python
    asdf install python
    pip3 -r requirements.txt
    
# Use

Automated AnyConnect VPN login (customized). To be used with OpenConnect.
Example:

    ./webvpn-login.py USER@COMPANY.com 'https://YOUR-VPN-HOST/+CSCOE+/logon.html' /tmp/vpncookie && cat /tmp/vpncookie | sudo time openconnect -v --cookie-on-stdin YOUR-VPN-HOST

License: GPL 3.0