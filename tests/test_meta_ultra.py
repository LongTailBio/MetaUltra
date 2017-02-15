#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_meta_ultra
----------------------------------

Tests for `meta_ultra` module.
"""

import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from meta_ultra import meta_ultra
from meta_ultra import cli
from meta_ultra.sample_manager import *
import meta_ultra.config 

class Test_meta_ultra(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

            
    def test_add_single_ended_seq_data(self):
        filenames = ['test1.fastq.gz', 'test2.fastq.gz', 'test3.fastq.gz']
        metadata = {
            'TEST1' : {'foo1':'bar1'},
            'TEST2' : {'foo2':'bar2'},
            'TEST3' : {'foo3':'bar3'},
            }
        sampleNameFunc = lambda x: x.upper()
        metadataFunc = lambda sname: metadata[sname]
        add_single_ended_seq_data('test-project',
                                  filenames,
                                  '.fastq.gz',
                                  SequencingRun(machine_type='fooseq'),               
                                  101,
                                  sampleNameFunc=sampleNameFunc,
                                  metadataFunc=metadataFunc)


        db = TinyDB(config.db_file)
        sampleTbl = db.table(config.db_sample_table)
        seqDataTbl = db.table(config.db_seq_data_table)
        self.assertEqual(len(sampleTbl.all()), 3)
        self.assertEqual(len(seqDataTbl.all()), 3)

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'meta_ultra.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


def suite():
    suite = unittest.TestSuite()
    suite.addTest( Test_meta_ultra('test_add_single_ended_seq_data'))
    suite.addTest( Test_meta_ultra('test_command_line_interface'))
    return suite


if __name__ == '__main__':
    unittest.main()
