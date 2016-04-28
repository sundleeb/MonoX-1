# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
from itertools import product
#out_file_name = '../eos/cms/store/user/zdemirag/signal_scan/templates_March9/MonoJ_806_1_catmonov.root'
out_file_name = 'mcfm805_templates_monov.root'

#bins = [250,300,350,400,500,600,1000]
bins = [250,300,350,400,500,600,750,1000]

samples = {}

mdm  = [1,5,10,25,50,125,100,150,200,300,400,500,600,700,800,900,1000,1250,1500,1750,2000]
mmed = [10,20,30,40,50,60,70,80,90,100,125,150,175,200,300,325,400,525,600,725,800,925,1000,1125,1200,1325,1400,1525,1600,1725,1800,1925,2000,2500,3000,3500,4000,5000]

#signalexpsA = [ ["MonoZ_A_%d_%d_1_signal"%(i,j) , ['signal','signal_801%04d%04d'%(i,j),1,1] ] for i,j in product(mmed,mdm) ] 
#signalexpsP = [ ["P_%d_%d_1_signal"%(i,j) , ['signal','signal_806%04d%04d'%(i,j),1,1] ] for i,j in product(mmed,mdm) ] 
#signalexpsV = [ ["V_%d_%d_1_signal"%(i,j) , ['signal','signal_800%04d%04d'%(i,j),1,1] ] for i,j in product(mmed,mdm) ] 
signalexpsS = [ ["S_%d_%d_1_signal"%(i,j) , ['signal','signal_805%04d%04d'%(i,j),1,1] ] for i,j in product(mmed,mdm) ] 

#for ss in signalexpsA: samples[ss[0]] = ss[1]
#for ss in signalexpsP: samples[ss[0]] = ss[1]
#for ss in signalexpsV: samples[ss[0]] = ss[1]
for ss in signalexpsS: samples[ss[0]] = ss[1]

monov_category = {
        'name':"monov"
        #,'in_file_name':"../eos/cms/store/user/zdemirag/signal_scan/slim/MonoJ_1_806.root"
        #,'in_file_name':"/afs/cern.ch/work/z/zdemirag/work/Limits13TeV/CMSSW_7_1_5/src/final806.root"
        ,'in_file_name':"/afs/cern.ch/work/z/zdemirag/work/Limits13TeV/CMSSW_7_1_5/src/MonoJ_805_mcfm.root"
        ,"cutstring":"pfMetPt>250 && pfMetPt < 10000 && id==2"
        ,"varstring":["pfMetPt",250,1000]
        ,"weightname":"weight"
        ,"bins":bins[:]
        ,"additionalvars":[['pfMetPt',25,250,1000]]
        ,"pdfmodel":0
        ,"samples": samples
}
categories = [monov_category]
