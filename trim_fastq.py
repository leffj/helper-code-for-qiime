#!/usr/bin/env python
# File created on 05 Mar 2012
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

# note: edited by Jon Leff to pull trim_fastq library script

from qiime.util import (parse_command_line_parameters,
                        make_option)
from qiime.parse import MinimalFastqParser

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = "Given an input fastq file, trim all seqs and quality strings to defined number of bases."
script_info['script_usage'] = [("","Trim fastq seqs/quals to 6 bases","trim_fastq.py -i in.fastq -o out.fastq -n 6")]
script_info['output_description']= ""
script_info['required_options'] = [
 make_option('-i','--input_fp',type="existing_filepath",help='the input fastq filepath'),\
 make_option('-o','--output_fp',type="new_filepath",help='the output fastq filepath'),\
 make_option('-n','--output_length',type="int",help="the length of the output sequences"),\
]
script_info['optional_options'] = [
 make_option('-s','--exclude_shorter_seqs',default=False,action='store_true',help="exclude sequences shorter than the output length [default=%default]"),\
]
script_info['version'] = __version__


def trim_fastq(fastq_lines,output_length,exclude_shorter):
    """trim fastq seqs/quals to output_length bases """
    for seq_id, seq, qual in MinimalFastqParser(fastq_lines,strict=False):
    	if exclude_shorter and len(seq)<output_length:
    		continue
        yield '@%s\n%s\n+%s\n%s\n' % (seq_id,seq[:output_length],
                                      seq_id,qual[:output_length])

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    output_f = open(opts.output_fp,'w')
    for record in trim_fastq(open(opts.input_fp,'U'),opts.output_length,opts.exclude_shorter_seqs):
        output_f.write(record)
    output_f.close()


if __name__ == "__main__":
    main()