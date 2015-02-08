import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d","--tdir",default='',help="pick histos from a different directory (will be catgeory of course!)")
parser.add_option("-c","--cat",default='',help="pick up a category name for $CAT")
parser.add_option("-v","--var",default='',help="pick up a variable name for $VAR")
parser.add_option("-o","--outext",default='',help="Add Extension to output name")
parser.add_option("-x","--xlab",default='',help="Set the Label for X-axis")
parser.add_option("-b","--batch",default=False,action='store_true',help="always run in batch and save .pdf with config name instead of drawing canvas")
parser.add_option("-g","--gendata",default=False,action='store_true',help="Generate Pretend data from the background")
parser.add_option("-p","--pull",default=False,action='store_true',help="replace the ratio plot with a pull (data-background)/(sigma_{data+bkg})")
parser.add_option("","--nolog",default=False,action='store_true',help="Turn of log plot")
parser.add_option("","--nospec",default=False,action='store_true',help="Don't make a spectrum plot")
(options,args) = parser.parse_args()

import ROOT as r 
r.gStyle.SetOptStat(0)

r.gROOT.ProcessLine(".L statsCalc.h+");
from ROOT import calculateExpectedSignificance 
from ROOT import calculateExpectedLimit 

fi = r.TFile.Open(args[0])
di = fi #.Get("mjw_1jet")

def getNormalizedHist(hist, templatehist):
  nb = hist.GetNbinsX()
  thret = templatehist.Clone()
  for b in range(1,nb+1): 
    sfactor = 1./templatehist.GetBinWidth(b)
    if options.nospec: sfactor = 1
    thret.SetBinContent(b,hist.GetBinContent(b)*sfactor)
    thret.SetBinError(b,hist.GetBinError(b)*sfactor)
  thret.GetYaxis().SetTitle("Events/GeV")
  if options.nospec: 
        thret.GetYaxis().SetTitle("Events")
  return thret

sys.path.append("configs")
configs = args[1:]
canvs = []
if len(configs) > 1:
  print "Moving to batch mode, will save pdfs as name of config"
  options.batch = True

if options.batch:
  r.gROOT.SetBatch(1)

for ic,config in enumerate(configs) :
 print "Run Config", config
 x = __import__(config)
 if options.tdir: x.directory = options.tdir

 # first run through signals, backgrounds and data to check if we need to replace things
 for s in x.signals.keys():
  #x.signals[s][0] = x.signals[s][0].replace("$CAT",options.cat)
  #x.signals[s][0] = x.signals[s][0].replace("$VAR",options.var)
  #x.signals[s][0] = x.signals[s][0].replace("$DIRECTORY",options.tdir)
  # replace the Key
  snew  =  s.replace("$CAT",options.cat)
  snew  =  snew.replace("$VAR",options.var)
  snew  =  snew.replace("$DIRECTORY",options.tdir)

  x.signals[snew] =  x.signals[s]; 
  x.signals.pop(s)

 for b in x.backgrounds.keys():
  for i in range(len(x.backgrounds[b][0])):
   x.backgrounds[b][0][i]=x.backgrounds[b][0][i].replace("$CAT",options.cat)
   x.backgrounds[b][0][i]=x.backgrounds[b][0][i].replace("$VAR",options.var)
   x.backgrounds[b][0][i]=x.backgrounds[b][0][i].replace("$DIRECTORY",options.tdir)
 x.dataname = x.dataname.replace("$CAT",options.cat)
 x.dataname = x.dataname.replace("$VAR",options.var)
 x.dataname = x.dataname.replace("$DIRECTORY",options.tdir)

 print x.signals

 if x.directory!="":x.directory+="/"
 if ":" in x.dataname: 
   fi,datnam = x.dataname.split(":")
   tfi = r.TFile.Open(fi)
   dataO = tfi.Get(datnam)
 else:
   dataO = di.Get(x.directory+x.dataname)
   print x.directory+x.dataname
 data 	    = getNormalizedHist(dataO,dataO)
 data.SetTitle("")
 origlabel = data.GetXaxis().GetTitle()
 #if options.xlab: data.GetXaxis().SetTitle(options.xlab)
 data.GetXaxis().SetTitle("")
 data.GetXaxis().SetLabelSize(0)
 data.GetYaxis().SetTickLength(0.03)

 can = r.TCanvas("c_%d"%ic,"c_%d"%ic,800,800)
 leg = r.TLegend(0.7,0.48,0.89,0.89); leg.SetFillColor(0); leg.SetTextFont(42)
 leg.AddEntry(data,"Data","PEL")
 legentries = []
 lat = r.TLatex(); lat.SetNDC()
 lat.SetTextFont(42)
 lat.SetTextSize(0.03)
 if options.xlab: label = options.xlab
 else: label = origlabel
 # make 2 pads
 pad1 = r.TPad("p1","p1",0,0.28,1,1)
 pad1.SetBottomMargin(0.01)
 pad1.SetCanvas(can)
 pad1.Draw()
 pad1.cd()
 data.Draw()

 thstack = r.THStack("bkg","backgroundstack")
 thstack.SetTitle("")
 totalbkg = 0; totalc=0
 print "	Nevents ", data.GetName(), data.Integral("width")

 totalbackground = 0
 for bkgtype_i,bkg in enumerate(x.key_order):
  nullhist = 0; nullc = 0

  for thist in x.backgrounds[bkg][0]:
    if ":" in thist:
     fi,datnam = thist.split(":")
     tfi = r.TFile.Open(fi)
     tmp = tfi.Get(datnam)
     print "trying...",datnam
    elif "Purity=" in thist:
       val = float(thist.split("=")[-1])
       tmp = dataO.Clone()
       tmp.Scale(1-val)
    else: 
       tmp = di.Get(x.directory+thist)
       print "trying...",x.directory+thist, "from",di.GetName()
    if nullc == 0 : 	
        print "Starting ", tmp.GetName(), tmp.Integral("")
    	nullhist = tmp.Clone()
    else:
        #print "  ... Adding ", tmp.GetName(), tmp.Integral("")
    	nullhist.Add(tmp)
    nullc+=1
  if bkgtype_i==0 :
  	totalbackground = nullhist.Clone()
	totalbackground.Sumw2();
  else : totalbackground.Add(nullhist)

  nullhist = getNormalizedHist(nullhist,data)
  print "	Nevents ", bkg, nullhist.Integral("width")
  nullhist.SetLineColor(1)
  nullhist.SetLineWidth(2)
  nullhist.SetFillColor(x.backgrounds[bkg][1])
  nullhist.SetFillStyle(1001)
  if totalc==0: totalbkg=nullhist.Clone()
  else : totalbkg.Add(nullhist)
  totalbkg.Sumw2()
  x.backgrounds[bkg][2]=nullhist.Clone()
  thstack.Add(x.backgrounds[bkg][2])
  legentries.append([x.backgrounds[bkg][2],bkg,"F"])
  totalc+=1
 
 legentries.reverse()
 for le in legentries: leg.AddEntry(le[0],le[1],le[2])
 thstack.Draw("histFsame")
 totalsignal = 0
 for sig_i,sig in enumerate(x.signals.keys()):
  if ":" in sig:
     fi,datnam = sig.split(":")
     tfi = r.TFile.Open(fi)
     print "Getting signal %s"%tfi.GetName()+datname
     tmp = tfi.Get(datnam)
  else: 
    print "Getting signal %s"%x.directory+"/"+sig
    tmp = di.Get(x.directory+"/"+sig)
  if sig_i==0: totalsignal = tmp.Clone()
  else: totalsignal.Add(tmp)
  tmp = getNormalizedHist(tmp,data)
  tmp.SetLineColor(x.signals[sig][1])
  tmp.SetLineWidth(3)
  x.signals[sig][2]=tmp.Clone()
  x.signals[sig][2].Draw("samehist")
  leg.AddEntry(x.signals[sig][2],x.signals[sig][0],"L")
  print "	Nevents ", tmp.GetName(), tmp.Integral("width")

 normtotalback = getNormalizedHist(totalbackground,data)
 print "Total Background " , normtotalback.Integral("width")
 # now set totalbackground errors to 0 
 for b in range(normtotalback.GetNbinsX()):
   totalbkg.SetBinError(b+1,0)

 if options.gendata: 
 	for b in range(1, totalbkg.GetNbinsX()+1):
		data.SetBinContent(b,normtotalback.GetBinContent(b))
		data.SetBinError(b,((normtotalback.GetBinContent(b))**0.5)/data.GetBinWidth(b))

 normtotalback.SetFillStyle(3005);
 normtotalback.SetFillColor(1);
 normtotalback.SetMarkerSize(0);
 #normtotalback.Draw("E2same");

 data.SetMinimum(0.002)
 data.SetMarkerColor(r.kBlack)
 data.SetLineColor(1)
 data.SetLineWidth(1)
 data.SetMarkerSize(0.9)
 data.SetMarkerStyle(20)
 data.Draw("same")
 leg.Draw()
 if not options.nolog: pad1.SetLogy()
 pad1.RedrawAxis()
 lat.DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}") 
 if options.cat : lat.DrawLatex(0.76,0.92,options.cat) 

 can.cd()
 pad2 = r.TPad("p2","p2",0,0.068,1,0.28)
 pad2.SetTopMargin(0.02)
 pad2.SetCanvas(can)
 pad2.Draw()
 pad2.cd()

 ratio = data.Clone()
 ratioErr = normtotalback.Clone()
 ratioErr.SetFillStyle(1001);
 ratioErr.SetFillColor(r.kGray);

 if not options.pull:
  ratio.GetYaxis().SetRangeUser(0.21,1.79)
  ratio.Divide(totalbkg)
  ratio.GetYaxis().SetTitle("Data/Bkg")
  ratioErr.Divide(totalbkg)

 else: 
  ratio.GetYaxis().SetRangeUser(-5,5)
  ratio.GetYaxis().SetTitle("(Data-Bkg)/#sigma")
  ratio.GetYaxis().SetTitleOffset(1.2)
  for b in range(1,ratio.GetNbinsX()+1):
    val = ratio.GetBinContent(b)-totalbackground.GetBinContent(b)
    err = ((ratio.GetBinError(b))**2 + (totalbackground.GetBinError(b))**2)**0.5
    ratio.SetBinContent(b,val/err) 
    ratio.SetBinError(b,1) 

 r.gStyle.SetOptStat(0)
 ratio.GetYaxis().SetNdivisions(5)
 ratio.GetYaxis().SetLabelSize(0.1)
 ratio.GetYaxis().SetTitleSize(0.12)
 ratio.GetXaxis().SetTitleSize(0.085)
 ratio.GetXaxis().SetLabelSize(0.12)

 # draw the sub-plot 
 #if options.xlab: ratio.GetXaxis().SetTitle(options.xlab)
 ratio.GetXaxis().SetTitle("")
 ratio.Draw()
 if not options.pull : ratioErr.Draw("sameE2")
 ratio.Draw("same")

 if options.pull: line = r.TLine(data.GetXaxis().GetXmin(),0,data.GetXaxis().GetXmax(),0)
 else  :line = r.TLine(data.GetXaxis().GetXmin(),1,data.GetXaxis().GetXmax(),1)
 line.SetLineColor(2)
 line.SetLineWidth(3)
 line.Draw()
 ratio.Draw("same")
 pad2.RedrawAxis()
 # add Label
 can.cd()
 lat.DrawLatex(0.68,0.02,label)
 #lat.DrawLatex(0.5,0.5,"#bold{CMS} #emph{Preliminary}") 
 canvs.append(can)
#can.SaveAs("metdist.pdf")
 can.Draw()
 if totalsignal != 0 : print "	Expected Significance ", calculateExpectedSignificance(totalsignal,totalbackground), " sigma"
 if totalsignal != 0 : print "	Expected Limit mu  <  ", calculateExpectedLimit(0.01,0.5,totalsignal,totalbackground)
# if totalsignal.Integral()>0 : print "	Expected Significance (incbkg) ", calculateExpectedSignificance(totalsignal,totalbackground,1), " sigma"
 if options.batch: can.SaveAs("%s_%s%s.pdf"%(config,options.tdir,options.outext))
 if options.batch: can.SaveAs("%s_%s%s.png"%(config,options.tdir,options.outext))
if not options.batch:raw_input("Press enter")
