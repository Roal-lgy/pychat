pips=pip/argparse.lock pip/colorama.lock pip/leancloud.lock pip/yaml.lock

all: $(pips) /usr/bin/pychat /usr/bin/update-pychat ~/.config/pychat/lock pychat
	@echo -e '\033[32minstalled\033[0m!!'

pychat: main.py _*py
	mv _root.py __root.py
	pyinstaller -F main.py
	cp dist/main ./pychat
	mv __root.py _root.py

/usr/bin/update-pychat:
	touch update-pychat
	echo '#!/bin/bash' > update-pychat
	echo -n 'dir=' >> update-pychat
	pwd >> update-pychat
	echo 'cd $$dir/ ; git pull' >> update-pychat
	chmod +x update-pychat
	sudo mv update-pychat /usr/bin/update-pychat

/usr/bin/pychat:
	touch _pychat
	echo '#!/bin/bash' > _pychat
	echo -n 'dir=' >> _pychat
	pwd >> _pychat
	echo 'python3 $$dir/main.py $$@' >> _pychat
	# cp main.py pychat
	chmod +x _pychat
	sudo mv _pychat /usr/bin/pychat

~/.config/pychat/lock:
	mkdir -p ~/.config/pychat
	cp example.yaml ~/.config/pychat/init.yaml
	touch ~/.config/pychat/lock

pip/argparse.lock:
	pip3 install argparse
	touch pip/argparse.lock

pip/colorama.lock:
	pip3 install colorama
	touch pip/colorama.lock

pip/leancloud.lock:
	pip3 install leancloud
	touch pip/leancloud.lock

pip/yaml.lock:
	pip3 install pyyaml
	touch pip/yaml.lock

clean:
	rm _pychat
	rm update-pychat
	mv __root.py _root.py
