#!/usr/bin/python
import sys
from cryptos import *
import time
import os


def main():

    # Remember time
    starttime = time.time()

    if len(sys.argv) < 1:
        print ("Please give the path and textfile that you want to convert to unique lines")
    else:
        filename = sys.argv[1]

        # Counter to 0
        dummycounter = 0

        if os.path.exists(filename) == False:
            print ("File does not exist")
        else:

            # The NEW filename to store the unique lines
            newfilename = filename[:len(filename) - 4] + "_pub2addr.txt"

            # Remove NEW file if it exists (if you want to, otherwise if already there it appends)
            if os.path.exists(newfilename):
                os.remove(newfilename)

            # Open NEW file
            newfile = open(newfilename, "at")

            # Start the essentials
            # --------------------
            with open(filename, "rt") as source:
                for dummyline in source:
                    if dummycounter % 1000 == 0: # Some stuff for the stat's and output
                        dummytext = "Public Keys converted: " + f"{dummycounter:,d}"
                        dummytext = dummytext.format().replace(",", ".")
                        print (dummytext)
                        # For debug
                        #print (dummyline[:len(dummyline) - 1])
                    dummycounter = dummycounter + 1
                    if len(dummyline) > 1: # Line empty?
                        # Copy line without ENTER
                        dummycopyofdummyline = dummyline[:len(dummyline) - 1]

                        # If public key is leveldb compressed then uncompress
                        if len(dummycopyofdummyline) <= 66:
                            # For debug
                            #print("smaller then 67")
                            #print(dummycopyofdummyline[0:2] + " " + dummycopyofdummyline[2:])

                            if dummycopyofdummyline[0:2] == "04": # 04=even then put 02=even
                                # For debug
                                #print("04 leveldb compressed pub key found")
                                dummycopyofdummyline = "02" + dummycopyofdummyline[2:]
                                dummycopyofdummyline = encode_pubkey(dummycopyofdummyline, "hex")
                            if dummycopyofdummyline[0:2] == "05": # 05=odd then put 03=odd
                                # For debug
                                #print("05 leveldb compressed pub key found")
                                dummycopyofdummyline = "03" + dummycopyofdummyline[2:]
                                dummycopyofdummyline = encode_pubkey(dummycopyofdummyline, "hex")

                        # Convert to address
                        address = pubkey_to_address(dummycopyofdummyline)

                        # For debug
                        #print (address_from_hex)
                        newfile.writelines(address + "\n")

            # End the essentials
            # ------------------

            # Close source file
            source.close()

            # Final stat's
            dummytext = "Public Keys converted: " + f"{dummycounter:,d}"
            dummytext = dummytext.format().replace(",", ".")
            print(dummytext)

            # Close NEW file
            newfile.close()

    # Calculate elapsed time
    endtime = time.time()

    print ("Complete Runtime:")
    print ("Minutes: " + str((endtime - starttime) / 60))
    print ("Hours  : " + str((endtime - starttime) / (60 * 60)))
    print ("Days   : " + str((endtime - starttime) / (60 * 60 * 24)))


if __name__ == '__main__':
    main()
