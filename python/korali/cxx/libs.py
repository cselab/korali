def getlibs(extdir):
  fixedflags = '-L' + extdir + ' -L' + extdir + '/../../../../lib' + ' -L' + extdir + '/../../../../lib64'
  print(fixedflags + ' ') 
