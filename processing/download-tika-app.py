import sys
from ftplib import FTP

ftp_url = '143.106.10.149' # ip: ftp.unicamp.br
tika_folder = '/pub/apache/tika/'
tika_app_prefix = 'tika-app'
local_tika_file = 'tika-app.jar'

ftp = FTP(ftp_url)
ftp.login()
ftp.cwd(tika_folder)
tika_file = ''
for file in ftp.nlst():
    if file.startswith(tika_app_prefix):
        tika_file = file
        break
if tika_file == '':
    print('The tika-app was not found in {} ftp'.format(ftp_url))
    sys.exit(1)
print("Downloading {} from {}".format(tika_file, ftp_url))
with open(local_tika_file, 'wb') as fp:
    ftp.retrbinary('RETR {}'.format(tika_file), fp.write)
ftp.quit()
print("Downloaded {}".format(tika_file))
