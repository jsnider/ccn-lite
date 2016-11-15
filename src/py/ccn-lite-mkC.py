#from subprocess import call

#call("/home/josn3503/ccn-lite/bin/ccn-lite-mkC -i /home/josn3503/ccn-lite/src/py/file_one.txt -s ndn2013 '/ndn/test/mycontent' > /home/josn3503/ccn-lite/test/ndntlv/mycontent.ndntlv", shell=True)


#call("echo 'hello johan'",stdout=subprocess.PIPE, shell=True)

#call("/home/josn3503/ccn-lite/bin/ccn-lite-mkC -i /home/josn3503/ccn-lite/src/py/file_one.txt -s ndn2013 '/ndn/test/mycontent' > /home/josn3503/ccn-lite/test/ndntlv/mycontent.ndntlv", stdin=subprocess.PIPE, shell=True)


'''
import subprocess

proc = subprocess.Popen(['/home/josn3503/ccn-lite/bin/ccn-lite-mkC', 
						 '-s', 'ndn2013',
						 '/ndn/test/mycontent'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
stdout_value = proc.communicate("what the flerp")[0]
print '\tpass through:', repr(stdout_value)

'''


'''

import subprocess

cat = subprocess.Popen(['ls', '-l'], 
                        stdout=subprocess.PIPE,
                        )

grep = subprocess.Popen(['grep', 'android'],
                        stdin=cat.stdout,
                        stdout=subprocess.PIPE,
                        )



end_of_pipe = grep.stdout

print 'Included files:'
for line in end_of_pipe:
    print '\t', line.strip()
    '''