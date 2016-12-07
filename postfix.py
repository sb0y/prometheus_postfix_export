#!/usr/bin/python3
# coding: utf-8

import string
import os
import subprocess
import time

#deferred.value `(test -d deferred && find deferred -type f ) | wc -l`
#active.value `(test -d active && find active -type f ) | wc -l`
#maildrop.value `(test -d maildrop && find maildrop -type f ) | wc -l`
#incoming.value `(test -d incoming && find incoming -type f ) | wc -l`
#corrupt.value `(test -d corrupt && find corrupt -type f ) | wc -l`
#hold.value `( test -d hold && find hold -type f ) | wc -l`

os.chdir( "/var/spool/postfix" )

def runCmd( cmd ):
    output,error = subprocess.Popen(cmd, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    if( error ):
        print("Error: " + error.decode(), file=sys.stderr)
        return ""
    
    return output.decode()

def runCmdTpl( tplID ):
    tpl = '(test -d {0} && find {1} -type f ) | wc -l'.format( tplID, tplID )
    ret = runCmd( tpl )
    return ret

def getIntFromCmd( tplID ):
    return float( runCmdTpl( tplID ) )

def write( tplID ):
    tpl = '''script_postfix_{0}{{hostname="{1}"}} {2}'''.format( tplID, socket.gethostname(), getIntFromCmd( tplID ) )
    with open( '/var/run/node-exporter-scandir/postfix.prom.$$', 'a') as f:
        f.write( tpl + "\n" )

write( 'deferred' )
write( 'active' )
write( 'maildrop' )
write( 'incoming' )
write( 'corrupt' )
write( 'hold' )

os.rename( '/var/run/node-exporter-scandir/postfix.prom.$$', '/var/run/node-exporter-scandir/postfix.prom' )
