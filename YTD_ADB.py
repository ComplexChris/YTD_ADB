import urllib, os, time, sys #, requests
from OpenSSL import SSL
from Tools import SAK

__version__ = "4.2.1"

## Create Manual for connecting Android device
## Create Help file
## -- Research .mp3
## COMPLETE - Create alternate "Manual" mode when KeyBoard interrupt
## COMPLETE - (M/A/E/C) Manual, Auto, Cancel
## Settings.txt > start_auto = True
## Test device connection per sync
## Get Spotify API or other String.split('/n') to search and download from YTD
## Create ADB function to test if connected. Run only if True.
## Clean Up self.Slugiy()
## Invegtigate IO (Internet connection)
## Replace self.isConnected with above mentioned "if connected" method
## ? Append statistics (i.e Duplicate IDs)
## --Completed: "Wired" or "Wireless" device found (x)
## Add extended options (i.e Start Settings, Erase, User, etc)
## "Enter username>" path="User"+un
## Add HTTP test in __init__ statement
## Check for default files (FAQ, SettingsHelp) create if False
## Default = Manual
## More options for custom YTD API (Playlist info, how many will be syned/downloaded)

# traviscalloway5@gmail.com

DEFAULT = {
           "MyMusic":os.path.join( os.getcwd(), "MyMusic"),
           "Buffer" : 16000000,
           "Refresh" : 60.0,
           "URL": ["""https://www.youtube.com/playlist?list=PLuBVoGs-BOLBtfQk6SP5ksKK8Ya4PBtH5"""],
           "IP":None,
           "IP_Port":5555,
           "Start_Auto":False}

DEFAULT_HELP = """ Note: Only change values and are correct type \n{
           \n"MyMusic" : str( Path to Directory ) ,
           \n"Buffer" : int( Max file size in bytes ),
           \n"Refresh" : int( Interval in seconds to check for new downloads/songs
                            [Lower the number, more frequent it'll sync, but higher memory consumption ),
           \n"URL" : list( Full URL link to specified playlist. Must remain within
                        list brackets, and in string format seperated by commas ),
           \n"IP" : str( Local IP adress of Android device. Must be on same wireless network
                      and device must be configured properly,
           \n"IP_Port" : int ( Port to which TCPIP Daemon listens on
           }"""
FAQ = """
Q: What does this program do, exactly?
A: Simple.
   Short: Automatically Downloads and Syncs playlist(s)
   Long: The User enters their Youtube playlist(s) URL into the "Settings.txt" file,
   and the program will run in the background, downloading all files in that
   playlist and syncing them to a connected Android device.
   
Q: I don't understand how to add my own playlist.
A: Open the "Settings.txt" and fill out the field "URL".
   Look at "SettingsHelp.txt" for further help.

Q: How long did it take to write/devolop this program?
A: About a week.

Q: How do I get the ADB to work?
A: Ensure your device drivers are installed on your computer, then,
   On your device, enable "Devoloper Options", and tick "USB Debugging."

"""


class Web(SAK):
    def __init__(self):
        pass

    def Verify(self, path, size):
        """Returns True if file and size is True"""
        if os.path.exists(path):
            if os.path.getsize(path)==size:
                return True
        return False

    def LoadSettings(self, settings_loc="Settings.txt"):
        """Imports settings from default file in JSON format"""
        var = {} ## Accepted variables/values for settings
        if os.path.exists(settings_loc)==False:
            self.WriteFile(settings_loc, str(DEFAULT), 'w')
            print "\nSettings File created: %s" % settings_loc
        try:
            user = eval(self.ReadFile( settings_loc ))
        except Exception as E:
            if os.path.exists(settings_loc)==False:
                print "\nSettings file not found ({0})".format( settings_loc )
                self.WriteFile(settings_loc, str(DEFAULT), 'w')
            print "\nUnable to load user settings, going with default..."
            user = DEFAULT
        
        for k in DEFAULT.keys():
            var[k] =  user[k] if k in user else DEFAULT[k]

        ## Specific parameter check
        """if os.path.exists( var['MyMusic'] ) == False:
            try: os.mkdir( var['MyMusic'] )
            except: os.mkdir( DEFAULT['MyMusic'] )"""
            
        return var

    
    def Save(self, URL, path):
        """Method for downlading content and writing to path"""
        if True: #self.Exists(path)==False:
            content = self.Download(URL)
            self.WriteFile(path, content)
    
    def BruteTagOld(self, url=None, html=None, length=11, tag='href="/watch?v=', closeTag='"', Quiet=False):
        """ Returns list of all values in tags """
        "Used to get related videos"
        ## Primary method
        html = self.Download(url) if (html==None and url!=None) else html
        values = []
        while True:
            a = html.find(tag)
            if a < 0: break
            b = a+len(tag);
            c = b+length
            val = html[ b : c ]
            html = html[c:]
            if val not in values:
                values.append ( str(val) )
        return values

    def BruteTag(self, url=None, html=None, length=11, tag='href="/watch?v=', closeTag='"', Quiet=False):
        """ Returns list of all values in tags """
        "Used to get related videos"
        ## Primary method
        html = self.Download(url) if (html==None and url!=None) else html
        values = []
        while True:
            a = html.find(tag)
            if a < 0:
                break
            b = a+len(tag);
            if type(length) == int:
                c = b+length
            else:
                tmp = html[b:].find(closeTag)
                c = b+tmp
                
            val = html[ b : c ]
            html = html[c:]
            if val not in values:
                values.append ( str(val) )
        return values


    def Download(self, URL):
        """Downloads data from URL and returns read()"""
        html = urllib.urlopen(URL).read() 
        return html
    def DownloadOLD(self, URL):
        """Attempt to negate HTTPS error"""
        r = requests.get(URL)
        return r.text

class YTD(Web):
    def __init__(self, Active=True):
        self.API = "http://www.youtubeinmp3.com/fetch/?format=JSON&filesize=1&bitrate=1&video=www.youtube.com/watch?v={0}"
        self.User_Input = lambda x=">>> ": raw_input(x)
        self.Settings = DEFAULT
        self.IsSync = False
        if Active:
            os.system("color a & title YTD w/ ADB v.{0}".format(__version__ ) ) 
            print "\n\nWelcome to YTD Auto-Sync Utility (v.{0})!\n".format(__version__)
            if "Y" in self.Raw_Choice("Initialize (Y/N)? "):
                self.Settings = self.LoadSettings()

                print "\n-Settings loaded..."
                for k, v in self.Settings.iteritems():
                    print " | " + " = ".join((k, str(v) ) )

                self.MakePath(self.Settings['MyMusic'] )
                
                if self.Settings['IP'] != None:
                    self.ADB_OBJ = ADB( self.Settings['IP'], self.Settings['IP_Port'] )
                else:
                    self.ADB_OBJ = ADB()
                self.isConnected = self.ADB_OBJ.is_connected
                
                if self.isConnected==False:
                    print " | Unable to initlize Android device."
                    print " | Restart program to try again, or continue without sync feature."
                elif self.isConnected: #else
                    self.ADB_Path =  self.ADB_OBJ.FindPath()
                    cType = "Wireless" if self.ADB_OBJ.is_wireless else "Wired"
                    print " | {1} Device found (SN: {0})".format( self.ADB_OBJ.GetName(), cType )
                    print " | Will sync to: " + str(self.ADB_Path)

                if self.Settings["Start_Auto"] == True:
                    if "Y" in self.Raw_Choice("\nBegin auto sync (Y/N)? "):
                        self.Auto()
                else:
                    self.Manual()
                            
                            
    def Manual(self):
        while True:
            print "\n%s\n\n" % ("_"*40) ## Line break
            print "\nManual Interface: "
            print "a. Download \tb. Sync \nc. Auto Mode \td. Exit"
            choice = self.Raw_Choice(">>>", "ABCD1234")
            if choice in "A1":
                self.Scrape()
            elif choice in "B2":
                if self.isConnected:
                    self.ADB_OBJ.Check( self.Settings['MyMusic'],
                                    self.ADB_Path, True, True)
            elif choice in "C3":
                self.Auto()
            elif choice in "D4":
                sys.exit()

    def Auto(self):
        x=0
        while True:
            x+=1
            try:
                print "\n%s\n\n" % ("_"*40)  ## Line break
                print "+--"+ str(time.ctime())
                print "   %s: Auto Syncing..." % str(x)
                self.Start()
            except KeyboardInterrupt:
                choice = self.Raw_Choice("\nExit(Y/1), Manual(M/2), or Cancel(N/3)? ", "YA1MB2NC3")
                if choice in 'YA1':
                    sys.exit()
                elif choice in "MB2":
                    self.Manual()
                    
    def UI(self):
        while True:
            resp = self.Raw_Choice("Sup >>> ", "ABC" )
            if resp=='A':
                self.Sync = False
            elif resp=='B':
                os.startfile("Settings.txt")
            else:
                sys.exit()
            
    def Start(self):
        null = self.Scrape()
        if self.isConnected:
            self.ADB_OBJ.Check( self.Settings['MyMusic'],
                                self.ADB_Path, True, True)
        print ".\n.\n.\n."
        
    def Single(self, ID, retTitle = False):
        """Downloads single video to path"""
        ## Step 1: Get JSON, and link to HTML containing download URL
        JSON_link = self.API.format(ID)
        JSON = {'title':"None", 'filesize':"0", 'link':""}
        try:
            JSON = eval( self.Download(JSON_link) )
        except:
            ## Third contingancy download method. Super annoying!
            alt, title = self.GetTitle(ID)
            JSON['link'] = self.Fix("", alt, True)
            JSON['title'] = title
        print 
        #print "\n" + self.Download(JSON_link)[:512]
        #sys.exit()
        ## Step 2: Take the returned URL, and extract download link
        url = JSON['link'].replace("\/", "/")
        url = urllib.quote( url , safe="%/:=&?~#+!$,;'@()*[]")  ##stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python 
        Con = self.MakeAscii( JSON['title'] )
        title = self.Slugify( "{0}_{1}.m4a".format( Con, ID ) )
        #print "Title: " + title
        path = os.path.join( self.Settings['MyMusic'], title)
        size = int(JSON['filesize'])
        if self.Verify(path, size)==True:
            print "\nSkipping ({0})...".format(title)
            return False
            
        if (size < self.Settings["Buffer"]):
            self.Save(url, path)
            ## Possible size difference alg = s - int( s *0.99999) and 1.00001
            if os.path.exists(path):
                if os.path.getsize(path) != size:
                ## Possible incorrect download
                    try:
                        self.Fix(path)
                    except:
                        print "...failed..."
        else:
            print "\nFile too large. Skipping {0}".format( str(title) )
        if retTitle: return title

    def Fix(self, path='', url=None, ret_url=False):
        """Invalid download. Attempts to read HTML file, extract actual url"""
        if url==None and os.path.exists(path):
            html = self.ReadFile(path, 'r')
        else:
            html = self.Download(url)
        frag = self.BruteTag(html=html, length=None, tag='''href="/download/''', closeTag='''">''')
        print ret_url, frag
        base = "http://www.youtubeinmp3.com/download"
        new_url = '/'.join((base, frag[0]))
        #print "\nRe-attempting download "+new_url
        if new_url == None:
            return
        else:
            if ret_url==False:
                self.Save(new_url, path) #.replace(".m4a", "_Re.m4a") ) #Change name to show/keep incorrect download
            else:
                return new_url
            
    def GetTitle(self, ID):
        ## Get Title form third nested URL
        alt = "http://www.youtubeinmp3.com/download/?video=www.youtube.com/watch?v={0}&autostart=1&n=&x=".format(ID)
        oTag = '<span id="videoTitle">'; cTag = '</span>'
        title = self.BruteTag(url=alt, length=None, tag=oTag, closeTag=cTag)[0]
        return alt, title
        
    def Scrape(self):
        """Get links from specified playlist stored in local variable."""
        url = self.Settings['URL']
        save_dir = self.Settings['MyMusic']
        skipped = 0
        videos = []  ## ID's of all Videos
        # Returns ID's from HTML of URL
        for playlist in url: 
            videos.extend( self.BruteTag( playlist )  )
        #print playlist
        #print len(videos), videos
        #sys.exit()
        library = str(os.listdir( self.Settings['MyMusic'] ) )

        for ID in videos:
            if ID not in library:
                print "\n+--Downloading...",
                resp = self.Single(ID, retTitle=True)
                if resp!=False:
                    print ( "'{0}' complete!".format( str( resp.rstrip(ID+'.m4a')[:45] ) ))
            else:
                #print ("\nSkipping: " + ID)
                skipped +=1
        lv = len(videos)
        print "\n{0}/{1} Downloaded.\n".format(lv-skipped, lv)

def Hello():
    print "Hello"
    threading.Timer(1.52, Hello ).start()
    raw_input("TEST")

class ADB(SAK):
    def __init__(self, IP=None, Port=None, startup=True):
        self.is_connected=False; self.is_wireless=False
        self.ADB_DeviceName = "None"
        self.storage_loc = [
        "/storage/extSdCard/YTD_Music",
        "/storage/sdcard0/YTD_Music",
        "/storage/emulated/0/YTD_Music",
        "/storage/emulated/legacy/YTD_Music"
        ] # Respective order in presedence.
        if startup:
            print "\n-Initilizing ADB server..."
            if IP != None:
                commands = ["adb kill-server",
                            "adb start-server",
                            "adb tcpip {0}".format(Port),
                            "adb connect {0}".format(IP),
                            "adb devices" ]
            else:
                commands = ["adb start-server",
                            "adb devices" ]

            cmd_in = os.popen( " & ".join(commands) ).read()
            self.WriteFile("Log.txt", " \n ".join((time.ctime(), cmd_in)), 'a')
            if "more than one device/emulator" in cmd_in:
                print "\nError: Multiple devices found. \nDisconnect device or delete device IP in Settings.txt"
                return
            elif "connected to {0}".format(IP) in cmd_in.lower() and IP!=None:
                ## Says that a device is connected, and is wireless
                self.is_connected=True; self.is_wireless=True
            else:
                #con_test = os.popen( "adb shell ls" ).read()
                #if "error" in con_test and "'(null)'" in con_test:
                if cmd_in.count("device")==2:
                    self.is_connected=True; self.is_wireless=False
                else:
                    # Redundant
                    return
                
            if self.is_connected==True:
                self.ADB_DeviceName = self.GetName()

    def CStat(self):
        self.is_connected=False; self.is_wireless=False
        cmd_in = os.popen( " & ".join(commands) ).read()
        pass
    
                
    def GetName(self):
        devs = os.popen("adb devices").read()
        name = (devs.split("\n"))[1]
        name = name.split('\t')[0]
        return name
        
    def Push(self, local_file, to):
        command = """adb push -p "{0}" {1}""".format(local_file, to)
        #print command
        #return
        #stat = os.popen( command )
        null = os.system(command)

    def LS(self, path='.', ret=False):
        command = "adb shell ls '%s'" % path
        stat = str(os.popen(command).read())
        if ret:
            return stat
        else:
            print stat

    def FindPath(self):
        """Obsolete"""
        #com = "adb shell [ ! -d /{0} ] && echo 'Directory not found'"
        com = """adb shell "[ -d '{0}' ] && echo 'Directory exists.' " """
        for possible in self.storage_loc:
            null = self.MakePath(possible)
            obj = os.popen( com.format(possible) )
            stat = obj.read()
            if "exists" in stat:
                self.ADB_Path = possible
                return possible
            """if "not found" in stat.lower():
                continue
            #if "not found" not in stat.lower():
            else:
                self.ADB_Path = possible
                return possible"""
        return False

    def FindPathOld(self):
        """Obsolete"""
        for possible in self.storage_loc:
            print "AAHHH"
            null = self.MakePath(possible)
            resp = os.popen("adb shell ls -la '{0}'".format(possible) )
            stat = resp.read().lower()
            print "Stat: " + stat
            if "no such file" in stat or "not found" in stat:
                del stat, null
                continue
            else:
                self.ADB_Path = possible
                return possible
        return False

    def MakePath(self, Path):
        null = os.popen("adb shell mkdir '{0}'".format(Path) ).read()
        #verify = os.popen("adb shell ls '{0}'".format(Path) ).read()
        """" if "no such file" in verify.lower():
            return False
        else:
            self.ADB_CreatedPath = Path
            return True """

    def ADB_Verify(self, path, size):
        com = "adb shell ls -l '{0}'".format(path)
        resp = os.popen(com).read()
        if str(size) in resp:
            return True

    def Check(self, Local_dir, to, sync=False, verbose=False, least=50000):
        ## Use sync, or verify to destination
        
        files = os.listdir(Local_dir)
        dev_files = os.popen("adb shell ls -la '{0}'".format(to) ).read()
        synced = 0; backup = 0
        for f in files:
            backup += 1
            fPath = to #'/'.join((to, f)) #.replace("\\", "/")   # Android Path
            #@fPath = os.path.join(to, f)
            #fPath = fPath.replace("\\", "/")
            defPath = '/'.join((Local_dir, f)).replace("\\", "/")   # Windows Path

            if os.path.getsize(defPath) < least:
                continue
            
            size = os.path.getsize( defPath )
            resp = self.ADB_Verify( fPath, size )
            if resp == True:
                continue
            else:
                if verbose:
                    print "\n+--Syncing %s \n " % f,
                if sync:
                    f_to = os.path.join(to, f)
                    self.Push( defPath, to)
                synced += 1
        print "\n{0}/{1}({2}) Synced!".format(synced, len(files), backup)
                
                        

Y = YTD(1)
