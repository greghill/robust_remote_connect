Boxes that can be difficult to establish incoming ssh connections into because of NATs, Firewalls, etc should run `field/robust_remote_connect.py [cloud_username] [cloud_ip]`. This will use `autossh` to open a `ssh -R` tunnel to a cloud server from the field box. Someone on the cloud server can connect to the box using `cloud/connect_from_cloud.sh [field_username] [field_hostname]`.

Required programs: `autossh, python3`

