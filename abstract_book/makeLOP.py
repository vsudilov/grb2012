#makeLOP.py
#vss april/2012

'''
Parse the output from the sql query:

SELECT u.name,u.firstname,u.affiliation,u.email
FROM user u
WHERE u.invitationstatus='invited'

and input the data to make an list of participants.
'''

_keys = ['u.name','u.firstname','u.affiliation','u.email']

import sys,os


class users(object):
  def __init__(self):
    self.users = []
  def appendUser(self,raw_user):
    if not raw_user:
      return
    self.users.append(raw_user)

  def _order(self):
    '''Order self.pusers based on last name'''
    self.users = sorted(self.users, key=lambda k: k['u.name'].upper())    
    
  def makeTex(self,template='templates/LOP.tex'):
    self._order()
    fp = open(template,'r')
    tex = fp.read()
    fp.close()
    
    _text = '\n'.join(['\\tiny %s &\\tiny %s & \\tiny %s & \\tiny %s \\\\ \\hline' % tuple([k[i] for i in _keys]) for k in self.users])
    _text = _text.replace('@','\\@')
    tex = tex.replace('$LOP',_text)
    
    
    fp = open('LOP.tex','w')
    fp.write(tex)
    fp.close()

      
def parse(line):
  line = line.replace('\n','') #Remove newline delimiter
  line = line.strip()
  if not line:
    return None
  line = line.split('|') #Field delimiter
  try:
    _d = dict((k, line[i]) for (i, k) in enumerate(_keys))
  except:
    print "WARNING: Failed parse. Here is the offending line:\n"
    print line
    print "\nPRESS ENTER TO CONTINUE"
    raw_input()
    return None
  return _d


def main():
  myUsers = users()
  fp = open('LOP.csv','r')
  read = fp.read()
  fp.close()
  lines = read.split('\n') #Newline delimiter
  for line in lines:
    myUsers.appendUser(parse(line))
  myUsers.makeTex()
  
  
if __name__ == "__main__":
  main()
