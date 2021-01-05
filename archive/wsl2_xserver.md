# Resolving issues with X Server in WSL2

## Error: /etc/machine-id contains 0 characters (32 were expected).

Solution ([source](https://askubuntu.com/a/1149989)):
```
sudo systemd-machine-id-setup
```
 
## Error: Unable to open X display.
This is what worked for me ([source](https://stackoverflow.com/questions/61110603/how-to-set-up-working-x11-forwarding-on-wsl2)):
1. Add the following two lines to your `~/.bashrc`:
```
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
export LIBGL_ALWAYS_INDIRECT=1
```
2. Check box for "Disable access control" upon starting VcXsrv.
3. Add a separate inbound rule for TCP port 6000 to the windows firewall.
    1. Go to Windows Defender Firewall control panel.
    2. On the left side, click "Advanced settings".
    3. On the left side, click "Inbound Rules".
    4. Create an inbound rule to allow TCP port 6000, applied to Domain, Private, Public. I named mine "WSL2 Xserver".
    5. Click on the Properties for that rule, and on the Scope tab, add remote IP address `172.16.0.0/12`.
4. In the same "Advanced settings" menu, I found all entries of VcXsrv (2 for me) and ticked "Allow the connection" for each.
