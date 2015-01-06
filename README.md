MonoX
=====

MonoX fitting etc

Produce templates from flat trees and additionally fit 
(di)muon control regions to correct V+Jet templates. Modify the config to suit your ntuples

  python buildModel.py categories_config_vtag.py

Run photon+Jet + dimuon combined control samples, calculates scale-factors on the fly
(Takes output from prefvious step as input)

  python runCombinedModel.py 

Make a bunch of plots from the output files to put into documentation
  
  ./runDraw.sh
