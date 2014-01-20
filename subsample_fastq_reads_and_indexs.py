#!/usr/bin/env python
from __future__ import division

__author__ = "Jonathan Leff"
__version__ = "0.0.1"

from os.path import split, splitext
from cogent.util.misc import create_dir
from qiime.util import parse_command_line_parameters, get_options_lookup,\
 make_option
from cogent.parse.fastq import MinimalFastqParser
from random import random
from itertools import izip

options_lookup = get_options_lookup()

script_info={}
script_info['brief_description']="""Randomly subsample an approx proportion of sequences from read and index fastq files"""
script_info['script_description']="""Subsample the read.fastq and index.fastq file, randomly select a specified proportion of reads"""
script_info['script_usage']=[]
script_info['script_usage'].append(("""Example:""","""Subsample a proportion of 0.05""","""%prog -i $PWD/reads.fastq -b indexs.fastq -p 0.05 -o $PWD/subsampled_seqs"""))
script_info['output_description']=""""""
script_info['required_options']=[\
   make_option('-i','--sequence_reads_fp',type="existing_filepath",\
        help='The sequence reads in fastq format'),
   make_option('-p','--proportion_subsample',action='store',type='float',\
        help='Specify the approx proportion of sequences to subsample'),
   make_option('-b','--index_reads_fp',type="existing_filepath",\
        help='The index (barcode) reads in fastq format')
]
script_info['optional_options']=[\
   options_lookup['output_dir']\
] 
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
      
    verbose = opts.verbose
    
    sequence_reads_fp = opts.sequence_reads_fp
    output_dir = opts.output_dir
    proportion_subsample = opts.proportion_subsample
    index_reads_fp = opts.index_reads_fp
    
    if proportion_subsample > 1 or proportion_subsample <= 0:
        raise ValueError,('proportion_subsample must be in range of 0-1')
    

    # if the output dir isn't specified, create one
    if not output_dir:
        input_file_basename, input_file_ext = \
         splitext(split(sequence_reads_fp)[1])
        output_dir = '%s_subsample/' % (input_file_basename)
    create_dir(output_dir)

    # prepare output files
    input_file_basename, input_file_ext = \
     splitext(split(sequence_reads_fp)[1])
    output_reads_fp = '%s_subsample%s' % (input_file_basename,
         input_file_ext)

    input_file_basename, input_file_ext = \
     splitext(split(index_reads_fp)[1])
    output_indexs_fp = '%s_subsample%s' % (input_file_basename,
         input_file_ext)

    # randomly subsample
    sequence_reads = open(sequence_reads_fp, "U")
    index_reads = open(index_reads_fp, "U")
    output_reads = open('%s/%s' %(output_dir,output_reads_fp), "w")
    output_indexs = open('%s/%s' %(output_dir,output_indexs_fp), "w")
    for (label, seq, qual), (labelI, seqI, qualI) in izip(MinimalFastqParser(sequence_reads,strict=False),MinimalFastqParser(index_reads,strict=False)):
        if random() < proportion_subsample:
            output_reads.write('@%s\n%s\n+\n%s\n' % (label, seq, qual))
            output_indexs.write('@%s\n%s\n+\n%s\n' % (labelI, seqI, qualI))
         
    sequence_reads.close()
    index_reads.close()
    output_reads.close()
    output_indexs.close()



if __name__ == "__main__":
    main()
