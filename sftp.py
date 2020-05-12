# list files in directory
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('sftpx.pilotcorp.com',22, username='ConsolidatedMovement',password='312l8R4Z')
ftp = client.open_sftp()
# ftp_client=ssh.open_sftp()
# ftp.put('D:/Users/turamau/PycharmProjects/gpss-consolidatedmovement/lambda/arv.csv','arv.csv')
# ftp.delete = 'arv.csv'
# ftp.close()
files = ftp.listdir('')
# f = open("cmqa_files.txt", "w+")

for z in files:
    # f.writelines(z)
    print(z)




























    # f.writelines(z + '\n')
    # x = ftp.file(files)
    # print(x.__dict__)
    # for y in x:
    #     print(y)

#
# '''To get data in file'''
# import paramiko
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect('sftpx.pilotcorp.com',22, username='ConsolidatedMovement',password='312l8R4Z')
# ftp = client.open_sftp()
# # ftp.put('D:/Users/turamau/PycharmProjects/gpss-consolidatedmovement/lambda/arv.csv')
# # remote_file = ftp.open('/arv.csv')
# # try:
# #     f = open("arv.csv", "w+")
# #     for line in remote_file:
# #         print(line)
#         # f.writelines(line + '\n')
#         # process line
# # finally:
# #     remote_file.close()
# # ssh.close()
# # sftp = paramiko.SFTPClient.from_transport(transport)
# # try:
# #     sftp.chdir(remote_path)  # Test if remote_path exists
# # except IOError:
# #     sftp.mkdir(remote_path)  # Create remote_path
# #     sftp.chdir(remote_path)
# # sftp.put(local_path, '.')    # At this point, you are in remote_path in either case
# # sftp.close()