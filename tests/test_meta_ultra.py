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
            'SE_TEST1' : {'foo1':'bar1'},
            'SE_TEST2' : {'foo2':'bar2'},
            'SE_TEST3' : {'foo3':'bar3'},
            }
        sampleNameFunc = lambda x: 'SE_' + x.upper()
        metadataFunc = lambda sname: metadata[sname]
        seqRun = SingleEndedSequencingRun(name='test_experiment',machine_type='fooseq')
        seqRun.save()
        self.assertTrue(seqRun.exists())
        samples, seqDats = add_single_ended_seq_data('test-project-single',
                                  filenames,
                                  '.fastq.gz',
                                            seqRun,
                                  101,
                                  sampleNameFunc=sampleNameFunc,
                                  metadataFunc=metadataFunc)

        for seqData in seqDats:
            self.assertTrue(seqData.exists())
        for sample in samples:
            self.assertTrue(sample.exists())

    def test_add_paired_ended_seq_data(self):
        filenames = ['test1_1.fastq.gz', 'test2_1.fastq.gz', 'test3_1.fastq.gz','test1_2.fastq.gz', 'test2_2.fastq.gz', 'test3_2.fastq.gz']
        metadata = {
            'PE_TEST1' : {'foo1':'bar1'},
            'PE_TEST2' : {'foo2':'bar2'},
            'PE_TEST3' : {'foo3':'bar3'},
            }
        sampleNameFunc = lambda x: 'PE_' + x.upper()
        metadataFunc = lambda sname: metadata[sname]
        seqRun = PairedEndedSequencingRun(name='test_experiment_2',machine_type='fooseq2')
        seqRun.save()
        self.assertTrue(seqRun.exists())
        samples, seqDats = add_paired_ended_seq_data('test-project-paired',
                                  filenames,
                                  '_1.fastq.gz',
                                  '_2.fastq.gz',
                                            seqRun,
                                  101,
                                  aveGapLen=180,
                                  sampleNameFunc=sampleNameFunc,
                                  metadataFunc=metadataFunc)


        for seqData in seqDats:
            self.assertTrue(seqData.exists())
        for sample in samples:
            self.assertTrue(sample.exists())

    def test_save_and_recreate(self):
        filenames = ['recreate_test1.fastq.gz']
        seqRun = SingleEndedSequencingRun(name='test_experiment_save_test',machine_type='fooseq')
        seqRun.save()
        SingleEndedSequencingRun( **seqRun.record())
        samples, seqDats = add_single_ended_seq_data('test-project-single',
                                  filenames,
                                  '.fastq.gz',
                                            seqRun,
                                    101,)

        for seqData in seqDats:
            SingleEndedSeqData(**seqData.record())
        for sample in samples:
            Sample(**sample.record())

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0


def suite():
    suite = unittest.TestSuite()
    suite.addTest( Test_meta_ultra('test_add_single_ended_seq_data'))
    suite.addTest( Test_meta_ultra('test_add_paired_ended_seq_data'))
    suite.addTest( Test_meta_ultra('test_save_and_recreate'))
    suite.addTest( Test_meta_ultra('test_command_line_interface'))
    return suite


if __name__ == '__main__':
    unittest.main()
