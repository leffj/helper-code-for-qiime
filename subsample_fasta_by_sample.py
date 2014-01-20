#!/usr/bin/env python
from __future__ import division

__author__ = "Jonathan Leff"
__version__ = "0.0.1"

from os.path import split, splitext
from qiime.util import parse_command_line_parameters, get_options_lookup,\
 make_option
from cogent.parse.fasta import MinimalFastaParser
import re
from random import random
import sys

options_lookup = get_options_lookup()

script_info={}
script_info['brief_description']="""Randomly subsample a number of sequences per sample from a given fasta file"""
script_info['script_description']="""Subsample the seqs.fna file, randomly select a specified number of seqs per sample"""
script_info['script_usage']=[]
script_info['script_usage'].append(("""Example:""","""Subsample seqs.fasta to 10,000 sequences per sample""","""%prog -i $PWD/seqs.fna -n 10000 -o $PWD/subsampled_seqs.fna"""))
script_info['output_description']=""""""
script_info['required_options']=[\
   options_lookup['fasta_as_primary_input'],\
   make_option('-n','--number_subsample',action='store',type='int',\
        help='Specify the number of sequences per sample to subsample')
]
script_info['optional_options']=[\
   options_lookup['output_fp']\
] 
script_info['version'] = __version__

#http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
      
    verbose = opts.verbose
    
    input_fasta_fp = opts.input_fasta_fp
    output_fp = opts.output_fp
    number_subsample = opts.number_subsample
    
    if number_subsample <= 0:
        raise ValueError,('number_subsample must be >0')
    
    # if the output fp isn't specified, create one
    if not output_fp:
        input_file_basename, input_file_ext = \
         splitext(split(input_fasta_fp)[1])
        output_fp = '%s_subsample_%s%s' % (input_file_basename,
         number_subsample,input_file_ext)

    input_fasta = open(input_fasta_fp, "U")

    # count the number of seqs for each unique sample
    number_seqs_bySample = {}
    for label, seq in MinimalFastaParser(input_fasta):
        matchID = re.match('(^.*?)_(.*)$',label)
        sampleID = matchID.group(1)
        if sampleID in number_seqs_bySample:
            number_seqs_bySample[sampleID] += 1
        else:
            number_seqs_bySample[sampleID] = 1

    # get the number of sequences in the file to support progress status
    numberSeqs = file_len(input_fasta_fp) / 2

    # write a seq the proportion of the time (for each sample) that will give 
    # approx the right amount of seqs per sample
    input_fasta = open(input_fasta_fp, "U")
    output_fasta = open(output_fp, "w")
    i = 0
    for label, seq in MinimalFastaParser(input_fasta):
        matchID = re.match('(^.*?)_(.*)$',label)
        sampleID = matchID.group(1)
        prop = number_subsample / number_seqs_bySample[sampleID]
        if random() <= prop:
            output_fasta.write('>%s\n%s\n' % (label, seq))
        # for progress status
        i += 1
        sys.stdout.write('\r')
        sys.stdout.write('[%s]' % (i / numberSeqs * 100))
        sys.stdout.flush()

    sys.stdout.write('\n')

         
    input_fasta.close()
    output_fasta.close()
        


if __name__ == "__main__":
    main()
