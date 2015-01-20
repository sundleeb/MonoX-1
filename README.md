MonoX
=====

MonoX fitting etc

configs/categories_config.py defines the analysis (make your own for different categories, models etc)
(assume here-on your config is called configs/config.py)

Scale tree weights with muon/photon scale factors

  python addEff.py config

Run recoil corrections to correct MET distribution in trees (produces new tree Tree -> TreeMet

  python addEff.py config
   
Produce templates from flat trees and additionally fit 
(di)muon control regions to correct V+Jet templates. Modify the config to suit your ntuples

  python buildModel.py config

Run photon+Jet + dimuon combined control samples, calculates scale-factors on the fly
(Takes output from prefvious step as input)

  python runCombinedModel.py 

Make a bunch of plots from the output files to put into documentation
  
  ./runDraw.sh

Write a PAS, win!
