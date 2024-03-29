#csv2abstract.py
#vss april/2012

'''
Parse the output from the sql query:

SELECT sp.sessionid, sp.sequencenumber, p.type, p.title, p.authors, p.affiliations, p.abstract, u.name, u.firstname
FROM session_presentation sp, presentation p, user u
WHERE p.id=sp.presentationid and u.invitationstatus='invited' and u.id=p.presenterid

and input the data to make an abstract book.
'''

_keys = ['sp.sessionid', 'sp.sequencenumber', 'p.type', 'p.title', 'p.authors', 'p.affiliations', 'p.abstract', 'u.name','u.firstname']

_invited_speakers = [
'Racusin',
'Piron',
'McBreen',
'Guiriec',
'Lazzati',
'MacFadyen',
'Kruehler',
'Schady',
'Tanvir',
'Bromm',
'Bersier',
'Rosswog',
'Nakar',
'Ahlers',
'Corsi',
'Hjorth',
'Levesque'
]

import sys


class presentations(object):
  def __init__(self):
    self.presentations = []
    _sessions = {}
    _sessions[1] = [1,"$ABSTRACT_SESSION_I_1","Session I: Recent results from Swift and Fermi"]
    _sessions[2] = [2,"$ABSTRACT_SESSION_IIa_2a","Session IIa: Prompt Emission Spectroscopy"]
    _sessions[3] = [6,"$ABSTRACT_SESSION_IIIa_3a","Session IIIa: Afterglow Theory"]
    _sessions[4] = [11,"$ABSTRACT_SESSION_Va_5a","Session Va: Progenitors of Long Duration Bursts"]
    _sessions[5] = [12,"$ABSTRACT_SESSION_Vb_5b","Session Vb: Progenitors of Short Duration Bursts"]
    _sessions[6] = [16,"$ABSTRACT_SESSION_VIII_8","Session VIII: Host Galaxies"]
    _sessions[7] = [9,"$ABSTRACT_SESSION_IVa_4a","Session IVa: GRBs as Probes of the Early Universe"]
    _sessions[8] = [14,"$ABSTRACT_SESSION_VI_6","Session VI: History and Future Instrumentation"]
    _sessions[9] = [15,"$ABSTRACT_SESSION_VII_7","Session VII: Grav. Waves, Neutrinos, Cosmic Rays and UHE Emission"]
    _sessions[22] = [3,"$ABSTRACT_SESSION_IIb_2b","Session IIb: Prompt Emission Spectroscopy"]
    _sessions[23] = [4,"$ABSTRACT_SESSION_IIc_2c","Session IIc: Prompt Emission Correlations and Temporal Properties"]
    _sessions[24] = [7,"$ABSTRACT_SESSION_IIIb_3b","Session IIIb: Afterglow Observations"]
    _sessions[25] = [13,"$ABSTRACT_SESSION_Vc_5c","Session Vc: Central Engine Physics"]
    _sessions[27] = [5,"$ABSTRACT_SESSION_IId_2d","Session IId: Very High-Energy Emission"]
    _sessions[31] = [8,"$ABSTRACT_SESSION_IIIc_3c","Session IIIc: Afterglow Observations"]
    _sessions[33] = [10,"$ABSTRACT_SESSION_IVb_4b","Session IVb: GRBs as Probes of the Early Universe"]
    _sessions[34] = [17,"$POSTERS_SESSION_PII_p2","P-II: Prompt and High-Energy Emission","II"]
    _sessions[35] = [18,"$POSTERS_SESSION_PIII_p3","P-III: Afterglow Emission","III"]
    _sessions[36] = [19,"$POSTERS_SESSION_PIV_p4","P-IV: Probes of the Early Universe","IV"]
    _sessions[37] = [20,"$POSTERS_SESSION_PV_p5","P-V: Progenitors and Central Engine Physics","V"]
    _sessions[38] = [21,"$POSTERS_SESSION_PVI_p6","P-VI: History and Future Instrumentation","VI"]
    _sessions[39] = [22,"$POSTERS_SESSION_PVII_p7","P-VII: Grav. Waves, Neutrinos, Cosmic Rays and UHE Emission","VII"]
    _sessions[40] = [23,"$POSTERS_SESSION_PVIII_p8","P-VIII: Host Galaxies","VIII"]
    self.sessions = _sessions
  
  def appendPresentation(self,raw_presentation):
    if not raw_presentation:
      return
    if int(raw_presentation['sp.sessionid']) not in self.sessions:
      print "UNDEFINED SESSION!"
      print raw_presentation
      print "PRESS ENTER TO SKIP"
      raw_input()
      return
    self.presentations.append(raw_presentation)
  
  def _order(self):
    '''Order self.presentations based on session, sequence'''
    self.presentations = sorted(self.presentations, key=lambda k: (self.sessions[int(k['sp.sessionid'])][0],int(k['sp.sequencenumber'])))
      

  def makeMaintex(self,filename="main.tex",template_abs='templates/abstract.tex',template_main='templates/main.tex'):
    self._order()

    #First: write abstracts###.tex
    fp = open(template_abs,'r')
    lines = fp.read()
    fp.close()
    
    _mapping = dict((i, []) for i in [self.sessions[k][1] for k in self.sessions])
    
    for p in self.presentations:
      header = self.sessions[int(p['sp.sessionid'])][1]
      tex = '%% %s\n%s' % (header,lines)

      if p['p.type'] == "poster":
        tex = tex.replace('$NUMBER','P-%s-%s' % (self.sessions[int(p['sp.sessionid'])][3],p['sp.sequencenumber']))
      else:
        tex = tex.replace('$NUMBER','')
      
      tex = tex.replace('$TITLE',p['p.title'])
      tex = tex.replace('$AUTHORS',p['p.authors'])
      tex = tex.replace('$AFFILIATIONS',p['p.affiliations'])
      tex = tex.replace('$TEXT',p['p.abstract'].replace('%','\\%'))
      
      if p['u.name'] in _invited_speakers:
        tex = tex.replace(p['u.name'],'%s (invited)' % p['u.name'])
      
      presenter = '%s, %s' % (p['u.name'],p['u.firstname'])
      if presenter == "von Kienlin, Andreas": #Won't sort properly if v is lowercase
        presenter = "Von Kienlin, Andreas"
      
      tex = tex.replace('$INDEX','\\tiny{%s}' % presenter)
      
      
      
      #Sanitize some errors
      tex = tex.replace('~','$\\sim$')
      tex = tex.replace('&','\\&')
      
      
      #if presenter not in tex:
      #  print "WARNING: Presenter [%s] not in author list [%s]" % (presenter,p['p.authors'])
        
      #tex = tex.replace(presenter,'\underline{%s}' % presenter)#Won't do anything if it isnt found
      
      
      fp = open('abstract%s.tex' % self.presentations.index(p),'w')
      _mapping[header].append('\include{abstract%s}' % self.presentations.index(p))
      fp.write(tex)
      fp.close()
    
    #Second: write main.tex
    fp = open(template_main,'r')
    lines = fp.read()
    fp.close()
    
    for key in _mapping:
      lines=lines.replace(key,'\n'.join(_mapping[key]))
    
    fp = open('main.tex','w')
    fp.write(lines)
    fp.close()
    
    print "[%s] written. Please run pdflatex on this file manually." % filename


  def makePoS(self): #Requested a special format from that guys that will do the proceedings
    
    fp = open('LOP.csv') #First read in LOP, since we queried this table seperatly from presentations, and now it is too late to change due to manual edits of both CSV files.
    lines = fp.readlines()
    fp.close()
    LOP = {}
    for line in lines:
      name,firstname,affiliation,email = line.split('|')
      LOP[name] = [firstname,affiliation,email]


    ascii = ''
    previous_session = 0
    for p in self.presentations:
      sessionID = int(p['sp.sessionid'])
      _cols = map(str.strip,[p['u.name'],p['u.firstname'],LOP[p['u.name']][1],LOP[p['u.name']][2],p['p.title']])
      if self.sessions[sessionID][0] != previous_session:
        previous_session = self.sessions[sessionID][0]
        ascii += '%s\n' % self.sessions[sessionID][2]
      ascii += '%s\n' % '|'.join(_cols)
      
    fp = open('SoP.txt','w')
    fp.write(ascii)
    fp.close()
    

def parse(line,newline='~!\n',field='|',keys=_keys):
  line = line.replace(newline,'') #Remove newline delimiter
  line = line.strip()
  if not line:
    return None
  line = line.split(field) #Field delimiter
  try:
    _d = dict((k, line[i]) for (i, k) in enumerate(keys))
  except:
    print "WARNING: Failed parse. Here is the offending line:\n"
    print line
    print "\nPRESS ENTER TO CONTINUE"
    raw_input()
    return None
  return _d


def main():
  myPresentations = presentations()

  fp = open('presentations.csv','r')
  read = fp.read()
  fp.close()
  lines = read.split('~!\n') #Newline delimiter
  for line in lines:
    myPresentations.appendPresentation(parse(line))
  myPresentations.makeMaintex()
  myPresentations.makePoS()
      
      


if __name__ == "__main__":
  #print "WARNING: Are you sure you want to run this script? It will revert ALL abstracts back to their database state.\nThis will DELETE ALL user edits to abstract*tex files! [yes/no]"
  #confirm = raw_input('')
  #if confirm != "yes":
  #  sys.exit('Exited.')
  main()
