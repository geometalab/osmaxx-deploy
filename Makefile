tests:
	vagrant up
	vagrant provision
	sleep 10
	fab -H osmaxx-local-testing-server bootstrap
