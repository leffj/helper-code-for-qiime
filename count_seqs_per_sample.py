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

options_lookup = get_options_lookup()

script_info={}
script_info['brief_description']="""Print sequences per sample from a given fasta file"""
script_info['script_description']="""seqs per sample"""
script_info['script_usage']=[]
script_info['script_usage'].append(("""Example:""","""Print sequences per sample""","""%prog -i $PWD/seqs.fna -o $PWD/subsampled_seqs.fna"""))
script_info['output_description']=""""""
script_info['required_options']=[\
   options_lookup['fasta_as_primary_input']\
]
script_info['optional_options']=[\
   options_lookup['output_fp']\
] 
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
      
    verbose = opts.verbose
    
    input_fasta_fp = opts.input_fasta_fp
    output_fp = opts.output_fp
    
    # if the output fp isn't specified, create one
    if not output_fp:
        input_file_basename, input_file_ext = \
         splitext(split(input_fasta_fp)[1])
        output_fp = '%s_counts.txt' % (input_file_basename)

    input_fasta = open(input_fasta_fp, "U")

    output_fasta = open(output_fp, "w")

    # count the number of seqs for each unique sample
    number_seqs_bySample = {}
    for label, seq in MinimalFastaParser(input_fasta):
        matchID = re.match('(^.*?)_(.*)$',label)
        sampleID = matchID.group(1)
        if sampleID in number_seqs_bySample:
            number_seqs_bySample[sampleID] += 1
        else:
            number_seqs_bySample[sampleID] = 1
    for key in number_seqs_bySample:
        output_fasta.write('%s\t%s\n' %(key,number_seqs_bySample[key]))

    input_fasta.close()


if __name__ == "__main__":
    main()
