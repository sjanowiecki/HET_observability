#calculating dark, dark+bright, and all availability per trimester
#  started 10 Aug 2018, SPJ
#   sep 1 2018, split off to plot PI targets on pre-computed graphs
#   re-named "HET_obs" to simplify
import numpy as np

#####----change this if needed----#####
#
#trimester year and number
c_y = 2020
c_t = 3
#
#####----------------------------#####
#NOTE: works for [2019,2020]-[1,2,3] right now
#    HETDEX data included for these trimesters only







#include weather/PR/eng time losses? should be True
include_losses = True

#include allocations to HETDEX fields? recommended.
include_HETDEX = True

#targets file with headers: ID, RA, Dec, exptime, Nvisits (etc ok):
targf = 'PI_targets.dat' #change if needed

setup_time = 300 #assume 300 seconds. 



#  exec(open("./HET_obs.py").read())



#time lost assumptions: 0.056(PR), 0.?(ENG), 0.3(WEATHER,monthly)
#    PR fraction is calculated AFTER accounting for weathered out nights
f_weather_lost = np.array([
        0.359,0.337,0.379,0.335,0.335,0.339,0.499,0.428,0.476,0.314,0.246,0.346 ])
#       Jan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec
f_pr_lost = 0.056
#engr time is only during bright, and is 10%:
f_eng_lost_BRIGHT = 0.10

allm=np.arange(1,13,1)

#merge weather+PR, monthly array
f_time_good = ( (1.0-f_weather_lost) * (1.0-f_pr_lost) )




#set alias/wrap-around point based on trimester
if (c_t==1):
    #hwrap = +18.0 #NOT USED
    offs= 20#-8 #limit offsets
elif (c_t==2):
    ##hwrap = +8.0 #i.e., values below 8 get +24. lims shift by hwrap
    offs=+2#+8 #limit offsets
elif (c_t==3):
    ##hwrap = 12.0 #NOT USED
    offs=+12 #0 #limits/save_LST offsets
else:
    print("issue with trimester")
    asplodez





import numpy as np
import matplotlib.pyplot as plt
import math

import astropy
from astropy.io import ascii
from astropy import units as u


from matplotlib import pyplot as plt

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

plt.register_cmap(name='viridis', cmap=plt.cm.viridis)

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=True)






def dolab1(fig):#:,thisplot):
        #18, far over!
        thisplot = fig.add_axes([0.808,0.05,0.05,0.05],visible=True)
        thisplot.spines['bottom'].set_color('white')
        thisplot.spines['top'].set_color('white')
        thisplot.spines['left'].set_color('white')
        thisplot.spines['right'].set_color('white')
        thisplot.xaxis.set_visible(False)
        thisplot.yaxis.set_visible(False)
        thisplot.set_zorder(500)
        thisplot.fill('white')
        thisplot.text(-0.045,-0.015,'18',fontsize=17)
        #12, near middle!
        thisplot = fig.add_axes([0.623,0.05,0.05,0.05],visible=True)
        thisplot.spines['bottom'].set_color('white')
        thisplot.spines['top'].set_color('white')
        thisplot.spines['left'].set_color('white')
        thisplot.spines['right'].set_color('white')
        thisplot.xaxis.set_visible(False)
        thisplot.yaxis.set_visible(False)
        thisplot.set_zorder(500)
        thisplot.fill('white')
        thisplot.text(-0.045,-0.015,'12',fontsize=17)
        #6, at left
        thisplot = fig.add_axes([0.442,0.05,0.05,0.05],visible=True)
        thisplot.spines['bottom'].set_color('white')
        thisplot.spines['top'].set_color('white')
        thisplot.spines['left'].set_color('white')
        thisplot.spines['right'].set_color('white')
        thisplot.xaxis.set_visible(False)
        thisplot.yaxis.set_visible(False)
        thisplot.set_zorder(500)
        thisplot.fill('white')
        thisplot.text(-0.045,-0.015,'6',fontsize=17)
        return fig#,thisplot

def dolab2(fig):
        a=0
        if (False):
            thisplot = fig.add_axes([0.80,0.05,0.05,0.05],visible=True)
            thisplot.spines['bottom'].set_color('white')
            thisplot.spines['top'].set_color('white')
            thisplot.spines['left'].set_color('white')
            thisplot.spines['right'].set_color('white')
            thisplot.xaxis.set_visible(False)
            thisplot.yaxis.set_visible(False)
            thisplot.set_zorder(500)
            #thisplot.fill('grey')
            thisplot.set_alpha(0.5)
            thisplot.text(-0.02,0.0,'6',fontsize=17)
        return fig#thisplot

def dolab3(fig):
        thisplot = fig.add_axes([0.680,0.045,0.05,0.05],visible=True)
        thisplot.spines['bottom'].set_color('white')
        thisplot.spines['top'].set_color('white')
        thisplot.spines['left'].set_color('white')
        thisplot.spines['right'].set_color('white')
        thisplot.xaxis.set_visible(False)
        thisplot.yaxis.set_visible(False)
        thisplot.set_zorder(500)
        #thisplot.fill('grey')
        thisplot.set_alpha(0.5)
        thisplot.text(-0.02,0.0,'6',fontsize=15)

        thisplot2 = fig.add_axes([0.860,0.045,0.05,0.05],visible=True)
        thisplot2.spines['bottom'].set_color('white')
        thisplot2.spines['top'].set_color('white')
        thisplot2.spines['left'].set_color('white')
        thisplot2.spines['right'].set_color('white')
        thisplot2.xaxis.set_visible(False)
        thisplot2.yaxis.set_visible(False)
        thisplot2.set_zorder(500)
        #thisplot2.fill('grey')
        thisplot2.set_alpha(0.5)
        thisplot2.text(-0.02,0.0,'12',fontsize=15)
        return fig#,thisplot




#def map_targets(targf,savedat):  #actually, no function now
#first, unpack saved data:
#read file, based on c_t and c_y
fin = 'data/allvisits_byLST_wHETDEX_'+str(c_y)+'-'+str(c_t)+'.dat'
fdat = ascii.read(fin)


save_LST = fdat['LST'].data
save_visits_all = fdat['all'].data
save_visits_br = fdat['br'].data
save_visits_grey = fdat['gray'].data #new name change
save_visits_dark = fdat['dark'].data
save_visits_HETDEX = fdat['visits_HETDEX'].data

#SUBTRACT HETDEX from dark and ALL
#   only subtract as much from the "all" time as there is "dark" time.
how_much_to_lose = np.array([hd if (hd<dt) else dt if (hd>dt) else 0 for hd,dt in zip(save_visits_HETDEX,save_visits_dark)])
if (include_HETDEX):
    save_visits_all -= how_much_to_lose
    save_visits_dark -= how_much_to_lose

#calculate LST step size from data
dall = save_LST[1:] -save_LST[0:-1] 
step_size = np.mean(dall)

#print('target time')
#read in target ra/dec, exptime, nvis, moon
targs = ascii.read(targf)
#print(targs)
    
#parse. IDs first, assume
targ_id = targs.columns[0].data
targ_ra = targs.columns[1].data
targ_dec = targs.columns[2].data
targ_exptime = targs.columns[3].data
targ_nvis = targs.columns[4].data
#targ_moon = targs.columns[5].data
#print parsed data
#print('these are the ID,ra,dec,exptime,nvis I found in '+targf+':')
#for i,r,d,e,n in zip(targ_id,targ_ra,targ_dec,targ_exptime,targ_nvis):
#        print i,r,d,e,n
#        print(' ')
    

#read in HET observability data file
hetf = 'data/HET_opt_tracking.txt'
het = ascii.read(hetf)
#print(het)
h_dec = het.columns[0].data
h_tott = het.columns[1].data
h_optaz = het.columns[2].data
h_ha1 = het.columns[3].data
h_ha2 = het.columns[4].data

#add ha3/ha4 for tracks of appropriate dec:
#  dec boundaries of double-valued?
#    -4.318553207530732 < dec < 65.6814360000000
d2min = -4.318553207530732 
d2max = 65.6814360000000
h_ha3 = np.array([-h if ((d>d2min)&(d<d2max)) else -99 for h,d in zip(h_ha2,h_dec)])
h_ha4 = np.array([-h if ((d>d2min)&(d<d2max)) else -99 for h,d in zip(h_ha1,h_dec)])
    
#determine LSTs of available tracks for these targets
# and prepare arrays for saving
LST1_start = targ_ra*0.0-99.
LST1_stop  = targ_ra*0.0-99.
LST2_start = targ_ra*0.0-99.
LST2_stop  = targ_ra*0.0-99.
for i,r,d,e,n in zip(targ_id,targ_ra,targ_dec,targ_exptime,targ_nvis):
        #print('target: '+str(i))
        #ok, so for this ra,dec (and exptime/nvis), find time per visit
        epv = e/n
        #also, get RA in decimal hours
        ra_h = r/15.
        
        #consider only a single visit, since will be identical
        #assumed setup time is: setup_time (in seconds)
        # so, total time for a single visit is:
        tott = (epv+setup_time)*u.s
        
        
        
        #for this dec, find the optimal start/stop times in LST
        # so, find closest h_dec and get the HA values (1,2,3,4)
        dd = np.abs(h_dec - d)
        ha1 = h_ha1[dd==dd.min()][0]
        ha2 = h_ha2[dd==dd.min()][0]
        ha3 = h_ha3[dd==dd.min()][0]
        ha4 = h_ha4[dd==dd.min()][0]
        #print(ha1,ha2,ha3,ha4)
        #verify that ha1/ha2 are valid: i.e. the first (usu west) track)
        if ((np.abs(ha1)<5)&(np.abs(ha2)<5)):
            #good!  these are always set up so ha1 is before ha2?
            hami = np.min([ha1,ha2])
            hama = np.max([ha1,ha2])
            #find midpoint of track:
            hamid = hami + (hama-hami)/2.
            #print(ha1,ha2,hamid)
            
            #VERIFY! is there enough time for this requested exptime within each visit?
            ha_total = hama-hami #in hours
            req_h = tott/(3600*u.s)
            if (req_h > ha_total):
                print(' ')
                print('target: '+str(i))
                print(ha1,ha2,ha3,ha4)
                print("{:.2f}h  first track available. you requested: {:.2f}h per ({:.0f}) visit".format(ha_total, req_h.value,n))
                #how many visits would it need?
                fix_nv = np.int(1.+(e/3600.)/ha_total)
                print('   that is a PROBLEM -- need more visits. for now you get '+str(fix_nv)+' visits instead')
                #print('epv before '+str(epv))
                epv = e/fix_nv
                #print('epv after '+str(epv))
                n=fix_nv
                tott = (epv+setup_time)*u.s
            
            #use total time to extend on either side of this, optimal.
            ha_start = hamid*u.h - tott/2.
            ha_stop = hamid*u.h + tott/2.
            #print(ha_start,ha_stop,tott)
            
            
            #combine with target RA to get LST start/stop
            LST1_start[targ_id==i] = ra_h + ha_start/u.h
            LST1_stop[targ_id==i] = ra_h + ha_stop/u.h

        #verify that ha3/ha4 are valid: i.e. the second (usu east) track)
        if ((np.abs(ha3)<5)&(np.abs(ha4)<5)):
            #good!  set up min/max
            hami = np.min([ha3,ha4])
            hama = np.max([ha3,ha4])
            #find midpoint of track:
            hamid = hami + (hama-hami)/2.
            #print(ha3,ha4,hamid)
            
            #VERIFY! is there enough time for this requested exptime within each visit?
            ha_total = hama-hami #in hours
            req_h = tott/(3600*u.s)
            if (req_h > ha_total):  #should never happen here!
                print("{:.2f}h second track available. you requested: {:.2f}h per visit".format(ha_total,req_h))
                print("error. still not enough visits....")
                asplode

            #use total time to extend on either side of this, optimal.
            ha_start = hamid*u.h - tott/2.
            ha_stop = hamid*u.h + tott/2.
            #print(ha_start,ha_stop,tott)
            
            
            #combine with target RA to get LST start/stop
            LST2_start[targ_id==i] = ra_h + ha_start/u.h
            LST2_stop[targ_id==i] = ra_h + ha_stop/u.h
        else:
            print("   also, no second track")
        #done:
        #print(' ')

#done:
print(' ')
print(' ')
    
    
#fix up rounding issues/etc. depends on trimester.
#print('checking')
if (c_t==1):
        #for trimester 1, 
        tmp = np.array([-99 if (l==-99) else l if (l>22) else l+24.0 for l in LST1_start])
        LST1_start = tmp
        tmp = np.array([-99 if (l==-99) else l if (l>22) else l+24.0 for l in LST1_stop])
        LST1_stop = tmp
        tmp = np.array([-99 if (l==-99) else l if (l>22) else l+24.0 for l in LST2_start])
        LST2_start = tmp
        tmp = np.array([-99 if (l==-99) else l if (l>22) else l+24.0 for l in LST2_stop])
        LST2_stop = tmp
if (c_t==2):
        #for trimester 2, we keep 0-24  ####OLD: allow up to 32h, and take negatives +24
        tmp = np.array([-99 if (l==-99) else l if ((l>=2)&(l<=25)) else l-24.0 if (l>25) else l+24.0 for l in LST1_start])
        LST1_start = tmp
        tmp = np.array([-99 if (l==-99) else l if ((l>=2)&(l<=25)) else l-24.0 if (l>25) else l+24.0 for l in LST1_stop])
        LST1_stop = tmp
        tmp = np.array([-99 if (l==-99) else l if ((l>=2)&(l<=25)) else l-24.0 if (l>25) else l+24.0 for l in LST2_start])
        LST2_start = tmp
        tmp = np.array([-99 if (l==-99) else l if ((l>=2)&(l<=25)) else l-24.0 if (l>25) else l+24.0 for l in LST2_stop])
        LST2_stop = tmp
if (c_t==3):
        #for trimester 3, less than 12, send up to >24    #to 36 now
        tmp = np.array([-99 if (l==-99) else l if ((l>12)&(l<36)) else l+24.0 if (l<12) else l-24.0 for l in LST1_start])
        LST1_start = tmp
        tmp = np.array([-99 if (l==-99) else l if ((l>12)&(l<36)) else l+24.0 if (l<12) else l-24.0 for l in LST1_stop])
        LST1_stop = tmp
        tmp = np.array([-99 if (l==-99) else l if ((l>12)&(l<36)) else l+24.0 if (l<12) else l-24.0 for l in LST2_start])
        LST2_start = tmp
        tmp = np.array([-99 if (l==-99) else l if ((l>12)&(l<36)) else l+24.0 if (l<12) else l-24.0 for l in LST2_stop])
        LST2_stop = tmp
    
    
#make new plots with all visits, HETDEX visits, and these targets
#  HETDEX - dark/grey color at bottom
#  N/S tracks: darker primary colors (populate by N visits!!)
#  E/W tracks: lighter (matched) colors
#     all using LST1[2]_start[stop] and targ_id and targ_nvis
    
    
    
fig = plt.figure(figsize=(13,6))
a = fig.add_subplot(111)
    
plt.subplots_adjust(wspace=0.25, hspace=0)

minorLocator1 = MultipleLocator(1) #x ticks/etc
majorLocator1 = MultipleLocator(6)
minorLocator2 = MultipleLocator(5) #y ticks/etc
majorLocator2 = MultipleLocator(25)
a.xaxis.set_minor_locator(minorLocator1)
a.xaxis.set_major_locator(majorLocator1)
a.yaxis.set_minor_locator(minorLocator2)
a.yaxis.set_major_locator(majorLocator2)


a.tick_params(axis='both', which='major', labelsize=16)

    
a.set_xlim(-0.5+offs,24.5+offs)
a.set_ylim(0,75)

a.plot(save_LST, save_visits_all,color='black',lw=3)
a.plot(save_LST, save_visits_dark,color='black',lw=1)
a.plot(save_LST, save_visits_grey+save_visits_dark,color='grey',lw=2)

a.set_xlabel(r'LST [h]', fontname='Arial', fontsize=22, fontweight='normal')
a.set_ylabel(r'N visits (including weather/etc)', fontname='Arial', fontsize=22, fontweight='normal')
    
#fix manually in two cases:
if (c_t==1): dolab1(fig)
if (c_t==2): dolab2(fig) #none needed
if (c_t==3): dolab3(fig)

if (include_HETDEX):
        a.text(15.5+offs,64,'subtracting HETDEX allocations',fontsize=15)
else:
        a.text(15.5+offs,64,'not including HETDEX fields',fontsize=15)


#add ranges of target tracks:
# first, make save arrays for single visits and 1of2 visits:  use saveLST
t_sv = save_LST*0 #single visits
t_Ev = save_LST*0 #visits with two tracks: East
t_Wv = save_LST*0 #visits with two tracks: West (first ones?)
for t1,t2,t3,t4,i,nv,texp in zip(LST1_start, LST1_stop, LST2_start, LST2_stop, targ_id, targ_nvis,targ_exptime):
        #if valid, add first trajectory for as many visits as needed
        #print (t1,t2,t3,t4)
        if ((t1>-30)&(t2>-30)&(t3>-30)&(t4>-30)):
                #two tracks! are they both definitely in darkness w/ appropriate moon?
                # for now, ALWAYS include, even if impossible....
                # add first track to appropriate vector
                t_Ev[(save_LST>t1)&(save_LST<t2)] += nv #this many visits
                # add second track to appropriate vector
                t_Wv[(save_LST>t3)&(save_LST<t4)] += nv #this many visits
                #print("  two tracks good")
        elif ((t1>-30)&(t2>-30)):
                #only 1 is good. it is #1:
                #add to singles
                t_sv[(save_LST>t1)&(save_LST<t2)] += nv #this many visits
                #print("  track 1 good")
        elif ((t3>-30)&(t4>-30)):
                t_sv[(save_LST>t3)&(save_LST<t4)] += nv #this many visits
                #print("  track 2 good")

#combine these to make shaded regions
t_tot = t_sv+t_Ev+t_Wv
#show these as further lines:
a.fill(save_LST, t_sv,color='blue',lw=0,alpha=0.8)
a.fill(save_LST, t_Ev,color='red',lw=0,alpha=0.3)
a.fill(save_LST, t_Wv,color='green',lw=0,alpha=0.3)
#print(save_LST,t_tot)

a.text(9+offs,71,str(c_y)+'-'+str(c_t), color='black', fontname='Arial', fontsize=23, fontweight='bold')


#labels:
a.text(0+offs,64.5,'Single tracks (N/S)',color='blue', fontname='Arial', fontsize=19, fontweight='bold',alpha=0.8)
a.text(0+offs,60.5,'West tracks',color='red', fontname='Arial', fontsize=19, fontweight='normal',alpha=0.4)
a.text(0+offs,56.5,'East tracks',color='green', fontname='Arial', fontsize=19, fontweight='normal',alpha=0.4)
#note names are off.... but ok.

a.text(0.7+offs,47.5,'All (bright+grey+dark)',fontsize=15)
a.text(0.7+offs,44.0,'Grey',fontsize=15)
a.text(0.7+offs,40.5,'Dark',fontsize=15)

a.plot([0+offs,0.5+offs],[48.5,48.5],color='black',lw=3)
a.plot([0+offs,0.5+offs],[45.0,45.0],color='grey',lw=2)
a.plot([0+offs,0.5+offs],[41.5,41.5],color='black',lw=1)

#horizontal lines
llines = np.array([10,20,30,40,50,60,70])
for l in llines:
        a.plot([-1+offs,25+offs],[l,l],color='grey',lw=1,ls=':',alpha=0.8)

        

graout = 'LST_visits_PI_'+str(c_y)+'-'+str(c_t)+'.pdf'
fig.savefig(graout, bbox_inches='tight')
    









