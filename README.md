XSScan

XSScan is a simple XSS scanner reflected

Compatibility Linux && Windows

Requirements :

- Python3
- Python3 modules : regex, colorama, seleniuù 
- chromedriver

Linux Installation

1) Download and install google chrome

- sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
- sudo apt install ./google-chrome-stable_current_amd64.deb

2) Download XSScan

- sudo git clone http://github.com/Reng-Deng-DenG/XSScan/
- sudo chmod -R 777 XSScan/

3) Give chromedriver right

- sudo chmod 777 /usr/bin/chromedriver

4) Edit chromedriver path in xsscan.py at line 30

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=chrome_options)

5) Install python module

- sudo pip3 install selenium colorama regex

6) Start XSScan

- sudo python3 xsscan.py


Windows installation

1) Download chromedriver

- https://chromedriver.chromium.org/downloads

2) Edit chromedriver path in xsscan.py at line 30

driver = webdriver.Chrome(executable_path="C:\\\Users\\\lucas-pc\\\Desktop\\\XSScan\\\chromedriver.exe", options=chrome_options)

3) Start XSScan

- sudo python3 xsscan.py





