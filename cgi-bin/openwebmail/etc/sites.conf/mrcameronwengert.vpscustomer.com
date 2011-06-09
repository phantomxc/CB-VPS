mailspooldir	/var/spool/vmail/mrcameronwengert.vpscustomer.com/mail
auth_withdomain	yes
auth_module	auth_pop3_hspc.pl
virtusertable /dev/null
