install: /usr/bin/pychat
	sleep 0

update:
	git pull
	sudo mv pychat /usr/bin/
	
/usr/bin/pychat:
	sudo mv pychat /usr/bin/

