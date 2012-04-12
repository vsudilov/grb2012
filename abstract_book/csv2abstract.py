#csv2abstract.py
#vss april/2012

'''
Convert abstract sql from the query SELECT title, authors, affiliations, abstract FROM presentation  
(with pipe `|` as delimiter) to abstract###.tex
'''

__template_abstract = '''
%%\\anumber{%%s}

\\atitle{%s}

\\bigskip

\\bigskip

\\bigskip

\\authors{%s}

\\affiliation{%s}

\\bigskip

\\bigskip

\\bigskip

\\bigskip
\\noindent %s
'''
# % (title,authors,affiliations,abstract)





__template_main = '''
%%file main.tex
%%Adapted from
%%http://yetanotherbiochemblog.wordpress.com/2011/10/11/managing-conference-materials-in-latex-part-1-abstract-template/
\\documentclass[14pt,a5paper,twoside]{book}
\\usepackage[utf8x]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[english]{babel}
\\usepackage{fixltx2e}

\\usepackage{hyphenat}
\\usepackage[usenames,dvipsnames]{color}

%%a5 paper= 	148mm x 210mm
%%a4 paper=	210mm x 297mm
\\setlength\\hoffset{-0.79cm} %% 1
\\setlength\\oddsidemargin{0cm} %% 3
\\setlength\\evensidemargin{0cm} %% 3
\\setlength\\textwidth{110mm} %% 8
\\setlength\\voffset{-2.54cm} %% 2
\\setlength\\topmargin{1.1cm} %% 4
\\setlength\\headheight{0.7cm} %% 5
\\setlength\\headsep{0.4cm} %% 6
\\setlength\\textheight{170mm} %% 7
%%\\setlength\\footskip{1.0cm} %% 11
\\parindent=0cm
\\parskip=0.1cm

\\renewcommand{\\rmdefault}{ptm}

\\newcommand{\\anumber}[1]{\\leavevmode{\\textbf{#1}}}
\\newcommand{\\atitle}[1]{\\leavevmode{\\textbf{#1}}}
\\newcommand{\\affiliation}[1]{\\leavevmode{\\textit{#1}}}
\\newcommand{\\email}[1]{\\leavevmode{\\url{#1}}}
\\newcommand{\\presenting}[1]{\\leavevmode{\\textbf{\\underline{#1}}}}
\\newcommand{\\authors}[1]{\\textbf{#1}}

\\usepackage{graphicx}
\\usepackage{wrapfig}
\\newcommand{\\photo}[1]{
    \\begin{wrapfigure}[4]{o}{0.2\\textwidth}
    \\includegraphics[width=0.2\\textwidth]{#1}
    \\end{wrapfigure}
}

\\usepackage{fancyhdr}
\\renewcommand{\\headrulewidth}{0.2pt}
\\renewcommand{\\footrulewidth}{0.2pt}

\\newcommand{\\redefineheaders}[1]{
    \\pagestyle{fancy}
    \\fancyhf{}
    \\fancyhead[LO,RE]{\\textit{#1}}
    \\fancyhead[CO,CE]{}
    \\fancyhead[RO,LE]{}
    \\fancyfoot[RO,LE]{\\thepage}
    \\fancyfoot[CO,CE]{}
    \\fancyfoot[LO,RE]{\\textit{GRB 2012 - May 7-11, Munich, Germany}}
}

\\usepackage{enumerate}

\\usepackage{makeidx}
\\makeindex

\\begin{document}
\\title{Abstract book}
\\maketitle
\\redefineheaders{Monday, May 7}

%s

\\end{document}
'''
# % \include{abstracts###.tex}







def main():
  fp = open('presentations.csv','r')
  read = fp.read()
  fp.close()
  lines = read.split('~!') #Newline delimiter
  number = -1
  for line in lines:
    number+=1
    if not line:
      continue
    line = line.split('|') #Field delimiter
    print line
    try:
      title = line[0]
      authors = line[1]
      affiliations = line[2]
      abstract = line[3]
      #print 'title: %s' % title
      #print 'authors: %s' % authors
      #print 'affiliations: %s' % affiliations
      #print 'abstract: %s' % abstract
      print '%s' % (title)
      print "  ===> Adding to abstract%s.tex\n\n" % number
      fp = open('abstract%s.tex' % number,'w')
      #print __template_abstract % (number,title,authors,affiliations,abstract)
      fp.write(__template_abstract % (title,authors,affiliations,abstract))
      fp.close()
    except:
      print "WARNING: Failed parse"
      print line
      print "PRESS ENTER TO CONTINUE"
      raw_input()
      continue
      
  fp = open('main.tex','w')
  includes = '\n'.join(['\include{abstract%s}' % i for i in range(number)])
  fp.write(__template_main % (includes)) 
  fp.close()
  print "[main.tex] written. Please run pdflatex on this file manually."


if __name__ == "__main__":
  main()