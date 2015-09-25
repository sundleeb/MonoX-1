MonoX
=====

MonoX fitting etc

Produce templates from flat trees and additionally fit 
(di)muon control regions to correct V+Jet templates. Modify the config to suit your ntuples, read the config 
provided for a description of how to produce one

  1) python buildModel.py categories_config  

Build the model (input for likelihood) which links signal regions to control regions (for this step you must have
the combine package from HiggsAnalysis/CombinedLimit (use slc6, i.e default, branch) from --> https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit
Edit the sections of USER DEFINED inside runModel, you will need to create a config for each process to be constrained by some control region(s) 
read W_constraints.py and Z_constraints.py for example

  2) python runModel.py 
  3) make datacards and run combine to fit/calculate limits etc
