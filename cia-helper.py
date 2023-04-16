#!/usr/bin/python3
# By Let's Shop team
# Tool to parse cias easily
# Heavily inspired by one of the examples
# Created with help from ZeroSkill

from pyctr.type.cia import CIAReader, CIASection, InvalidCIAError
from pyctr.crypto.engine import BootromNotFoundError
import sys, base64

if len(sys.argv) == 1:
    exit('Usage: ./cia-helper.py [cia file]')
try:
    try:
        try:
            try:
                with CIAReader(sys.argv[1]) as cia:
                    print("Welcome to CIA Helper! This tool is designed to help you adding a homebrew to Let's Shop.")
                    print("If the title needs to be downloaded with a redeemable card, please make the id like: 50000000000000")
                    print('Title ID:', cia.tmd.title_id.upper())
                    print('Title Version:',cia.tmd.title_version.__index__())
                    app = cia.contents[CIASection.Application]
                    app_title = app.exefs.icon.get_app_title('English')
                    print('Application Title:', app_title.short_desc)
                    print('Application Description:', app_title.long_desc)
                    print('Application Publisher:', app_title.publisher)
                    print('Product code:', app.product_code)
                    print('Size:', cia.total_size)
                    chunks = [ chunk for chunk in cia.tmd.chunk_records if chunk.cindex in cia.contents ]
                    filename = chunks[0].id.upper()
                    with open(filename+".app", 'wb') as file:
                        file.write(cia.open_raw_section(CIASection.Application).read())    
                    try:
                        filename = chunks[1].id.upper()    
                        with open(filename+".app", "wb") as file:
                            file.write(cia.open_raw_section(CIASection.Manual).read())
                        print("Note: a manual has been found and extracted to "+filename+".app.")
                    except IndexError:
                        pass    
                    try:
                        filename = chunks[2].id.upper()    
                        with open(filename+".app", "wb") as file:
                            file.write(cia.open_raw_section(CIASection.DownloadPlayChild).read())
                        print("Note: a download play app has been found and extracted to "+filename+".app.")
                    except IndexError:
                        pass             
                    with open("tmd.bin", 'wb') as file:
                        file.write(cia.open_raw_section(CIASection.TitleMetadata).read())
                    print('Finished! You can now put the tmd.bin and the .app file in cdn/'+cia.tmd.title_id.upper()+' (create the folder)')
                    print('Have a great day!')
            except BootromNotFoundError:
                print("Necessary files were not found. Please create a '3ds' directory in your home folder and put boot9.bin in it.")
        except FileNotFoundError:
            print("Your file does not exists.")
    except InvalidCIAError:
        print("Your file is not a CIA.")
except:
    print("Something wrong happened. Sorry! (try again)")