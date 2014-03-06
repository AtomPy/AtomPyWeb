import sys, time, os
import DownloadAPI as API

#Master loop (every 30 seconds, check)
while True:
    
    #First thing we need to do is get our database file list
    drive = API.getDriveService()
    fileList = API.getFileList(drive)

    #Log file buffer
    backupFolder = None
    logFile = []

    #References deleted
    deletionOccured = False
    
    #We only care about excel files, dwindle down the list
    tempFileList = []
    fileListTitles = []
    for x in range(len(fileList)):
        if fileList[x]['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            tempFileList.append(fileList[x])
            fileListTitles.append(fileList[x]['title'])
    fileList = tempFileList

    #Storage array for files we want to backup
    filesToBackup = []

    #Get the latest reference file list
    directories = os.listdir('C:\\wamp\\www\\Backups\\')
    if len(directories) == 0:
        
        #There are no previous backups, backup everything
        filesToBackup = fileList
        logFile.append('All new files!')

    else:
        
        #There are previous backups
        
        #Grab the reference file from the latest one
        latest = 0
        for x in range(len(directories)):
            if directories[x] > directories[latest]:
                latest = x
        f = open('C:\\wamp\\www\\Backups\\' + directories[latest] + '\\referenceList.txt','rb')
        refs = f.readlines()
        for x in range(len(refs)):
            refs[x] = refs[x].replace('\r\n','')
        f.close()

        #Now, go through all of the files
        for x in range(len(fileList)):

            #Find the index of file in the reference list
            index = -1
            for y in range(len(refs)):
                if refs[y].split(',')[0] == fileList[x]['title']:
                    index = y
                    break

            # (INSERT) If index = -1, then the file is new
            if index == -1:
                filesToBackup.append(fileList[x])
                logFile.append('New File: ' + fileList[x]['title'])

            # (MODIFIED) If index is not -1, if exists in the database
            if index != -1:

                #Has the file changed? Check the dates
                if fileList[x]['modifiedDate'][:-1] > refs[index].split(',')[1]:

                    #It was modified, back it up
                    filesToBackup.append(fileList[x])
                    logFile.append('Modified File (by ' + fileList[x]['lastModifyingUserName'] + '): ' + fileList[x]['title'])

        #Now go through all of the references to look for deletions
        for x in range(len(refs)):
            if refs[x].split(',')[0] not in fileListTitles:
                
                # (DELETE)
                logFile.append('Deleted File: ' + refs[x].split(',')[0])
                deletionOccured = True

    #Create the backup folder
    if deletionOccured == True or len(filesToBackup) > 0:
        backupFolder = "C:\\wamp\\www\\Backups\\" + time.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs(backupFolder)

    #Now do the actual backing-up
    if len(filesToBackup) > 0:
        
        #Now cycle through all of the files to be backed up
        for x in range(len(filesToBackup)):

            #Download the file and save to the folder
            f = open(backupFolder + '\\' + filesToBackup[x]['title'] + '.xlsx', 'wb')
            logFile.append('Downloading: ' + filesToBackup[x]['title'])
            f.write(API.getRawFile(drive, filesToBackup[x]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']))
            f.close()

        #Create this backup's reference file list
        f = open(backupFolder + '\\referenceList.txt','wb')
        for x in range(len(fileList)):
            f.write(fileList[x]['title'] + ',' + fileList[x]['modifiedDate'] + '\r\n')
        f.close()
        logFile.append('Backup finished!')
        
    else:
        #Nothing to backup
        logFile.append('Nothing to backup!')

    #Now save the log file
    if backupFolder != None:
        f = open(backupFolder + '\\log.txt','wb')
        for x in range(len(logFile)):
            f.write(logFile[x] + '\r\n')
        f.close()

    #Deletion-only backup
    if deletionOccured == True and len(filesToBackup) == 0:
        #Create this backup's reference file list
        f = open(backupFolder + '\\referenceList.txt','wb')
        for x in range(len(fileList)):
            f.write(fileList[x]['title'] + ',' + fileList[x]['modifiedDate'] + '\r\n')
        f.close()
        logFile.append('Backup finished!')

    #And now we wait 30 seconds
    time.sleep(30)
    print 'Waiting...'
