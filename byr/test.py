import shutil, os, subprocess

total, used, free = shutil.disk_usage('/')
print(free)

print("Total: %d GB" % (total // (2**30)))
print("Used: %d GB" % (used // (2**30)))
print("Free: %d GB" % (free // (2**30)))


with open(os.devnull, 'w') as devnull:
	subprocess.Popen(['transmission-cli', '-p', '12447', '276922.torrent'], stdout=devnull, stderr=devnull)
