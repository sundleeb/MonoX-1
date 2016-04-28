# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
from itertools import product

#out_file_name = '../eos/cms/store/user/zdemirag/signal_scan/templates_March9/MonoJ_806_1_catmonojet.root'

out_file_name = 'mcfm805_templates_monojet.root'

bins = [200., 230., 260.0, 290.0, 320.0, 350.0, 390.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0]

samples = {}

mmed = [10,20,30,40,50,60,70,80,90,100,125,150,175,200,300,325,400,525,600,725,800,925,1000,1125,1200,1325,1400,1525,1600,1725,1800,1925,2000,2500,3000,3500,4000,5000]
mdm  = [1,5,10,25,50,100,150,200,300,400,500,600,700,800,900,1000,1250,1500,1750,2000]

#signalexpsV = [ ["V_%d_%d_1_signal"%(i,j) , ['signal','signal_800%04d%04d'%(i,j),1,1] ] for i,j in product(mmed,mdm) ] 
#signalexpsA = [ ["MonoZ_A_%d_%d_1_signal"%(i,j) , ['signal','signal_801%04d%04d'%(i,j),1,1] ] for i,j in product(mmed,mdm) ] 
signalexpsS = [ ["S_%d_%d_1_signal"%(i,j) , ['signal','signal_805%04d%04d'%(i,j),1,1] ] for i,j in product(mmed,mdm) ] 
#signalexpsP = [ ["P_%d_%d_1_signal"%(i,j) , ['signal','signal_806%04d%04d'%(i,j),1,1] ] for i,j in product(mmed,mdm) ] 

#for ss in signalexpsV: samples[ss[0]] = ss[1]
#for ss in signalexpsA: samples[ss[0]] = ss[1]
#for ss in signalexpsP: samples[ss[0]] = ss[1]
for ss in signalexpsS: samples[ss[0]] = ss[1]

monojet_category = {
        'name':"monojet"
        #,'in_file_name':"../eos/cms/store/user/zdemirag/signal_scan/slim/MonoJ_1_806.root"
        #,'in_file_name':"/afs/cern.ch/work/z/zdemirag/work/Limits13TeV/CMSSW_7_1_5/src/final806.root"
        ,'in_file_name':"/afs/cern.ch/work/z/zdemirag/work/Limits13TeV/CMSSW_7_1_5/src/MonoJ_805_mcfm.root"
        ,"cutstring":"pfMetPt>200 && pfMetPt < 10000 && id==1"
        ,"varstring":["pfMetPt",200,1250]
        ,"weightname":"weight"
        ,"bins":bins[:]
        ,"additionalvars":[['pfMetPt',25,200,1250]]
        ,"pdfmodel":0
        ,"samples": samples
}
categories = [monojet_category]
