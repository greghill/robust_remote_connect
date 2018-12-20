Boxes that can be difficult to establish incoming ssh connections into because of NATs, Firewalls, etc should run `field/robust_remote_connect.py [cloud_username] [cloud_ip]`. This will use `autossh` to open a `ssh -R` tunnel to a cloud server from the field box. Someone on the cloud server can connect to the box using `cloud/connect_from_cloud.sh [field_username] [field_hostname]`.

Required programs: `autossh, python3

also you need: sshd (you need to be able to call ssh localhost and it should either let you in or reject your keys. Make sure to set "PasswordAuthentication no" in /etc/ssh/sshd_config, you should not be able to log in with your password (bad security to let outside people do that))

