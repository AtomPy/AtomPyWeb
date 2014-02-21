import sys, time, os
import DownloadAPI as API

#Master loop (every 5 mins, check)
while True:
    #First thing we need to do is get our file list
    drive = API.getDriveService()
    fileList = API.getFileList(drive)

    #Get our reference file list
    f = open('C:\\wamp\\www\\Backups\\referenceList.txt','rb')
    refs = f.readlines()
    for x in range(len(refs)):
        refs[x] = refs[x].replace('\n','')
    f.close()

    #Backup file structure
    backupFiles = []

    #Now cycle through each excel file in the database
    for x in range(len(fileList)):
        if fileList[x]['mimeType'] == 'application/vnd.google-apps.spreadsheet':

            index = -1
            for y in range(len(refs)):
                if refs[y].split(',')[0] == fileList[x]['title']:
                    index = y
                    break

            #Now see if the file is not in the reference list
            if index == -1:
                #Since it is not in the reference list, go
                #ahead and add it
                refs.append(fileList[x]['title'] + ',' + fileList[x]['modifiedDate'][:-1])

                #Add to the files to backup
                backupFiles.append(x)
                print 'NEW: ' + fileList[x]['title']

            else:
                #The file is in the reference list, so check
                #to see if the file has been modified
                if fileList[x]['modifiedDate'][:-1] > refs[index].split(',')[1]:
                    #The file has been modified
                    #Go ahead and add the file to the backup
                    backupFiles.append(x)
                    print 'MOD: ' + fileList[x]['title']

    #Check to make sure there are any files to backup
    if len(backupFiles) > 0:
        #Create the backup folder
        backupFolder = "C:\\wamp\\www\\Backups\\" + time.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs(backupFolder)
        
        #Now cycle through all of the files to be backed up
        for x in range(len(backupFiles)):

            #Download the file and save to the folder
            f = open(backupFolder + '\\' + fileList[backupFiles[x]]['title'] + '.xlsx', 'wb')
            print 'Downloading: ' + fileList[backupFiles[x]]['title']
            f.write(API.getRawFile(drive, fileList[backupFiles[x]]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']))
            f.close()

        #Now also append the reference list
        f = open('C:\\wamp\\www\\Backups\\referenceList.txt','wb')
        for x in range(len(refs)):
            f.write(refs[x] + '\n')
        f.close()
        print '\nBackup finished!\n'
        
    else:
        #Nothing to backup
        print '\nNothing to backup!\n'

    #And now we wait...
    time.sleep(300)
