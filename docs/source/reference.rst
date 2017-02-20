**********************
Database API Reference
**********************

MetaUltra provides a python API to track samples, metadata, computed-results, and datafiles.


Information Retrieval
=====================

.. py:function:: getProjects()

.. py:function:: getExperiments()

.. py:function:: getExperiments()

.. py:function:: getSamples(projects=None)

   Get a list of samples. If project name is not specified
   all samples are returned, otherwise only samples in the
   given projects are returned

   :rtype: list
   :param projectNames: The name of the projects samples
                        should be from
   :type projectName: str or None
   :return: A ``list`` of samples from the specified
            projects.

.. py:function:: getData(dataType=None,samples=None, experiments=None, projects=None)

   Get a list of every data object passing the filter.

   :rtype: list
   :param dataType: 
   :param samples: A list of sample objects or sample names,
                   the difference is automatically detected
   :param experiments: A list of experiments or experiment
                       names, the difference is automatically
                       detected
   :return: A ``list`` of data objects.

.. py:function:: getSingleEndedSeqData(samples=None, experiments=None, projects=None)

   Alias for ``getData``

.. py:function:: getPairedEndedSeqData(samples=None, experiments=None, project=None)

   Alias for ``getData``
            

Information Storage
===================

.. py:function:: saveProject(name, metadata)

  :rtype: Project
  :param name:
  :param metadata: A jsonable object
  
.. py:function:: saveSample(name, project, metadata)

  :rtype: Sample
  :param name:
  :param projectName:
  :param metadata: A jsonable object


.. py:function:: saveSingleEndedSeqData(name, readFilename, aveReadLen, sample, experiment, project)

  :rtype: SingleEndedSeqData

.. py:function:: savePairedEndedSeqData(name, read1Filename, read2Filename, aveReadLen, sample, experiment, project, aveGapLen=None)

  :rtype: PairedEndedSeqData


.. py:function:: saveSingleEndedSeqRun(name, machineType)

  :rtype: SingleEndedSeqRun

.. py:function:: savePairedEndedSeqRun(name, machineType)

  :rtype: PairedEndedSeqRun

.. py:function:: saveResult(name, resultFilenames, data, conf, sample, project)

  :rtype: Result
  :param resultFilenames: A ``list`` of the filenames being registered


          
  
