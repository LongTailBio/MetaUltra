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
from meta_ultra.data_type import DataType
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
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_project')
        api.saveConf('test_conf', {})
        api.saveResult('test_result', [], 'test_SEDSD', 'test_conf', 'test_sample', 'test_exp', 'test_project')
        api.removeProject('test_project')
        self.assertIs(None, api.getProject('test_project')) 
        self.assertIs(None, api.getSample('test_sample')) 
        self.assertEquals(None, api.getDataRec('test_SEDSD'))
        self.assertEquals(None, api.getResult('test_result'))

        
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
        api.init()
        api.saveConf('test_conf', {})

    def tests_double_add_conf_fails(self):
        api.init()
        api.saveConf('test_conf', {})
        self.assertRaises(RecordExistsError, api.saveConf, 'test_conf', {})


    def test_get_conf(self):
        api.init()
        api.saveConf('test_conf', {})
        self.assertEquals('test_conf', api.getConf('test_conf').name)

    def test_remove_conf(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_project')
        api.saveConf('test_conf', {})
        api.saveResult('test_result', [], 'test_SEDSD', 'test_conf', 'test_sample', 'test_exp', 'test_project')
        api.removeConf('test_conf')
        self.assertEquals(None, api.getConf('test_conf'))
        self.assertEquals(None, api.getResult('test_result'))

    
    def test_atomic_remove_conf(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_project')
        api.saveConf('test_conf', {})
        api.saveResult('test_result', [], 'test_SEDSD', 'test_conf', 'test_sample', 'test_exp', 'test_project')
        api.removeConf('test_conf', atomic=True)
        self.assertEquals(None, api.getConf('test_conf'))
        self.assertEquals('test_result', api.getResult('test_result').name)


    def test_query_confs_all(self):
        pass
        
    def test_query_confs_names(self):
        pass

    

    # experiments
    
    def test_add_experiment(self):
        api.init()
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveExperiment('test_exp_', DataType.WGS_DNA_SEQ_PAIRED_END, None)

    def test_double_add_experiment_fails(self):
        api.init()
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        self.assertRaises(RecordExistsError, api.saveExperiment, 'test_exp', DataType.WGS_DNA_SEQ_PAIRED_END, None)

    def test_get_experiment(self):
        api.init()
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        self.assertEquals('test_exp', api.getExperiment('test_exp').name)

    def test_remove_experiment(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_project')
        api.saveConf('test_conf', {})
        api.saveResult('test_result', [], 'test_SEDSD', 'test_conf', 'test_sample', 'test_exp', 'test_project')
        api.removeExperiment('test_exp')
        self.assertIs(None, api.getSample('test_exp')) 
        self.assertEquals(None, api.getDataRec('test_SEDSD'))
        self.assertEquals(None, api.getResult('test_result'))

        
    def test_atomic_remove_experiment(self):
        api.init()
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.removeExperiment('test_exp', atomic=True)
        self.assertIs(None, api.getExperiment('test_exp'))

    def test_query_exps_all(self):
        api.init()
        api.saveExperiment('test_exp_1', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveExperiment('test_exp_2', 'WGS_DNA_SEQ_SINGLE_END', None)
        expNames = [el.name for el in api.getExperiments()]
        self.assertIn('test_exp_1', expNames)
        self.assertIn('test_exp_2', expNames)

        
    def test_query_exps_names(self):
        api.init()
        api.saveExperiment('test_exp_1', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveExperiment('test_exp_2', 'WGS_DNA_SEQ_SINGLE_END', None)
        expNames = [el.name for el in api.getExperiments(names=['test_exp_2'])]
        self.assertNotIn('test_exp_1', expNames)
        self.assertIn('test_exp_2', expNames)



    def test_query_exps_data_types(self):
        api.init()
        api.saveExperiment('test_exp_1', 'WGS_DNA_SEQ_PAIRED_END', None)
        api.saveExperiment('test_exp_2', 'WGS_DNA_SEQ_SINGLE_END', None)
        expNames = [el.name for el in api.getExperiments(dataTypes=[DataType.WGS_DNA_SEQ_SINGLE_END])]
        self.assertNotIn('test_exp_1', expNames)
        self.assertIn('test_exp_2', expNames)


        

    # samples
    
    def test_add_sample(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)

    def test_add_sample_fails_without_project(self):
        api.init()
        self.assertRaises(InvalidRecordStateError, api.saveSample, 'test_sample', 'PHONE_SAMPLE', 'test_project', None)

    def test_double_add_sample_fails(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        self.assertRaises(RecordExistsError, api.saveSample, 'test_sample', 'PHONE_SAMPLE', 'test_project', None)

    def test_get_sample(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        self.assertEquals('test_sample', api.getSample('test_sample').name)
        
    def test_remove_project_creates_sample_error_state(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        api.removeProject('test_project', atomic=True)
        self.assertFalse(api.getSample('test_sample').validStatus())
        
    def test_remove_sample(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_project')
        api.saveConf('test_conf', {})
        api.saveResult('test_result', [], 'test_SEDSD', 'test_conf', 'test_sample', 'test_exp', 'test_project')
        api.removeSample('test_sample')
        self.assertIs(None, api.getSample('test_sample')) 
        self.assertEquals(None, api.getDataRec('test_SEDSD'))
        self.assertEquals(None, api.getResult('test_result'))

        
    def test_atomic_remove_sample(self, atomic=True):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_project', None)
        api.removeSample('test_sample', atomic=True)
        self.assertIs(None, api.getSample('test_sample')) 

    def test_query_samples_all(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample_1','PHONE_SAMPLE',  'test_project', None)
        api.saveSample('test_sample_2','PHONE_SAMPLE',  'test_project', None)
        sNames = [el.name for el in api.getSamples()]
        self.assertIn('test_sample_1', sNames)
        self.assertIn('test_sample_2', sNames)
        
        
    def test_query_samples_names(self):
        api.init()
        api.saveProject('test_project', None)
        api.saveSample('test_sample_1', 'PHONE_SAMPLE', 'test_project', None)
        api.saveSample('test_sample_2', 'PHONE_SAMPLE', 'test_project', None)
        sNames = [el.name for el in api.getSamples(names='test_sample_1')]
        self.assertIn('test_sample_1', sNames)
        self.assertNotIn('test_sample_2', sNames)


    def test_query_samples_sample_types(self):
        pass

    def test_query_samples_projects(self):
        api.init()
        api.saveProject('test_project_1', None)
        api.saveProject('test_project_2', None)
        api.saveSample('test_sample_1', 'PHONE_SAMPLE', 'test_project_1', None)
        api.saveSample('test_sample_2', 'PHONE_SAMPLE', 'test_project_2', None)
        sNames = [el.name for el in api.getSamples(projects=['test_project_1'])]
        self.assertIn('test_sample_1', sNames)
        self.assertNotIn('test_sample_2', sNames)

    # data records

    def test_add_SEDSD(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')

    def test_add_PEDSD(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_PAIRED_END', None)
        api.savePairedEndDNASeqData('test_PEDSD',
                                    'test_1.fastq.gz',
                                    'test_2.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
    

    def test_add_data_rec_fails_without_project(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.removeProject('test_proj', atomic=True)
        self.assertRaises(InvalidRecordStateError,
                          api.saveSingleEndDNASeqData,
                          'test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')


    def test_add_data_rec_fails_without_sample(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        self.assertRaises(InvalidRecordStateError,
                          api.saveSingleEndDNASeqData,
                          'test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')

    def test_add_data_rec_fails_without_exp(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        self.assertRaises(InvalidRecordStateError,
                          api.savePairedEndDNASeqData,
                          'test_PEDSD',
                                    'test_1.fastq.gz',
                                    'test_2.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')


        
    def test_double_add_data_rec_fails(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
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
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        self.assertEquals('test_SEDSD', api.getDataRec('test_SEDSD').name)

    def test_remove_project_creates_data_error_state(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.removeProject('test_proj', atomic=True)
        self.assertFalse(api.getDataRec('test_SEDSD').validStatus())


    def test_remove_sample_creates_data_error_state(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.removeSample('test_sample', atomic=True)
        self.assertRaises(InvalidRecordStateError, api.getDataRec, 'test_SEDSD')

        
    def test_remove_exp_creates_data_error_state(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.removeExperiment('test_exp', atomic=True)
        self.assertFalse(api.getDataRec('test_SEDSD').validStatus())


    def test_remove_data_rec(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.saveConf('test_conf', {})
        api.saveResult('test_result', [], 'test_SEDSD', 'test_conf', 'test_sample', 'test_exp', 'test_proj')
        api.removeData('test_SEDSD')
        self.assertEquals(None, api.getDataRec('test_SEDSD'))
        self.assertEquals(None, api.getResult('test_result'))

        
    def test_atomic_remove_data_rec(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.removeData('test_SEDSD', atomic=True)
        self.assertEquals(None, api.getDataRec('test_SEDSD'))

    def test_query_data_recs_all(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD_1',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.saveSingleEndDNASeqData('test_SEDSD_2',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        names = [el.name for el in api.getData()]
        self.assertIn('test_SEDSD_1', names)
        self.assertIn('test_SEDSD_2', names)

        
    def test_query_data_recs_names(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD_1',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.saveSingleEndDNASeqData('test_SEDSD_2',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        names = [el.name for el in api.getData(names=['test_SEDSD_1'])]
        self.assertIn('test_SEDSD_1', names)
        self.assertNotIn('test_SEDSD_2', names)


    def test_query_data_recs_data_types(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD_1',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp',
                                    'test_proj')
        api.saveExperiment('test_exp_2', 'WGS_DNA_SEQ_PAIRED_END', None)
        api.savePairedEndDNASeqData('test_PEDSD',
                                    'test_1.fastq.gz',
                                    'test_2.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp_2',
                                    'test_proj')
        names = [el.name for el in api.getData(dataTypes=[DataType.WGS_DNA_SEQ_SINGLE_END])]
        self.assertIn('test_SEDSD_1', names)
        self.assertNotIn('test_PEDSD', names)


    def test_query_data_recs_samples(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample_1', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveSample('test_sample_2', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD_1',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample_1',
                                    'test_exp',
                                    'test_proj')
        api.saveSingleEndDNASeqData('test_SEDSD_2',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample_2',
                                    'test_exp',
                                    'test_proj')
        names = [el.name for el in api.getData(samples=['test_sample_2'])]
        self.assertNotIn('test_SEDSD_1', names)
        self.assertIn('test_SEDSD_2', names)


    def test_query_data_recs_exps(self):
        api.init()
        api.saveProject('test_proj', None)
        api.saveSample('test_sample', 'PHONE_SAMPLE', 'test_proj', None)
        api.saveExperiment('test_exp_1', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveExperiment('test_exp_2', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD_1',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp_1',
                                    'test_proj')
        api.saveSingleEndDNASeqData('test_SEDSD_2',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample',
                                    'test_exp_2',
                                    'test_proj')
        names = [el.name for el in api.getData(experiments=['test_exp_1'])]
        self.assertIn('test_SEDSD_1', names)
        self.assertNotIn('test_SEDSD_2', names)


    def test_query_data_recs_projects(self):
        api.init()
        api.saveProject('test_proj_1', None)
        api.saveProject('test_proj_2', None)
        api.saveSample('test_sample_1', 'PHONE_SAMPLE', 'test_proj_1', None)
        api.saveSample('test_sample_2', 'PHONE_SAMPLE', 'test_proj_2', None)
        api.saveExperiment('test_exp', 'WGS_DNA_SEQ_SINGLE_END', None)
        api.saveSingleEndDNASeqData('test_SEDSD_1',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample_1',
                                    'test_exp',
                                    'test_proj_1')
        api.saveSingleEndDNASeqData('test_SEDSD_2',
                                    'test.fastq.gz',
                                    100,
                                    'test_sample_2',
                                    'test_exp',
                                    'test_proj_2')
        names = [el.name for el in api.getData(projects=['test_proj_1'])]
        self.assertIn('test_SEDSD_1', names)
        self.assertNotIn('test_SEDSD_2', names)


    # misc

    def test_get_data_types(self):
        pass

    def test_get_sample_types(self):
        pass
    
    

if __name__ == '__main__':
    unittest.main()
