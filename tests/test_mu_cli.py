#!/usr/bin/env python

import os
import tempfile
import sys
import tempfile
import unittest
from contextlib import contextmanager
from click.testing import CliRunner
from meta_ultra import api
from meta_ultra import config
from meta_ultra.config import DataType
from meta_ultra.database import RecordExistsError, InvalidRecordStateError
from shutil import rmtree

def changeToTempDir():
    tdir = tempfile.mkdtemp()
    os.chdir(tdir)
    return tdir

class Test_api(unittest.TestCase):
    def setUp(self):
        self.tdir = changeToTempDir()
        
    def tearDown(self):
        rmtree(self.tdir)
        
    def test_cli_init(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        self.assertIn(config.mu_dir, os.listdir(self.tdir))

    # projects
    
    def test_cli_add_project(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        self.assertEquals('test_project', api.getProject('test_project').name)
        
    def test_cli_view_project(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('view', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        self.assertIn('test_project', result.output)

    def test_cli_remove_project(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('remove', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('view', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        self.assertNotIn('test_project', result.output)


    # experiments
    
    def test_cli_add_experiment(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'experiment', 'test_exp')
        self.assertEquals(0, result.exit_code)
        self.assertEquals('test_exp', api.getExperiment('test_exp').name)


    def test_cli_view_experiment(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'experiment', 'test_exp')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('view', 'experiment', 'test_exp')
        self.assertEquals(0, result.exit_code)
        self.assertIn('test_exp', result.output)
        self.assertEquals('test_exp', api.getExperiment('test_exp').name)

    def test_cli_remove_experiment(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'experiment', 'test_exp')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('remove', 'experiment', 'test_exp')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('view', 'experiment', 'test_exp')
        self.assertEquals(0, result.exit_code)
        self.assertNotIn('test_exp', result.output)

    # samples
    
    def test_cli_add_sample(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'sample', 'test_sample')
        self.assertEquals(0, result.exit_code)
        self.assertEquals('test_sample', api.getSample('test_sample').name)


    def test_cli_view_sample(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'sample', 'test_sample')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('view', 'sample', 'test_sample')
        self.assertEquals(0, result.exit_code)
        self.assertIn('test_sample', result.output)

        
    def test_cli_remove_sample(self):
        result = CliRunner().invoke('init')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'project', 'test_project')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('add', 'sample', 'test_sample')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('view', 'sample', 'test_sample')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('remove', 'sample', 'test_sample')
        self.assertEquals(0, result.exit_code)
        self.assertNotIn('test_sample', result.output)

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
        result = CliRunner().invoke('view', 'data', 'test_SEDSD')
        self.assertEquals(0, result.exit_code)
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
        result = CliRunner().invoke('view', 'data', 'test_SEDSD')
        self.assertEquals(0, result.exit_code)
        result = CliRunner().invoke('rmove', 'data', 'test_SEDSD')
        self.assertEquals(0, result.exit_code)
        self.assertNotIn('test_SEDSD', result.output)

    # misc

    def test_cli_view_data_types(self):
        pass

    def test_cli_view_sample_types(self):
        pass
    
    

if __name__ == '__main__':
    unittest.main()
