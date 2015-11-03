MonoX
=====
MonoX fitting etc

Produce templates from flat trees
         
  python buildModel.py categories_config


Build the model (input for likelihood) which links signal regions to control regions (for this step you must have the combine package from HiggsAnalysis/CombinedLimit (use slc6, i.e default, branch) from --> https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit

Edit the sections labelled "USER DEFINED" inside runModel You will need to create a config for each process to be constrained by some control region(s) and add them to the list "controlregions_def" See W_constraints.py and Z_constraints.py for examples

Run photon+Jet + dimuon combined control samples

  python runModel.py
