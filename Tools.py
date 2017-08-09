import os, sys


# Basic module for various operations
s = "C:\\Users\\Chris\\Documents\\Python_2.7\\2016\\YTD_Sync\\MyMusic\\David Guetta - What I Did For Love (Lyric Vido) ft Emeli Sand\\u00e9_9fL5iWgWwno.m4a"

class SAK():
    """(Swiss Army Knife) - Class for basic tools"""
    Exists = lambda self, x: os.path.exists(x)
    def MakeAscii(self, single):
        #https://stackoverflow.com/questions/1342000/how-to-make-the-python-interpreter-correctly-handle-non-ascii-characters-in-stri        
        test = ''
        Forbid = '/\:*?"<>|&;=,^!@#$[]'
        for i in single:
            #print "char: {0}".format(i)
            if ord(i)<128:
                if i not in Forbid:
                    test+=i
        return test
        #return "".join(i for i in s if ord(i)<128)
    
    def MakePath(self, path):
        """Recursively creates path
        working back from the parent directory each iteration"""
        if True: #for x in range(3):
            try:
                if os.path.exists(path)==False:
                    os.mkdir(path)
                #break
            except OSError:
                self.MakePath( os.path.abspath( os.path.join(path, "..") ))

    def Slugify(self, Path, instead='_'):
        """ Creates File appropriate ASCII file names from absolute paths"""
        Forbid = '/\:*?"<>|&;=,^!@#$[]'
        fin = ''
        frag = os.path.basename(Path)
        
        for c in frag:
            if c!= ' ': c = c.strip() 
            if c not in Forbid: fin += c
            else: c+=instead
        #Frag = unicodedata.normalize('NFKD',
        #Frag = self.MakeAscii( fin.encode('ascii','ignore') )
        #return Path.replace(frag, self.MakeAscii(fin) ) #re.sub(Forbid, "", Frag)
        return os.path.join(os.path.dirname(Path), self.MakeAscii(fin) )
                
    def ReadFile(self, FileName, mode='rb'):
        with file(FileName, mode) as f:
            return f.read()
            
    def WriteFile(self, FileName, Content, mode='wb'):
        with file(FileName, mode) as f:
            f.write(Content)
        f.close()
        
    def Smart_Input(self, msg='(Y/N)'):
        """ raw_input() with additional system options """
        while True:
            Out = raw_input(msg)
            OutUp = Out.upper()
            LOO = len(Out)
            path = Out[2:].strip(' ') ## Used for "CD"
            if path.upper() in ["HOME"]: path = _ScriptLoc
            
            if OutUp in "EXIT,SHIT,FUCK,QUIT,STOP" and len(Out)==4:
                sys.exit() #raise SystemExit
            elif OutUp in ["LS", "DIR"]:
                print _Fancy, os.listdir('.')
            elif OutUp in ["GWD", "PWD"]:
                print _Fancy, os.getcwd()
            elif OutUp in ["FAQ", "HELP"]:
                print _Fancy, FAQ
            elif OutUp in ["START", "OPEN"]:
                os.startfile('.')
            elif OutUp[:2]=="CD" and self.Exists(path):
                os.chdir(path)
                print "\nChanging directories to: \n%s \n" % os.getcwd()
            else:
                return Out
            
    def Raw_Choice(self, Msg='(Y/N)', Options='YN', Length=[1]):
        """ Exactly what it sounds like... """
        while True:
            Answer = self.Smart_Input(Msg+'> ').upper()
            if (Answer in Options and len(Answer) in Length):
                return Answer

    def raw_int(self, msg="Enter a number > ", minInt=0, maxInt=1000, null=False):
        """User input for intergers in specific range"""
        while True:
            try:
                n= int(raw_input(msg))
                if n in range(0, 1000):
                    return n                
            except:
                if n=='' and null:
                    return 0
                continue

    def Rename(self, name):
        """Tests name, renames if exists"""
        x = 2
        while self.Exists(name):
            name = name.replace('({0})'.format(x-1), '')
            frag = name.split('.')
            a, b = '.'.join(frag[:-1]), frag[-1]
            name = "%s(%s).%s" %(a, x, b)
            x+=1
        return name

Tools = SAK()
