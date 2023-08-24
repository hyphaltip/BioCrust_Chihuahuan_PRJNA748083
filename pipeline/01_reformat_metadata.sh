#!/usr/bin/bash -l
#SBATCH -p short --out logs/00_reformat_metdata.log

module load csvkit
IN=lib/PRJNA748083_metadata.csv
OUT=lib/PRJNA748083.csv
if [ ! -s $OUT ]; then
	cut -d, -f1,6,22,23,25,26,30,32,33,40,52,53,54,55 $IN > $OUT
fi
