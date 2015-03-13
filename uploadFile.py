import time, os
time.sleep(10)
f = open('Uploads/test.txt', 'wb')
f.close()
os.chmod('Uploads/test.txt', 0777)
