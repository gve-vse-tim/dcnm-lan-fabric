# dcnmctl Usage

dcnmctl global CLI options
- --dcnm_host, env DCNM_HOST : IP or FQDN of DCNM server
- --dcnm_user, env DCNM_USER : username for DCNM server credentials
- --dcnm_pass, env DCNM_PASS : password for DCNM server credentials
- --dcnm_verify, env DCNM_VERIFY : (boolean/flag) if specified, require valid TLS. Default is false (don't verify)
- --sw_user, env SW_USER : username for switch credentials
- --sw_pass, env SW_PASS : password for switch credentials

Example:

dcnmctl --dcnm_host 100.100.100.100 --dcnm_user admin --dcnm_pass password --dcnm_verify ....

## Switch Management

dcnmctl [global opts] switch add poap FABRIC SW_SER_NUM SW_NAME SW_MGMT0_IP --sw_user SW_USER --sw_pass SW_PASS 
    Note: this will look for a switch with the specified serial number in POAP phase and set the
    switch hostname, mgmt0 IP address, username, and password to the provided values. 

dcnmctl [global opts] switch add discover FABRIC SW_MGMT0_IP --sw_user SW_USER --sw_pass SW_PASS
    Note: unlike the GUI, it's not practical to walk the network via CLI.  So this CLI is essentially a
    direct add of a single switch given that switch's mgmt0 IP address.

dcnmctl [glboal opts] switch delete FABRIC SW_SER_NUM

dcnmctl [global opts] switch role FABRIC SW_NAME SW_ROLE
