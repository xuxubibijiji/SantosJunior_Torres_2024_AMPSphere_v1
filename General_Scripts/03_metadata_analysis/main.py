import sys
import os
sys.path.append(os.path.join(os.getcwd(), "utils"))

#from utils.download_files import inputsgen
from utils.gtdb2pgenomes import conversion_from_GTDB_to_pGenomes
from utils.preprocess import filtermmseqs2_amp_contig
from utils.progenomes_genes import ampsphere2progenomes
from utils.metadata import metadata
from utils.addspecI import addspecI
from utils.hr_envo import hrenvo

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
    
