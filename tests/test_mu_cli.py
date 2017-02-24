#!/usr/bin/env python

import os
import tempfile
import sys
import tempfile
import unittest
from contextlib import contextmanager
from click.testing import CliRunner
from meta_ultra import api
import meta_ultra.cli as cli
from meta_ultra import config
from meta_ultra.config import DataType
from meta_ultra.database import RecordExistsError, InvalidRecordStateError
from shutil import rmtree

def changeToTempDir():
    tdir = tempfile.mkdtemp()
    os.chdir(tdir)
    return tdir

class Test_cli(unittest.TestCase):
    def setUp(self):
        self.tdir = changeToTempDir()
        
    def tearDown(self):
        rmtree(self.tdir)
        
    def test_cli_init(self):
        result = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        self.assertIn(config.mu_dir, os.listdir(self.tdir))

    # projects
    
    def test_cli_add_project(self):
        result0 = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result0.exit_code, msg=result0.output)
        result1 = CliRunner().invoke(cli.main, ['add', 'project', '-n', 'test_project'])
        self.assertEquals(0, result1.exit_code, msg=result1.output)
        self.assertEquals('test_project', api.getProject('test_project').name, msg=result1.output)
        
    def test_cli_view_project(self):
        result0 = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result0.exit_code, msg=result0.output)
        result1 = CliRunner().invoke(cli.main, ['add', 'project', '-n', 'test_project'])
        self.assertEquals(0, result1.exit_code, msg=result1.output)
        result2 = CliRunner().invoke(cli.main, ['view', 'projects', 'test_project'])
        self.assertEquals(0, result2.exit_code, msg=result2.output)
        self.assertIn('test_project', result2.output, msg=result2.output)

    def test_cli_remove_project(self):
        result0 = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result0.exit_code, msg=result0.output)
        result1 = CliRunner().invoke(cli.main, ['add', 'project', '-n', 'test_project'])
        self.assertEquals(0, result1.exit_code, msg=result1.output)
        result2 = CliRunner().invoke(cli.main, ['remove', 'projects', 'test_project', '--no-check'])
        self.assertEquals(0, result2.exit_code, msg=result2.output)
        result3 = CliRunner().invoke(cli.main, ['view', 'projects', 'test_project'])
        self.assertEquals(0, result3.exit_code, msg=result3.output)
        self.assertNotIn('test_project', result3.output, msg=result3.output)


    # samples
    
    def test_cli_add_sample(self):
        result0 = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result0.exit_code, msg=result0.output)
        result1 = CliRunner().invoke(cli.main, ['add', 'project', '-n', 'test_project'])
        self.assertEquals(0, result1.exit_code, msg=result1.output)
        result2 = CliRunner().invoke(cli.main, ['add', 'sample', '-n', 'test_sample', '-p', 'test_project'])
        self.assertEquals(0, result2.exit_code, msg=result2.output)
        self.assertEquals('test_sample', api.getSample('test_sample').name)


    def test_cli_view_sample(self):
        result0 = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result0.exit_code, msg=result0.output)
        result1 = CliRunner().invoke(cli.main, ['add', 'project', '-n', 'test_project'])
        self.assertEquals(0, result1.exit_code, msg=result1.output)
        result2 = CliRunner().invoke(cli.main, ['add', 'sample', '-n', 'test_sample', '-p', 'test_project'])
        self.assertEquals(0, result2.exit_code, msg=result2.output)
        result3 = CliRunner().invoke(cli.main, ['view', 'samples', 'test_sample'])
        self.assertEquals(0, result3.exit_code, msg=result3.output)
        self.assertIn('test_sample', result3.output)

        
    def test_cli_remove_sample(self):
        result0 = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result0.exit_code, msg=result0.output)
        result1 = CliRunner().invoke(cli.main, ['add', 'project', '-n', 'test_project'])
        self.assertEquals(0, result1.exit_code, msg=result1.output)
        result2 = CliRunner().invoke(cli.main, ['add', 'sample', '-n', 'test_sample', '-p', 'test_project'])
        self.assertEquals(0, result2.exit_code, msg=result2.output)
        result3 = CliRunner().invoke(cli.main, ['view', 'samples', 'test_sample'])
        self.assertEquals(0, result3.exit_code, msg=result3.output)
        result4 = CliRunner().invoke(cli.main, ['remove', 'samples','test_sample', '--no-check'])
        self.assertEquals(0, result4.exit_code, msg=result4.output)
        self.assertNotIn('test_sample', result4.output, msg=result4.output)

    # data records

    def test_cli_view_data_rec(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'test_proj', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        
        result = CliRunner().invoke(cli.main, ['view', 'data', 'test_SEDSD'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        self.assertIn('test_SEDSD', result.output)

    def test_cli_remove_data_rec(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'test_proj', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        self.assertEquals('test_SEDSD', api.getDataRec('test_SEDSD').name)
        result = CliRunner().invoke(cli.main, ['view', 'data', 'test_SEDSD'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        result = CliRunner().invoke(cli.main, ['remove', 'data',  'test_SEDSD', '--no-check'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        self.assertNotIn('test_SEDSD', result.output)

    # misc

    def test_cli_view_data_types(self):
        pass

    def test_cli_view_sample_types(self):
        pass
    
    

if __name__ == '__main__':
    unittest.main()


        # experiments
'''    
    def test_cli_add_experiment(self):
        result = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        result = CliRunner().invoke(cli.main, ['add', 'experiments', '-n', 'test_exp'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        self.assertEquals('test_exp', api.getExperiment('test_exp').name)


    def test_cli_view_experiment(self):
        result = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke(cli.main, ['add', 'experiment','-n',  'test_exp'])
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke(cli.main, ['view', 'experiments', 'test_exp'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        self.assertIn('test_exp', result.output, msg=result.output)
        self.assertEquals('test_exp', api.getExperiment('test_exp').name)

    def test_cli_remove_experiment(self):
        result = CliRunner().invoke(cli.main, ['init'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        result = CliRunner().invoke(cli.main, ['add', 'experiment', '-n', 'test_exp'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        result = CliRunner().invoke(cli.main, ['remove', 'experiment', '-n', 'test_exp'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        result = CliRunner().invoke(cli.main, ['view', 'experiments', 'test_exp'])
        self.assertEquals(0, result.exit_code, msg=result.output)
        self.assertNotIn('test_exp', result.output)
'''
