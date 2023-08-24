#!/usr/bin/env python3
import os, re
import pandas as pd
import argparse
import urllib.request
import textwrap
# RDP looks like this
# AJ000684_S000004347;tax=d:Bacteria,p:"Actinobacteria",c:Actinobacteria,o:Actinobacteridae,f:Actinomycetales,g:Corynebacterineae;

#'Domain': 'd',
taxlevels = {    
            'Domain': 'k',
            'Phylum': 'p',
            'Class': 'c',
            'Order': 'o',
            'Family': 'f',
            'Genus': 'g'
#            'Species': 's'
}
cyanodbXLS = "https://zenodo.org/record/7864137/files/CyanoSeq_1.2.xlsx?download=1"
fname = 'CyanoSeq_1.2.xlsx'
outname = 'lib/CyanoSeq_1.2.fa'

outtype = 'unite'
if os.path.exists(fname):
    df = pd.read_excel(fname)
else:
    df = pd.read_excel(cyanodbXLS)

with open(outname,'w') as outfh:
    for index,row in df.iterrows():
        #print(index,row)
        taxl = []
        for t in taxlevels:
            if outtype == 'unite':
                taxl.append(f'{taxlevels[t]}__{row[t]}')
            else:
                taxl.append(f'{taxlevels[t]}:{row[t]}')
        species = ""
        taxstr = ""
        if outtype == 'unite':
            if f'{row["Species"]}' != "nan":
                species = f'{row["Genus"]}_{row["Species"]}'
                taxl.append(f's__{species}')
            taxstr = ";".join(taxl)
        else:
            taxstr = ",".join(taxl)

        seqstr = re.sub(r'\-','',f"{row['Sequence_Long']}")
        if seqstr != 'nan':
            if outtype == 'unite':
                outfh.write(f">{species}|{row['Genbank_accession']}|{row['Genbank_accession']}|reps|{taxstr}\n")
            else:
                outfh.write(f">{row['Genbank_accession']};tax={taxstr}\n")
            #outfh.write(textwrap.fill(seqstr,width=60) + "\n")
            outfh.write(seqstr + "\n")
