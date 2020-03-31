#$ file tarball /uscms_data/d3/kdlin/internet2/run_scale/CMSSW_10_6_6_resnet50-v2.tar.gz
#$ njobs 50

import qondor
import datetime
import os

delay_min = 5
allowed_lateness_min = 5
timezone_offset_hour = 5

NEVENTS= 501
#ADDRESS="35.192.95.176"
ADDRESS="ailab01.fnal.gov"

preprocessing = qondor.preprocessing(__file__)
cmssw = qondor.CMSSW.from_tarball(preprocessing.files['tarball'])
cmssw.run_commands([
    #'xrdcp root://cmseos.fnal.gov//store/kdlin/deepcalo_all.bin $CMSSW_BASE/src/SonicCMS/Core/data/',
#    'mv $CMSSW_BASE/../deepcalo_5000.bin $CMSSW_BASE/src/SonicCMS/Core/data/deepcalo_all.bin',
#    'mv $CMSSW_BASE/../skim1000.root $CMSSW_BASE/src/SonicCMS/Core/data/skim.root',
    'xrdcp root://cmseos.fnal.gov//store/user/pedrok/sonic/store_mc_RunIISpring18MiniAOD_BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph_MINIAODSIM_100X_upgrade2018_realistic_v10-v1_30000_24A0230C-B530-E811-ADE3-14187741120B.root $CMSSW_BASE/src/SonicCMS/TensorRT/python/',
    'cd $CMSSW_BASE/src/',
    'source /cvmfs/cms.cern.ch/cmsset_default.sh',
    'export SCRAM_ARCH=slc7_amd64_gcc700',
    'scramv1 b ProjectRename',
    'eval `scramv1 runtime -sh`',
    'scram b ExternalLinks'
    #'cd $CMSSW_BASE/src/SonicCMS/TensorRT/python',
    #'cmsRun OnLine_HLT_GRun_dummy.py'
    ])

submission_time = datetime.datetime.strptime(
    os.environ['CLUSTER_SUBMISSION_TIMESTAMP'],
    '%Y%m%d_%H%M%S'
    )

run_time = submission_time + datetime.timedelta(minutes=delay_min) + datetime.timedelta(hours=timezone_offset_hour)

qondor.utils.sleep_until(run_time, allowed_lateness_min*60, True)
cmssw.run_commands([
    'cd $CMSSW_BASE/src/SonicCMS/TensorRT/python',
    'cmsRun jetImageTest_mc_cfg.py maxEvents=%d batchsize=10 address=%s mode=PseudoAsync' % (NEVENTS, ADDRESS),
    ])
