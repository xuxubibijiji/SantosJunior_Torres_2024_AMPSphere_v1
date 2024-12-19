import sys
import os
print("Current working directory:", os.getcwd())
print("Python search paths:", sys.path)
sys.path.append(os.path.join(os.getcwd(), "utils"))

#from utils.download_files import inputsgen
from utils.gtdb2pgenomes import conversion_from_GTDB_to_pGenomes
print("gtdb2pgenomes imported successfully!")

from utils.preprocess import filtermmseqs2_amp_contig
print("preprocess imported successfully!")

from utils.progenomes_genes import ampsphere2progenomes
print("progenomes_genes imported successfully!")

from utils.metadata import metadata
print("metadata imported successfully!")

from utils.addspecI import addspecI
print("addspecI imported successfully!")

from utils.hr_envo import hrenvo
print("hr_envo imported successfully!")


def main():
#    print('Download inputs')
#    inputsgen()
    print('Create conversion tables from GTDB into ProGenomes')
    conversion_from_GTDB_to_pGenomes()
    print('Linking taxonomy and GMSC genes')
    filtermmseqs2_amp_contig()
    print('Generating table of genes from ProGenomes2')
    ampsphere2progenomes()
    print('Processing metadata')
    metadata()
    print('Adding specI cluster info to the tables')
    addspecI()
    print('Adding metadata info and consolidating data')
    hrenvo()
    
