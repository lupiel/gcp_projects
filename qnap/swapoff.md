# commands
```
cat /proc/swaps
cat /proc/mdstat


swapoff /dev/md256
swapoff /dev/md322
mdadm --stop /dev/md256
mdadm --stop /dev/md322
swapoff /share/CACHEDEV1_DATA/.swap/qnap_swap
rm /share/CACHEDEV1_DATA/.swap/qnap_swap
mdadm /dev/md9 --fail /dev/sda1
mdadm /dev/md9 --fail /dev/sdb1
mdadm /dev/md13 --fail /dev/sda4
mdadm /dev/md13 --fail /dev/sdb4
```

# BEFORE:
```
[admin@NASSERVER ~]$ cat /proc/swaps
Filename                                Type            Size            Used            Priority
/dev/md321                              partition       8283708         1041836         -2
/dev/md256                              partition       530108          0               -3
/dev/md322                              partition       7235132         0               -4
/share/CACHEDEV1_DATA/.swap/qnap_swap   file            16777212        0               -5
[admin@NASSERVER ~]$ cat /proc/mdstat
Personalities : [linear] [raid0] [raid1] [raid10] [raid6] [raid5] [raid4] [multipath]
md3 : active raid1 sdb3[0]
      7804071616 blocks super 1.0 [1/1] [U]

md2 : active raid1 sda3[0]
      7804071616 blocks super 1.0 [1/1] [U]

md1 : active raid1 nvme0n1p3[0]
      1749202944 blocks super 1.0 [1/1] [U]

md322 : active raid1 sdb5[1] sda5[0]
      7235136 blocks super 1.0 [2/2] [UU]
      bitmap: 0/1 pages [0KB], 65536KB chunk

md256 : active raid1 sdb2[1] sda2[0]
      530112 blocks super 1.0 [2/2] [UU]
      bitmap: 0/1 pages [0KB], 65536KB chunk

md321 : active raid1 nvme0n1p5[0]
      8283712 blocks super 1.0 [2/1] [U_]
      bitmap: 1/1 pages [4KB], 65536KB chunk

md13 : active raid1 nvme0n1p4[0] sda4[128] sdb4[129]
      458880 blocks super 1.0 [128/3] [UUU_____________________________________________________________________________________________________________________________]
      bitmap: 1/1 pages [4KB], 65536KB chunk

md9 : active raid1 nvme0n1p1[0] sda1[128] sdb1[129]
      530048 blocks super 1.0 [128/3] [UUU_____________________________________________________________________________________________________________________________]
      bitmap: 1/1 pages [4KB], 65536KB chunk

unused devices: <none>
```

# AFTER:
```
[admin@NASSERVER ~]$ cat /proc/swaps
Filename                                Type            Size            Used            Priority
/dev/md321                              partition       8283708         1039268         -2
[admin@NASSERVER ~]$ cat /proc/mdstat
Personalities : [linear] [raid0] [raid1] [raid10] [raid6] [raid5] [raid4] [multipath]
md3 : active raid1 sdb3[0]
      7804071616 blocks super 1.0 [1/1] [U]

md2 : active raid1 sda3[0]
      7804071616 blocks super 1.0 [1/1] [U]

md1 : active raid1 nvme0n1p3[0]
      1749202944 blocks super 1.0 [1/1] [U]

md321 : active raid1 nvme0n1p5[0]
      8283712 blocks super 1.0 [2/1] [U_]
      bitmap: 1/1 pages [4KB], 65536KB chunk

md13 : active raid1 nvme0n1p4[0]
      458880 blocks super 1.0 [128/1] [U_______________________________________________________________________________________________________________________________]
      bitmap: 1/1 pages [4KB], 65536KB chunk

md9 : active raid1 nvme0n1p1[0]
      530048 blocks super 1.0 [128/1] [U_______________________________________________________________________________________________________________________________]
      bitmap: 1/1 pages [4KB], 65536KB chunk

unused devices: <none>
```

# add to autostart:
https://www.qnap.com/pl-pl/how-to/faq/article/running-your-own-application-at-startup

for me:
```
    1  $echo $(/sbin/hal_app --get_boot_pd port_id=0)6
    2  sudo echo $(/sbin/hal_app --get_boot_pd port_id=0)6
    3  mount /dev/mmcblk0p6 /tmp/config
    4  ls
    5  bdf
    6  ls /tmp/config
    7  vi /tmp/config/autorun.sh
    8  cat /tmp/config/autorun.sh
    9  ls -la /tmp/config/autorun.sh
   10  chmod +x /tmp/config/autorun.sh
   11  ls -la /tmp/config/autorun.sh
   12  unmount /tmp/config/
   13  sudo unmount /tmp/config/
   14  sudo umount /tmp/config/
   15  history
```
