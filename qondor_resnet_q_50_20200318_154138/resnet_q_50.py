#$ file tarball /uscms/home/nsuaysom/nobackup/kelvin/CMSSW_10_6_6_cha.tar.gz
#$ njobs 50
#$ delay 1 m
#$ allowed_lateness 100 m

import qondor
preprocessing = qondor.preprocessing(__file__)
cmssw = qondor.CMSSW.from_tarball(preprocessing.files['tarball'])
cmssw.run_commands([
	'cd $CMSSW_BASE/src/',
	'source /cvmfs/cms.cern.ch/cmsset_default.sh',
	'export SCRAM_ARCH=slc7_amd64_gcc700',
	'scramv1 b ProjectRename',
	'eval `scramv1 runtime -sh`',
	'scram b ExternalLinks',
    	'cd SonicCMS/TensorRT/python/',
	'cmsRun jetImageTest_mc_cfg.py maxEvents=50 batchsize=10 address=ailab01.fnal.gov'
    ])
