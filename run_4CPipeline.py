#! /usr/bin/env python
# run: python2 ./run_4CPipeline.py ../10_Adrien_Translocation_Detection/fastqs/MN00149_0303/VPinfo.txt --limit_to=2 --run_name=MN00149_0303
import argparse
import sys
import pandas as pd
import numpy as np
from os import path, makedirs, environ, system
from shutil import copy
import re
from string import lower

# set debug mode
if 'PYCHARM_HOSTED' in environ:
    print '[w] This script is being run interactively. Running in debug mode!'
    sys.argv = ['./run_4CPipeline.py', '../10_Adrien_Translocation_Detection/backup/vp_info.txt', '--limit_to=5']

# process input arguments
parser_obj = argparse.ArgumentParser(description='Job submitter for processing 4C runs',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_obj.add_argument('vp_info', default=None, type=str, help='VP info file of the runs.')
parser_obj.add_argument('--input_dir', default='../14_Demultiplexing_4C_runs/fastq_passed', type=str, help='Input dir for storing source fastq files.')
parser_obj.add_argument('--run_name', default='VER3500', type=str, help='Name of sequencing run')
parser_obj.add_argument('--output_dir', default='./Output/', type=str,
                        help='Output dir for processing runs.')
parser_obj.add_argument('--limit_to', default=None, type=str,
                        help='Process experiments in given set of source FASTQ indices only.')
inp_args = parser_obj.parse_args(sys.argv[1:])

# load vp info file
vpi_all = pd.read_csv(inp_args.vp_info, sep='\t')
assert len(np.unique(vpi_all['expname'])) == vpi_all['expname'].shape[0]

# group experiments according to source fastq files
expr_grp = vpi_all.groupby('fastq', sort=False)
print '[i] Found {:d} source FASTQ files.'.format(expr_grp.ngroups)
if not inp_args.limit_to:
    inp_args.limit_to = range(expr_grp.ngroups)
else:
    inp_args.limit_to = [int(x) for x in inp_args.limit_to.split(',')]
    print '[i] Limiting demux to following source indices: {:s}'.format(str(inp_args.limit_to))

# loop over experiments
for grp_idx, (fastq_name, expr_pd) in enumerate(expr_grp):
    if not grp_idx in inp_args.limit_to:
        continue
    source_name = re.sub('\..*', '', fastq_name)
    source_fqname = '{:s}/{:s}/{:s}'.format(inp_args.input_dir, inp_args.run_name, fastq_name)
    if not path.isfile(source_fqname):
        print '{:2d}: Source not found, submission ignored: {:s}'.format(grp_idx, fastq_name)
        continue
    else:
        print '{:2d}: Submitting a job for {:s}'.format(grp_idx, fastq_name)

    # prepare the pipeline
    output_path = '{:s}/{:s}/{:s}/'.format(inp_args.output_dir, inp_args.run_name, source_name)
    if not path.isdir(output_path):
        makedirs(output_path)
    # copy('./side_analysis/08_4CPipeline_Commit0a58396/conf.yml', output_path)
    # copy('./side_analysis/08_4CPipeline_Commit0a58396/functions.R', output_path)
    # copy('./side_analysis/08_4CPipeline_Commit0a58396/pipe4C.R', output_path)

    # add vp info file
    vpi_fname = output_path + 'input_vpinfo.txt'
    expr_pd.to_csv(vpi_fname, sep='\t', index=False)

    # make qsub command
    cmd = 'module load R/3.5.1; ' + \
          'Rscript ./pipe4C.R ' + \
          '--vpFile {:s} --readsQuality 1 --cores 6 --plot '.format(vpi_fname) + \
          '--fqFolder {:s}/{:s}/ '.format(inp_args.input_dir, inp_args.run_name) + \
          '--outFolder {:s}'.format(output_path)
    qsub_cmd = 'qsub -P hub_laat -N p4c_{:s} '.format(source_name) + \
               '-l h_rt=30:00:00 -l h_vmem=20G -pe threaded 6 ' + \
               '~/bulk/bin/run_script.sh "{:s}"'.format(cmd)

    # submission
    print 'Command to submit:\n{:s}'.format(qsub_cmd)
    # if lower(raw_input('Should I submit (y/N)? ')) == 'y':
    system(qsub_cmd)

