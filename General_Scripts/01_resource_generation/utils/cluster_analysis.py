def analyze_level_III(analysis_folder):
    '''
    Loads fasta file for AMPSphere and
    create a dataframe with the sequence,
    access and family; also computes
    the families which will be selected by
    size to next computations.
    '''
    import gzip
    import pandas as pd
    from collections import Counter
    from Bio import SeqIO

    # loading info about peptides and families
    infile = f'{analysis_folder}/AMPSphere_v.2022-03.faa.gz'
    lv3 = dict()
    for record in SeqIO.parse(gzip.open(infile,
                                        'rt',
                                        encoding='utf-8'),
                              'fasta'):
        lv3[record.id] = [str(record.seq),
                          record.description.split(' | ')[1]]

    # selecting families of at least 8 peptides
    select_fam = [v[1] for k, v in lv3.items()]
    select_fam = [k for k, v in Counter(select_fam).items() if v >= 8]
    select_fam = sorted(select_fam)

    # converting dictionary to a dataframe
    lv3 = pd.DataFrame.from_dict(lv3,
                                 orient='index',
                                 columns=['sequence',
                                          'family'])
    lv3 = lv3.reset_index()
    lv3 = lv3.rename({'index': 'access'}, axis=1)

    return (lv3, select_fam)


def organize_house(analysis_folder):
    '''
    Create folders to receive the data generated
    by this script
    '''
    import os

    # creating folders for results
    os.makedirs(f'{analysis_folder}/families', exist_ok=True)
    subdirs = ['fastas',
               'aln',
               'tree_nwk',
               'tree_fig',
               'hmm',
               'hmm_logo']

    for folder in subdirs:
        os.makedirs(f'{analysis_folder}/families/{folder}',
                    exist_ok=True)


def fasta_files(lv3, select_fam, analysis_folder):
    '''
    Generates the fasta files per family
    '''
    # computing results per family
    by_family = lv3.groupby('family').groups
    for f, ixs in by_family.items():
        df = lv3.loc[ixs]
        ofile = f'{analysis_folder}/families/fastas/{f}.faa'
        with open(ofile, 'w') as db:
            for row in df.itertuples():
                db.write(f'>{row.access}\n{row.sequence}\n')


def alignments(select_fam, analysis_folder): 
    '''
    Computes alignments from
    the fasta files generated
    before
    '''
    import subprocess
    import os

    # 检查 muscle 的可执行文件路径
    muscle_path = subprocess.run(["which", "muscle"], stdout=subprocess.PIPE, text=True).stdout.strip()
    if not muscle_path:
        raise FileNotFoundError("muscle executable not found. Please install muscle or check its PATH.")

    for f in select_fam:
        f = 'SPHERE-III.000_002'  # 示例文件名
        ifile = os.path.join(analysis_folder, 'families/fastas', f"{f}.faa")
        ofile = os.path.join(analysis_folder, 'families/aln', f"{f}.aln")

        # 检查输入文件是否存在
        if not os.path.exists(ifile):
            raise FileNotFoundError(f"Input file not found: {ifile}")

        # 调用 muscle
        subprocess.check_call([
            muscle_path,
            '-in', ifile,
            '-out', ofile,
            '-maxiters', '1',
            '-diags'
        ])



def trees(select_fam, analysis_folder):
    '''
    Computes trees and their ascII representation
    from the alignment files generated before
    '''
    from .phylogen import treebuilder, draw_ascii

    for f in select_fam:
        # compute tree
        ofile = f'{analysis_folder}/families/tree_nwk/{f}.nwk'
        i2file = f'{analysis_folder}/families/aln/{f}.aln'
        treebuilder(i2file,
                    ofile,
                    'WAG+CAT',
                    1000)

        # compute image
        ifile = f'{analysis_folder}/families/tree_nwk/{f}.nwk'
        ofile = f'{analysis_folder}/families/tree_fig/{f}.ascii'
        draw_ascii(ifile,
                   ofile,
                   column_width=80)


def hmm(select_fam, data_folder, analysis_folder):
    '''
    Computes HMM profile and logo
    from the alignment files generated before
    '''
    from utils.hmm import hbuild

    for f in select_fam:
        # computing HMM profile
        ofile = f'{analysis_folder}/families/hmm/{f}.hmm'
        i2file = f'{analysis_folder}/families/aln/{f}.aln'

        hbuild(i2file,
               ofile,
               f)


def hmmlogo(select_fam, data_folder, analysis_folder):
    '''
    Computes HMM logo for each family
    '''
    import lzma
    from .hmm import pict_hmmlogo

    for f in select_fam:
        # computing HMM logo
        alph = lzma.open(f'{data_folder}/alph.json')
        cmap = lzma.open(f'{data_folder}/cmap.json')
        ifile = f'{analysis_folder}/families/hmm/{f}.hmm'
        ofile = f'{analysis_folder}/families/hmm_logo/{f}.svg'
        pict_hmmlogo(alph, cmap, ifile, ofile)


def process_cluster():
    import os

    data_folder = 'data/'
    analysis_folder = 'analysis/'

    for folder in [data_folder, analysis_folder]:
        os.makedirs(folder, exist_ok=True)

    print('Retrieve sequences and families')
    lv3, select_fam = analyze_level_III(analysis_folder)
    print('Generate folders')
    organize_house(analysis_folder)
    print('Generate fasta per family')
    fasta_files(lv3, select_fam, analysis_folder)
    print('Align peptides')
    alignments(select_fam, analysis_folder)
    print('Drawing trees')
    trees(select_fam, analysis_folder)
    print('Calculating Hidden Markov Models')
    hmm(select_fam, data_folder, analysis_folder)
    print('Calculating HMM logos')
    hmmlogo(select_fam, data_folder, analysis_folder)

