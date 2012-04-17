#makeIOP.py
#vss april/2012

'''
Parse the output from the sql query:

SELECT sp.sessionid, sp.sequencenumber, p.type, p.title, p.authors, p.affiliations, p.abstract
FROM session_presentation sp, presentation p, user u
WHERE p.id=sp.presentationid and u.invitationstatus='invited' and u.id=p.presenterid

and input the data to make an abstract book.
'''

_keys = ['sp.sessionid', 'sp.sequencenumber', 'p.type', 'p.title', 'p.authors', 'p.affiliations', 'p.abstract']

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
    _sessions[9] = [15,"$ABSTRACT_SESSION_VII_7","Session VII: Grav. Waves, Neutrinos, Cosmic Rays a..."]
    _sessions[22] = [3,"$ABSTRACT_SESSION_IIb_2b","Session IIb: Prompt Emission Spectroscopy"]
    _sessions[23] = [4,"$ABSTRACT_SESSION_IIc_2c","Session IIc: Prompt Emission Correlations and Temp..."]
    _sessions[24] = [7,"$ABSTRACT_SESSION_IIIb_3b","Session IIIb: Afterglow Observations"]
    _sessions[25] = [13,"$ABSTRACT_SESSION_Vc_5c","Session Vc: Central Engine Physics"]
    _sessions[27] = [5,"$ABSTRACT_SESSION_IId_2d","Session IId: Very High-Energy Emission"]
    _sessions[31] = [8,"$ABSTRACT_SESSION_IIIc_3c","Session IIIc: Afterglow Observations"]
    _sessions[33] = [10,"$ABSTRACT_SESSION_IVb_4b","Session IVb: GRBs as Probes of the Early Universe"]
    _sessions[34] = [17,"$POSTERS_SESSION_PII_p2","II"]
    _sessions[35] = [18,"$POSTERS_SESSION_PIII_p3","III"]
    _sessions[36] = [19,"$POSTERS_SESSION_PIV_p4","IV"]
    _sessions[37] = [20,"$POSTERS_SESSION_PV_p5","V"]
    _sessions[38] = [21,"$POSTERS_SESSION_PVI_p6","VI"]
    _sessions[39] = [22,"$POSTERS_SESSION_PVII_p7","VII"]
    _sessions[40] = [23,"$POSTERS_SESSION_PVIII_p8","VIII"]
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
    self.presentations = sorted(self.presentations, key=lambda k: (self.sessions[int(k['sp.sessionid'])][0],k['sp.sequencenumber']))
      

  def makeMaintex(self,filename="main.tex",template_IOP='templates/IOP.tex',template_main='templates/main.tex'):
    self._order()

    self._order()
    fp = open(template_IOP,'r')
    tex = fp.read()
    fp.close()
    
    _text = '\n'.join(['\\tiny %s &\\tiny %s & \\tiny %s & \\tiny %s \\\\ \\hline' % tuple([k[i] for i in _keys]) for k in self.users])
    #_text = _text.replace('@','\\MVAt')
    _text = _text.replace('_','\_')
    
    tex = tex.replace('$LOP',_text)
    
    fp = open('IOP.tex','w')
    fp.write(tex)
    fp.close()
    

def parse(line):
  line = line.replace('~!\n','') #Remove newline delimiter
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
  myPresentations = presentations()

  fp = open('presentations.csv','r')
  read = fp.read()
  fp.close()
  lines = read.split('~!\n') #Newline delimiter
  for line in lines:
    myPresentations.appendPresentation(parse(line))
  myPresentations.makeMaintex()
      
      
      


if __name__ == "__main__":
  main()
