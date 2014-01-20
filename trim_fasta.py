#!/usr/bin/env python
# File created on 09 Dec 2012
from __future__ import division

__author__ = "Jon Leff"
__copyright__ = ""
__credits__ = ["Jon Leff"]
__license__ = ""
__version__ = ""
__maintainer__ = "Jon Leff"
__email__ = "leff.jonathan@gmail.com"
__status__ = "Development"


from qiime.util import (parse_command_line_parameters,
                        make_option)
from cogent.parse.fasta import MinimalFastaParser

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = "Given an input fasta file, trim all seqs and quality strings to defined number of bases."
script_info['script_usage'] = [("","Trim fasta seqs/quals to 6 bases","trim_fasta.py -i in.fasta -o out.fasta -n 6")]
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

def trim_fasta(fasta_lines,output_length,exclude_shorter):
    """trim fasta seqs to output_length bases """
    for seq_id, seq in MinimalFastaParser(fasta_lines,strict=False):
    	if exclude_shorter and len(seq)<output_length:
    		continue
        yield '>%s\n%s\n' % (seq_id,seq[:output_length])

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    output_f = open(opts.output_fp,'w')
    for record in trim_fasta(open(opts.input_fp,'U'),opts.output_length,opts.exclude_shorter_seqs):
        output_f.write(record)
    output_f.close()


if __name__ == "__main__":
    main()