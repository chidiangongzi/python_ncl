#
#  File:
#    TRANS_slice.py
#
#  Synopsis:
#    Illustrates how to create a slice plot
#
#  Categories:
#    contour plot
#
#  Author:
#    Karin Meier-Fleischer, based on NCL example
#  
#  Date of initial publication:
#    September 2018
#
#  Description:
#    This example shows how to create a slice plot.
#    xarray is used to read the NetCDF file, but PyNIO can also
#    be used. See the lines commented with ###.
#
#  Effects illustrated:
#    o  Read netCDF data
#    o  Drawing a slice plot
# 
#  Output:
#    A single visualization is produced.
#
#  Notes: The data for this example can be downloaded from 
#    http://www.ncl.ucar.edu/Document/Manuals/NCL_User_Guide/Data/
#   
'''
  Transition Guide PyNGL Example: TRANS_slice.py

  -  Read netCDF data
  -  Drawing a slice plot
  
  18-09-04  kmf
'''
import numpy as np
import Ngl
import xarray as xr
###import Nio
import os

#--  define variables
fname  = "rectilinear_grid_3D.nc"  #-- data file name

#--  open file and read variables
f    =  xr.open_dataset(fname)         #-- open data file
t    =  f.t[0,:,::-1,:]     #-- first time step, reverse latitude
lev  =  f.lev.values        #-- all levels
lat  =  f.lat[::-1]         #-- reverse latitudes
lon  =  f.lon.values        #-- all longitudes

###f    =  Nio.open_file(fname,"r")         #-- open data file
###t    =  f.variables["t"][0,:,::-1,:]     #-- first time step, reverse latitude
###lev  =  f.variables["lev"][:]            #-- all levels
###lat  =  f.variables["lat"][::-1]         #-- reverse latitudes
###lon  =  f.variables["lon"][:]            #-- all longitudes

nlat =  len(lat)                         #-- number of latitudes

longname = t.long_name
units    = f'deg{t.units}'
###longname = f.variables["t"].attributes['long_name']
###units    = f.variables["t"].attributes['units']

# Subselect the data around latitude 40 and 41.
t40 = t.sel(lat=slice(40,41)).squeeze()
print(t40.shape)    # 17 x 192

#-- open a workstation
wks =  Ngl.open_wks("png",os.path.basename(__file__).split('.')[0])

#-- set resources
res                 =  Ngl.Resources()   #-- generate an res object for plot
res.nglFrame        =  False

#-- viewport resources
res.vpXF            =  0.1               #-- start x-position of viewport
res.vpYF            =  0.9               #-- start y-position of viewport
res.vpWidthF        =  0.7               #-- width of viewport
res.vpHeightF       =  0.6               #-- height of viewport

#-- contour resources
res.cnFillOn        =  True              #-- turn on contour fill
res.cnFillPalette   = "temp_diff_18lev"
res.cnLineLabelsOn  =  False             #-- turn off line labels
res.cnInfoLabelOn   =  False             #-- turn off info label
res.cnLevelSelectionMode = "ManualLevels"#-- select manual levels
res.cnMinLevelValF  =  200.              #-- minimum contour value
res.cnMaxLevelValF  =  290.              #-- maximum contour value
res.cnLevelSpacingF =  5.                #-- contour increment

res.tiMainString    = 'slice at lat = {:4.2f}'.format(t40.lat.values)
res.tiYAxisString   =  f"{longname}  [hPa]"

#-- grid resources
res.sfXArray        =  lon               #-- scalar field x
res.sfYArray        =  lev/100               #-- scalar field y

#-- reverse y-axis
res.trYReverse      =  True              #-- reverse the Y axis
res.nglYAxisType    = "LogAxis"          #-- y axis log

#-- draw slice contour plot
plot = Ngl.contour(wks,t40,res)

#-- Retrieve some resources from map for adding labels
vpx  = Ngl.get_float(plot,'vpXF')
vpy  = Ngl.get_float(plot,'vpYF')
vpw  = Ngl.get_float(plot,'vpWidthF')
fnth = Ngl.get_float(plot,'tmXBLabelFontHeightF')

#-- write variable long_name and units to the plot
txres               = Ngl.Resources()
txres.txFontHeightF = fnth

txres.txJust  = "CenterLeft"
Ngl.text_ndc(wks,longname,vpx,vpy+0.02,txres)
txres.txJust  = "CenterRight"
Ngl.text_ndc(wks,units,   vpx+vpw,vpy+0.02,txres)

#-- advance the frame
Ngl.frame(wks)

#-- done
Ngl.end()
