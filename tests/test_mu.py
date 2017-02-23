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
from meta_ultra.database import RecordExistsError
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
        
    def test_init(self):
        api.init()
        assert config.mu_dir in os.listdir(self.tdir)

    # projects
    
    def test_add_project(self):
        api.init()
        api.saveProject('test_project', None)

    def tests_double_add_project_fails(self):
        api.init()
        api.saveProject('test_project_', None)
        self.assertRaises(RecordExistsError, api.saveProject, 'test_project_', None)

    def test_get_project(self):
        api.init()
        api.saveProject('test_project', None)
        self.assertEquals('test_project', api.getProject('test_project').name)

    def test_remove_project(self):
        pass
        
    def test_atomic_remove_project(self):
        api.init()
        api.saveProject('test_project', None)
        api.removeProject('test_project', atomic=True)
        self.assertIs(None, api.getProject('test_project'))

    def test_query_projects_all(self):
        pass
        
    def test_query_projects_names(self):
        pass

    # confs
    
    def test_add_conf(self):
        pass

    def tests_double_add_conf_fails(self):
        pass

    def test_get_conf(self):
        pass

    def test_remove_conf(self):
        pass
    
    def test_atomic_remove_conf(self):
        pass

    def test_query_confs_all(self):
        pass
        
    def test_query_confs_names(self):
        pass

    

    # experiments
    
    def test_add_experiment(self):
        api.init()
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        api.saveExperiment('test_exp_', DataType.DNA_SEQ_PAIRED_END)

    def test_double_add_experiment_fails(self):
        api.init()
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        self.assertRaises(RecordExistsError, api.saveExperiment, 'test_exp', DataType.DNA_SEQ_PAIRED_END)

    def test_get_experiment(self):
        api.init()
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        self.assertEquals('test_exp', api.getExperiment('test_exp').name)

    def test_remove_experiment(self):
        pass
        
    def test_atomic_remove_experiment(self):
        api.init()
        api.saveExperiment('test_exp', None)
        api.removeExperiment('test_exp', atomic=True)
        self.assertIs(None, api.getExperiment('test_exp'))

    def test_query_exps_all(self):
        pass
        
    def test_query_exps_names(self):
        pass

    def test_query_exps_data_types(self):
        pass

        

    # samples
    
    def test_add_sample(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)

    def test_add_sample_fails_without_project(self):
        api.init()
        api.saveSample('test_sample', 'test_project', None)

    def test_double_add_sample_fails(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        self.assertRaises(RecordExistsError, api.saveSample, 'test_sample', 'test_project', None)

    def test_get_sample(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        self.assertEquals('test_sample', api.getSample('test_sample').name)

    def test_remove_project_creates_sample_error_state(self):
        pass
        
    def test_remove_sample(self):
        pass
        
    def test_atomic_remove_sample(self, atomic=True):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        api.removeSample('test_sample', atomic=True)
        self.assertIs(None, api.getSample('test_sample')) 

    def test_query_samples_all(self):
        pass
        
    def test_query_samples_names(self):
        pass

    def test_query_samples_sample_types(self):
        pass

    def test_query_samples_projects(self):
        pass

    

        
    # data records

    def test_add_SEDSD(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')

    def test_add_PEDSD(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_PAIRED_END')
        api.savePairedEndDNASeqData('test_PEDSD',
                                    'test_1.fastq.gz',
                                    'test_2.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
    

    def test_add_data_rec_fails_without_project(self):
        api.init()
        api.saveSample('test_sample', 'test_project', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')


    def test_add_data_rec_fails_without_sample(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')

    def test_add_data_rec_fails_without_exp(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        api.savePairedEndDNASeqData('test_PEDSD',
                                    'test_1.fastq.gz',
                                    'test_2.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')


        
    def test_double_add_data_rec_fails(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')

        self.assertRaises( RecordExistsError,
                           api.saveSingleEndDNASeqData,
                           'test_SEDSD',
                           'test.fastq.gz',
                           100,
                           'test_sample',
                           'test_exp',
                           'test_proj')


    def test_get_data_rec(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        self.assertEquals('test_SEDSD', api.getDataRec('test_SEDSD').name)

    def test_remove_project_creates_data_error_state(self):
        pass

    def test_remove_sample_creates_data_error_state(self):
        pass

    def test_remove_exp_creates_data_error_state(self):
        pass

    def test_remove_data_rec(self):
        pass
        
    def test_atomic_remove_data_rec(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'test_project', None)
        api.saveExperiment('test_exp', 'DNA_SEQ_SINGLE_END')
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.removeData('test_SEDSD', atomic=True)
        self.assertEquals(None, api.getDataRec('test_SEDSD'))

    def test_query_data_recs_all(self):
        pass
        
    def test_query_data_recs_names(self):
        pass

    def test_query_data_recs_data_types(self):
        pass

    def test_query_data_recs_samples(self):
        pass

    def test_query_data_recs_exps(self):
        pass

    def test_query_data_recs_projects(self):
        pass

    # misc

    def test_get_data_types(self):
        pass

    def test_get_sample_types(self):
        pass
    
    

if __name__ == '__main__':
    unittest.main()
