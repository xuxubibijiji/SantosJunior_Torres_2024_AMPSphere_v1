# clustering_analysis.py

import gzip
from Bio import SeqIO
import math

def seqload(file_path='../../data_folder/AMPSphere_v.2022-03.faa.gz'):
    """
    Load sequences from a gzipped FASTA file.
    :param file_path: Path to the gzipped FASTA file containing sequences.
    :return: Dictionary where keys are sequence IDs and values are sequences.
    """
    sequences = {}
    with gzip.open(file_path, 'rt', encoding='utf-8') as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            sequences[record.id] = str(record.seq)
    return sequences

def f_evalue(seq1, score, use_gap_penalty=False):
    """
    Calculate the e-value for a sequence alignment score.
    :param seq1: The query sequence.
    :param score: Alignment score from pairwise alignment.
    :param use_gap_penalty: Whether to use gap penalties in the calculation.
    :return: Calculated e-value.
    """
    # Statistical constants
    K = 0.13  # Scaling constant
    Lambda = 1.37  # Statistical parameter
    
    # Effective length correction
    effective_length = len(seq1)
    
    # Calculate e-value
    e_value = K * effective_length * math.exp(-Lambda * score)
    
    # Apply additional penalty if specified
    if use_gap_penalty:
        e_value *= 1.5  # Example adjustment for gap penalties
    
    return e_value
