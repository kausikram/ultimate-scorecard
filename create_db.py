#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Kausikram
#
# Created:     11-10-2012
# Copyright:   (c) Kausikram 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from models import *

def main():
    Team.create_table()
    Match.create_table()
    SpiritScore.create_table()
    MatchTeam.create_table()

if __name__ == '__main__':
    main()
