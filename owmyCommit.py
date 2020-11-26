import re
import subprocess
import argparse
import os

#==========================================

# Variables
git="/usr/bin/git"
commandGitLog =  git + " log"
commandGitShow = git + " show"

# Regex
regexSocket=(r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5})")
regexIP=(r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):(\d{1,5})")
regexCIDR=(r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\/\d{2})")
regexName=(r"Author:\s([a-zA-z]+\s[a-zA-z]+)")
regexEmail=(r"([a-zA-z0-9-_.]+@[a-zA-z0-9-_.]+\.[a-zA-z0-9-_.]+\.?[a-zA-z0-9-_.])")
regexDirUnix=(r"(/\w+/?\w+/?\w+)")
regexDirWindows=(r"([a-zA-Z]:\\[\\\S|*\S]?.*)")
regexURL=(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
regexUUID=(r"(\w{1,8}-\w{4}-\w{4}-\w{4}-\w{12})")
regexJWT=(r"(eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*)")
regexAWSKey=(r"(AWS[A-Za-z0-9_]*\=?[A-Za-z0-9_\/]*)")
regexPass=(r"([pass|password|key|apikey|api_key|token]\s?\=\=?\s?\"[a-z-A-Z0-9!@#$%&*()_+=]+\")")

#==========================================

def scriptBanner():
    print(""" 
 _______  _     _  __   __  __   __  _______  _______  __   __  __   __  ___   _______ 
|       || | _ | ||  |_|  ||  | |  ||       ||       ||  |_|  ||  |_|  ||   | |       |
|   _   || || || ||       ||  |_|  ||       ||   _   ||       ||       ||   | |_     _|
|  | |  ||       ||       ||       ||       ||  | |  ||       ||       ||   |   |   |  
|  |_|  ||       ||       ||_     _||      _||  |_|  ||       ||       ||   |   |   |  
|       ||   _   || ||_|| |  |   |  |     |_ |       || ||_|| || ||_|| ||   |   |   |  
|_______||__| |__||_|   |_|  |___|  |_______||_______||_|   |_||_|   |_||___|   |___|  

            """ + "\ndeveloped by icarot\nVersion: 0.0.1\n")

def setParam():
    # Define the parameters of the script.
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Will print all commits line submitted.", action="store_true")
    global args
    args = parser.parse_args()

def saveFile(data,filename):
    print("Creating a file...");
    file = open(filename, "w")
    file.write(data)
    file.close()
    if os.path.isfile(filename):
        print("File created: " + filename + "\n###")
    else:
        print("[ERROR] File " + filename + "was not created.\n###")

def runCommand(command):
    returnCommand = subprocess.run(command, shell=True, capture_output=True, text=True)
    return returnCommand

def gitInstalled():
    # Check if the command Git is configured correctly.
    if not os.path.isfile(git): 
        print("[ERROR] Please set the binary path of Git in the variable 'git' within owmyCommit.py")
        exit()

def getCommitHash(returnGitLog):
    setCollectedCommitHash = set()
    for line in returnGitLog.stdout.split(sep="\n"):
        commitHash = re.match("^commit (\w+)$", line)
        if commitHash:
            setCollectedCommitHash.add(commitHash[1])
    return setCollectedCommitHash

def getCommitDetail(returnGetCommitHash):
    setCollectedCommitDetail = set()
    for line in returnGetCommitHash:
        command = str(commandGitShow + ' ' + line)
        returnGitShowDetail = runCommand(command)
        setCollectedCommitDetail.add(returnGitShowDetail.stdout)
    return setCollectedCommitDetail

def getInfoFromCommit(returnGetCommitDetail, regex, label):
    setCollectedInfo = set()    
    for commit in returnGetCommitDetail:
        for line in commit.split(sep="\n"):
            if args.verbose:
                print(line)
            matchPattern = re.search(regex, line, re.IGNORECASE)
            if matchPattern:
                setCollectedInfo.add(matchPattern[1])
    print("\n" + label + "\n#")
    if len(setCollectedInfo) == 0:
        print("[INFO] Item not found!")
    else:
        print(setCollectedInfo)

def main():
    scriptBanner()
    setParam()
    returnGitLog = runCommand(commandGitLog)
    returnGetCommitHash = getCommitHash(returnGitLog)
    returnGetCommitDetail = getCommitDetail(returnGetCommitHash)
    getInfoFromCommit(returnGetCommitDetail, regexSocket, "Socket:")
    getInfoFromCommit(returnGetCommitDetail, regexIP, "IP:")
    getInfoFromCommit(returnGetCommitDetail, regexCIDR, "CIDR:")
    getInfoFromCommit(returnGetCommitDetail, regexName, "Name:")
    getInfoFromCommit(returnGetCommitDetail, regexEmail, "Email:")
    getInfoFromCommit(returnGetCommitDetail, regexDirUnix, "Directory Unix:")
    getInfoFromCommit(returnGetCommitDetail, regexDirWindows, "Directory Windows:")
    getInfoFromCommit(returnGetCommitDetail, regexURL, "URL:")
    getInfoFromCommit(returnGetCommitDetail, regexUUID, "UUID:")
    getInfoFromCommit(returnGetCommitDetail, regexJWT, "JWT:")
    getInfoFromCommit(returnGetCommitDetail, regexAWSKey, "AWS Key:")
    getInfoFromCommit(returnGetCommitDetail, regexPass, "General Key:")

#==========================================
main()
