from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.template.loader  import get_template

import subprocess
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import os


def execute (template, request ):
    hash_type = 'NTLM'
    wordlist_location = './wordlist.txt'
    output_file = './output.txt'
    hash_file = './hashfile.txt'

    hash_modes={'NTLM':'1000', 'MD5':'0'}

    hashcat_command = f"hashcat -m { hash_modes[hash_type.upper()] } -a 0 -w {wordlist_location} --potfile-disable --remove --outfile {output_file} --threads 4 {hash_file}"

    try:
        with subprocess.Popen(hashcat_command) as p:
            for line in p.stdout:
                yield( template.render({"line": line} ) )
            if p.returncode == 0:
                k = open (output_file,'r')
                for x in k.readlines():
                    yield ( template.render({"line": x}) )
                
    except Exception as e:
        yield ( template.render({"line": f"Error executing dehashing command: {e}"} ) )

def executor ( request ):

    template = get_template("dehash.html")
    return StreamingHttpResponse( execute( template, request ) )  


    
