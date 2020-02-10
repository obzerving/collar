##################################################################################################################
#                                                                                                                #
# Collar Calculator                                                                                              #
# Version 1.0                                                                                                    #
#                                                                                                                #
# This program generates an SVG file consisting of                                                               #
#   - A paper model of one of the n sides with tabs to assemble into a full 3D model                             #
#   - Top and bottom lids for the generated model                                                                #
#   - A wrapper to cover the generated model                                                                     #
#                                                                                                                #
# Copyright: (c) 2020, Joseph Zakar <observing@gmail.com>                                                        #
# GNU General Public License v3.0+ (see LICENSE or                                                               #
# https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)#fulltext)                                  #
#                                                                                                                #
##################################################################################################################

import sys
import os
import uuid
from xml.dom.minidom import parse
import xml.dom.minidom
from svgpathtools import *
import math
import tkinter
from tkinter import *
import tkinter.filedialog
import tkinter.font as font
from tkinter import messagebox
from copy import deepcopy

# user defined defaults
outputfile = ''
dashlength = 0.15
plgn1a = 5.0
plgn2a = 3.0
n = 6
tabht = .25
shght = 2.0

# program defined defaults
tabangle = 25
vlen = 0.0
orientTop = 0
orientBottom = 1
orientRight = 2
orientLeft = 3

class Node:
   def __init__(self):
      self.x = 0.0
      self.y = 0.0
      self.rotval = 0.0
   
def main(argv):
   # globals for makeTab
   global orientTop
   global orientBottom
   global orientRight
   global orientLeft
   global tab_height
   global tab_angle
   # globals for this program
   global outputfile
   global n
   global dashlength
   global plgn1a
   global plgn2a
   global tabht
   global shght
   global tabangle
   global vlen
   tab_height = tabht
   tab_angle = tabangle
   numnodes = 8
   dscores = [] # temporary list of all score lines
   opaths = []  # all the generated paths will be stored in this list to write an SVG file
   oattributes = [] # each path in opaths has a corresponding set of attributes in this list
   # attributes for body, top, and bottom
   battributes = {'style' : 'fill:#32c864;stroke:#000000;stroke-width:0.96;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dashoffset:0;stroke-opacity:1'}
   # attributes for wrapper
   wattributes = {'style' : 'fill:#6432c8;stroke:#000000;stroke-width:0.96;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dashoffset:0;stroke-opacity:1'}
   # attributes for scorelines
   sattributes = {'style' : 'fill:none;stroke:#000000;stroke-width:0.96;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dashoffset:0;stroke-opacity:1'}

   top = tkinter.Tk()
   top.title("Collar Calculator")
   pane = PanedWindow(top, orient=VERTICAL)
   pane.pack(fill=BOTH, expand=1)
   F2 = Frame(pane)
   L2 = tkinter.Label(F2, text="Output File Name")
   L2.pack( side = tkinter.LEFT)
   E2 = tkinter.Entry(F2, bd =5, width=30)
   E2.pack(side = tkinter.LEFT)
   F3 = Frame(pane)
   L3 = tkinter.Label(F3, text="Number of Polygon Sides")
   L3.pack( side = tkinter.LEFT)
   E3 = tkinter.Entry(F3, bd =5, width=5)
   E3.insert(0,str(n))
   E3.pack(side = tkinter.LEFT)
   F4 = Frame(pane)
   L4 = tkinter.Label(F4, text="Length of Dashline in inches (zero for solid line)")
   L4.pack( side = tkinter.LEFT)
   E4 = tkinter.Entry(F4, bd =5, width=6)
   E4.insert(0,str(dashlength))
   E4.pack(side = tkinter.LEFT)
   F4a = Frame(pane)
   L4a = tkinter.Label(F4a, text="Height of Tab in inches")
   L4a.pack( side = tkinter.LEFT)
   E4a = tkinter.Entry(F4a, bd =5, width=6)
   E4a.insert(0,str(tabht))
   E4a.pack(side = tkinter.LEFT)
   F5a = Frame(pane)
   L5a = tkinter.Label(F5a, text="Size of Smaller Polygon in inches)")
   L5a.pack( side = tkinter.LEFT)
   E5a = tkinter.Entry(F5a, bd =5, width=5)
   E5a.insert(0,str(plgn2a))
   E5a.pack(side = tkinter.LEFT)
   F5b = Frame(pane)
   L5b = tkinter.Label(F5b, text="Size of Larger Polygon in inches)")
   L5b.pack( side = tkinter.LEFT)
   E5b = tkinter.Entry(F5b, bd =5, width=5)
   E5b.insert(0,str(plgn1a))
   E5b.pack(side = tkinter.LEFT)
   F7 = Frame(pane)
   L7 = tkinter.Label(F7, text="Height of Collar in inches)")
   L7.pack( side = tkinter.LEFT)
   E7 = tkinter.Entry(F7, bd =5, width=5)
   E7.insert(0,str(shght))
   E7.pack(side = tkinter.LEFT)
   def OutfileCallBack():
      ftypes = [('svg files','.svg'), ('All files','*')]
      outputfile = tkinter.filedialog.asksaveasfilename(title = "Save File As", filetypes = ftypes, defaultextension='.svg')
      E2.insert(0,outputfile)
   def CancelCallBack():
      top.destroy()
   def OKCallBack():
      global outputfile
      global n
      global dashlength
      global plgn1a
      global plgn2a
      global tabht
      global shght
      outputfile = E2.get()
      n = int(E3.get())
      dashlength = float(E4.get())
      tabht = float(E4a.get())
      plgn1a = float(E5b.get())
      plgn2a = float(E5a.get())
      shght = float(E7.get())
      top.destroy()
   B2 = tkinter.Button(F2, text="Browse", command=OutfileCallBack)
   B2.pack(side = tkinter.LEFT)
   F6 = Frame(pane)
   bfont = font.Font(size=12)
   B3 = tkinter.Button(F6, text="Cancel", command=CancelCallBack)
   B3['font'] = bfont
   B3.pack(side = tkinter.LEFT, ipadx=30)
   B4 = tkinter.Button(F6, text="OK", command=OKCallBack)
   B4['font'] = bfont
   B4.pack(side = tkinter.RIGHT,ipadx=40)
   pane.add(F2)
   pane.add(F3)
   pane.add(F4)
   pane.add(F4a)
   pane.add(F5a)
   pane.add(F5b)
   pane.add(F7)
   pane.add(F6)
   top.mainloop()
   if outputfile == '':
      root = tkinter.Tk()
      root.withdraw()
      messagebox.showerror("Collar Input Error", "Output File is Required")
      sys.exit(5)
   # Determine largest (plgn1) and smallest (plgn2) polygon
   plgn1 = max(plgn1a, plgn2a)
   plgn2 = min(plgn1a, plgn2a)
   wrapscale = 1.005 # wrapper is scaled up 0.5% to better cover the model
   done = 0
   # We go through this loop twice
   # First time for the model, scorelines, and the lids
   # Second time for the wrapper
   while done < 2:
      w1 = (plgn1)*(math.sin(math.pi/n))
      w2 = (plgn2)*(math.sin(math.pi/n))
      tabadd = tabht / math.tan(math.radians(90-tabangle))
      if plgn1 == max(plgn1a, plgn2a):
         pieces = []
         nodes = []
         nd = []
         for i in range(8):
            nd.append(Node())
      else:
         i = 0
         while i < n:
            j = 0
            while j < 8:
               del pieces[i][0]
               j = j + 1
            i = i + 1
         i = 0
         while len(pieces) > 0:
            del pieces[0]
            i = i + 1
         i = 0
         while i < 8:
            del nodes[0]
            i = i + 1
      for pn in range(n):
         nodes.clear()
         #what we need here is to skip the rotatation and just move the x and y if there is no difference between the polygon sizes.
         #Added by Sue to handle equal polygons
         if plgn1a == plgn2a:
            nda1 = (0.5*w1)-tabadd
            if nda1 <= 0:
               tabangle2 = math.degrees(math.atan(2*tabht/w1)) - 0.01
               tabadd2 = tabht*math.tan(math.radians(tabangle2))
               nda1 = (0.5*w1) - tabadd2
            nd[0].x =  pn * w1
            nd[0].y = shght
            nd[1].x = nd[0].x + tabadd
            nd[1].y = nd[0].y + tabht
            nd[2].x = nd[0].x + w1 - tabadd
            nd[2].y = nd[1].y  
            nd[3].x = nd[0].x + w1  
            nd[3].y = nd[0].y
            nd[4].x = nd[3].x
            nd[4].y = nd[0].y - shght   
            nd[5].x =nd[2].x 
            nd[5].y = nd[4].y - tabht  
            nd[6].x =nd[1].x 
            nd[6].y = nd[5].y 
            nd[7].x = nd[0].x  
            nd[7].y = nd[4].y 
         else:
            if pn == 0:
               nd[7].x = -w2/2
               nd[7].y = (plgn2a/2)*math.cos(math.pi/n)
               nd[0].x = -w1/2
               nd[0].y = (plgn1a/2)*math.cos(math.pi/n)
               vlen = math.sqrt(shght**2 + (nd[0].y-nd[7].y)**2)
               nd[0].y = nd[0].y + (vlen-(nd[0].y-nd[7].y))
               nd[4].x = w2/2
               nd[4].y = nd[7].y
               nd[3].x = w1/2
               nd[3].y = nd[0].y
               nd[1].x = nd[0].x + tabadd
               nd[1].y = nd[0].y + tabht
               nd[2].x = nd[3].x - tabadd
               nd[2].y = nd[3].y + tabht
               nd[6].x = nd[7].x + tabadd
               nd[6].y = nd[7].y - tabht
               nd[5].x = nd[4].x - tabadd
               nd[5].y = nd[4].y - tabht
               ox,oy = findIntersection(nd[0].x,nd[0].y,nd[7].x,nd[7].y,nd[3].x,nd[3].y,nd[4].x,nd[4].y)
               origin = complex(ox,oy)
               Q2 = math.degrees(math.atan((nd[0].y - origin.imag)/(w1/2 - origin.real)))
               Q1 = 90 - Q2
            else:
               d1 = 'M'
               for j in range(8):
                  d1 = d1 + ' ' + str(nd[j].x) + ',' + str(nd[j].y)
               d1 = d1 + ' z'
               p1 = parse_path(d1)
               p2 = p1.rotated(-2*Q1, origin)
               for j in range(8):
                  nd[j].x = p2[j][0].real
                  nd[j].y = p2[j][0].imag
         for i in range(8):
            nodes.append(deepcopy(nd[i]))
         pieces.append(deepcopy(nodes))
      if done == 0:
         dprop = 'M'
         for pn in range(n):
            if(pn == 0):
               dprop = dprop+' '+str(pieces[pn][0].x)+','+str(pieces[pn][0].y)
            dprop = dprop+' '+str(pieces[pn][1].x)+','+str(pieces[pn][1].y)
            dprop = dprop+' '+str(pieces[pn][2].x)+','+str(pieces[pn][2].y)
            dprop = dprop+' '+str(pieces[pn][3].x)+','+str(pieces[pn][3].y)
         # Placing the tab on the last piece
         if pn == n-1:
            cpt1 = complex(pieces[pn][3].x, pieces[pn][3].y)
            cpt2 = complex(pieces[pn][4].x, pieces[pn][4].y)
            # tab oriented on the right when N3.x > N0.x and N3.y > N4.y
            if (pieces[pn][3].x > pieces[pn][0].x) and (pieces[pn][3].y > pieces[pn][4].y):
               tabpt1, tabpt2 = makeTab(cpt1, cpt2, orientRight)
            # tab oriented on the top when N3.y == N4.y and N3.x <= N0.x
            elif (pieces[pn][3].x <= pieces[pn][0].x) and (pieces[pn][3].y == pieces[pn][4].y):
               tabpt1, tabpt2 = makeTab(cpt1, cpt2, orientTop)
            # tab oriented on the left when N3.x <= N0.x and N3.y < N4.y
            elif (pieces[pn][3].x <= pieces[pn][0].x) and (pieces[pn][3].y < pieces[pn][4].y):
               tabpt1, tabpt2 = makeTab(cpt1, cpt2, orientLeft)
            # tab oriented on the bottom when N3.y == N4.y and N3.x <= N0.x
            elif (pieces[pn][3].x <= pieces[pn][0].x) and (pieces[pn][3].y == pieces[pn][4].y):
               tabpt1, tabpt2 = makeTab(cpt1, cpt2, orientRight)
            else:
               print('Unable to determine tab orientation! Right hand tab selected.')
               tabpt1, tabpt2 = makeTab(cpt1, cpt2, orientRight)
         dprop = dprop+' '+str(tabpt1.real)+','+str(tabpt1.imag)
         dprop = dprop+' '+str(tabpt2.real)+','+str(tabpt2.imag)
         for pn in range(n-1, -1, -1):
            if(pn == (n-1)):
               dprop = dprop+' '+str(pieces[pn][4].x)+','+str(pieces[pn][4].y)
            dprop = dprop+' '+str(pieces[pn][5].x)+','+str(pieces[pn][5].y)
            dprop = dprop+' '+str(pieces[pn][6].x)+','+str(pieces[pn][6].y)
            dprop = dprop+' '+str(pieces[pn][7].x)+','+str(pieces[pn][7].y)
         dprop = dprop+' '+str(pieces[0][0].x)+','+str(pieces[0][0].y)
         outpath = parse_path(dprop)
         opaths.append(outpath)
         oattributes.append(battributes)
         for pn in range(n):
            spaths = makescore(pieces[pn][0], pieces[pn][3],dashlength)
            dscores.append(spaths)
            spaths = makescore(pieces[pn][3], pieces[pn][4],dashlength)
            dscores.append(spaths)

         for pn in range(n-1, -1, -1):
            spaths = makescore(pieces[pn][4], pieces[pn][7],dashlength)
            dscores.append(spaths)

         # lump together all the score lines into one path
         slist = ''
         for dndx in dscores:
            slist = slist + dndx
         opaths.append(parse_path(slist))
         oattributes.append(sattributes)
         ## At this point, we can generate the top and bottom polygons
         ## r = sidelength/(2*sin(PI/numpoly))
         opaths.append(makepoly(w1, n))
         oattributes.append(battributes)
         opaths.append(makepoly(w2, n))
         oattributes.append(battributes)
         plgn1 = plgn1*wrapscale
         plgn2 = plgn2*wrapscale
         done = 1
      else:
         dwrap = 'M'
         for pn in range(n):
            if(pn == 0):
               dwrap = dwrap+' '+str(pieces[pn][0].x)+','+str(pieces[pn][0].y)
            dwrap = dwrap+' '+str(pieces[pn][3].x)+','+str(pieces[pn][3].y)
         for pn in range(n-1, -1, -1):
            if(pn == (n-1)):
               dwrap = dwrap+' '+str(pieces[pn][4].x)+','+str(pieces[pn][4].y)
            dwrap = dwrap+' '+str(pieces[pn][7].x)+','+str(pieces[pn][7].y)
         dwrap = dwrap+' '+str(pieces[0][0].x)+','+str(pieces[0][0].y)
         outpath = parse_path(dwrap)
         opaths.append(outpath)
         oattributes.append(wattributes)
         done = 2
   totalpaths = Path()
   for tps in opaths:
      totalpaths.append(tps)
   xmin,xmax,ymin,ymax=totalpaths.bbox()
   tmpfile = str(uuid.uuid4())
   wsvg(opaths, filename=tmpfile, attributes=oattributes)
   # Post processing stage
   # Due to issues with svgpathtools, some post processing of the file output from the library is necessary until issues have been resolved
   # The following attributes are suitable for input to inkscape and/or the Cricut Design Space
   # Document properties are 11.5 x 11.5 inches. The viewBox sets the scale at 72 dpi. Change the display units in Inkscape to inches.
   docscale = 72
   isvg_attributes = {'xmlns:dc': 'http://purl.org/dc/elements/1.1/', 'xmlns:cc': 'http://creativecommons.org/ns#', 'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'xmlns:svg': 'http://www.w3.org/2000/svg', 'xmlns': 'http://www.w3.org/2000/svg', 'id': 'svg8', 'version': '1.1', 'viewBox': '0 0 828.0 828.0', 'height': '11.5in', 'width': '11.5in'}
   # Assumes order of paths is body, scorelines, big polygon, small polygon, wrapper
   ids = ['body','scorelines','bigpoly','smallpoly','wrapper']
   # Read the xml tree from the file
   DOMTree = xml.dom.minidom.parse(tmpfile)
   # Accessing the svg node (which must be the root element)
   svg =DOMTree.documentElement
   # correct the height, width, and viewBox attributes
   svg.setAttribute('height', isvg_attributes['height'])
   svg.setAttribute('width', isvg_attributes['width'])
   svg.setAttribute('viewBox', isvg_attributes['viewBox'])
   # All path nodes under svg
   paths = svg.getElementsByTagName("path")
   wbbox = xmax-xmin
   hbbox = ymax-ymin
   strwidth = isvg_attributes['width']
   if not(strwidth.isdigit()):
      # For now, assume it is a two character unit at the end of the string
      # TODO: Process the units field and modify paths accordingly
      midbbox = (float(strwidth[:-2])-wbbox)/2 -xmin
   else:
      midbbox = (float(strwidth)-wbbox)/2 -xmin
   strheight = isvg_attributes['height']
   if not(strwidth.isdigit()):
      # For now, assume it is a two character unit at the end of the string
      # TODO: Process the units field and modify paths accordingly
      centerbbox = (float(strheight[:-2])-hbbox)/2 -ymin
   else:
      centerbbox = (float(strheight)-hbbox)/2 -ymin
   for p in range(len(paths)):
      # Change paths to close with z rather than repeating first point
      inodes = paths[p].getAttribute('d').split()
      dstr = ''
      firstpoint = ''
      lastpoint = ''
      rplcoord = 0
      process = 1
      for coord in range(len(inodes)):
         if not((inodes[coord] == 'M') or (inodes[coord] == 'L')):
            if firstpoint == '':
               firstpoint = inodes[coord]
            elif coord == len(inodes)-1: # check last point
               if inodes[coord] == firstpoint: # does it repeat first point
                  dstr = dstr + 'z' # yes. replace it with a z
                  process = 0 # and stop processing
               else:
                  ipoint = inodes[coord].split(',')
                  dstr = dstr + cstr + str((float(ipoint[0])+midbbox)*docscale) + ',' + str((float(ipoint[1])+centerbbox)*docscale) + ' '
                  process = 0
            if(process == 1):
               ipoint = inodes[coord].split(',')
               dstr = dstr + cstr + str((float(ipoint[0])+midbbox)*docscale) + ',' + str((float(ipoint[1])+centerbbox)*docscale) + ' '
            else:
               paths[p].setAttribute('d', dstr) # and replace the path
         else:
            cstr = inodes[coord] + ' '
      # Update the path ids to something more meaningful
      paths[p].setAttribute('id',ids[p])
   with open(outputfile,'w') as xml_file:
      DOMTree.writexml(xml_file, indent="\t", newl="\n")
   try:
      os.remove(tmpfile)
   except OSError:
      pass   
   root = tkinter.Tk()
   root.withdraw()
   messagebox.showinfo("Collar Successful Termination", "width = "+str(round(xmax-xmin,3))+", height = "+str(round(ymax-ymin,3)), parent=root)

def makepoly(toplength, numpoly):
   # Assuming pt1 > pt2
   r = toplength/(2*math.sin(math.pi/numpoly))
   pstr = 'M'
   for ppoint in range(0,numpoly):
      xn = r*math.cos(2*math.pi*ppoint/numpoly)
      yn = r*math.sin(2*math.pi*ppoint/numpoly)
      pstr = pstr + ' ' + str(xn) + ',' + str(yn)
      if ppoint == 0:
         x0 = xn
         y0 = yn
   pstr = pstr + ' ' + str(x0) + ',' + str(y0)
   ppaths = parse_path(pstr)
   return ppaths

def makeTab(pt1, pt2, orient):
   global orientTop
   global orientBottom
   global orientRight
   global orientLeft
   global tab_height
   global tab_angle
   switched = 0
   rpt1x = rpt1y = rpt2x = rpt2y = 0.0
   tabDone = False
   currTabHt = tab_height
   currTabAngle = tab_angle
   while not tabDone:
      if (orient == orientTop) or (orient == orientBottom):
         if pt1.real > pt2.real:
            ppt1 = pt2
            ppt2 = pt1
            switched = 1
         else:
            ppt1 = pt1
            ppt2 = pt2
         if orient == orientTop:
            TBset = -1
         elif orient == orientBottom:
            TBset = 1
         tp1 = complex(0, TBset*currTabHt) 
         tp2 = complex(0, TBset*currTabHt)
         rtp1x = tp1.real*math.cos(math.radians(-TBset*currTabAngle)) - tp1.imag*math.sin(math.radians(-TBset*currTabAngle)) + ppt1.real
         rtp1y = tp1.imag*math.cos(math.radians(-TBset*currTabAngle)) + tp1.real*math.sin(math.radians(-TBset*currTabAngle)) + ppt1.imag
         rtp2x = tp2.real*math.cos(math.radians(TBset*currTabAngle)) - tp2.imag*math.sin(math.radians(TBset*currTabAngle)) + ppt2.real
         rtp2y = tp2.imag*math.cos(math.radians(TBset*currTabAngle)) + tp2.real*math.sin(math.radians(TBset*currTabAngle)) + ppt2.imag
      elif (orient == orientRight) or (orient == orientLeft):
         if pt1.imag < pt2.imag:
            ppt1 = pt2
            ppt2 = pt1
            switched = 1
         else:
            ppt1 = pt1
            ppt2 = pt2
         if orient == orientRight:
            TBset = -1
         else: # orient == orientLeft
            TBset = 1
         tp1 = complex(-TBset*currTabHt, 0)
         tp2 = complex(-TBset*currTabHt, 0)
         rtp1x = tp1.real*math.cos(math.radians(TBset*currTabAngle)) - tp1.imag*math.sin(math.radians(TBset*currTabAngle)) + ppt1.real
         rtp1y = tp1.imag*math.cos(math.radians(TBset*currTabAngle)) + tp1.real*math.sin(math.radians(TBset*currTabAngle)) + ppt1.imag
         rtp2x = tp2.real*math.cos(math.radians(-TBset*currTabAngle)) - tp2.imag*math.sin(math.radians(-TBset*currTabAngle)) + ppt2.real
         rtp2y = tp2.imag*math.cos(math.radians(-TBset*currTabAngle)) + tp2.real*math.sin(math.radians(-TBset*currTabAngle)) + ppt2.imag
         # Check for vertical line. If so, we are already done
         if (ppt1.real != ppt2.real):
            slope = (ppt1.imag - ppt2.imag)/(ppt1.real - ppt2.real)
            theta = math.degrees(math.atan(slope))
            # create a line segment from ppt1 to rtp1
            td1 = 'M '+str(ppt1.real)+' '+str(ppt1.imag)+' '+str(rtp1x)+' '+str(rtp1y)
            rrtp1 = parse_path(td1)
            # create a line segment from ppt2 to rtp2
            td2 = 'M '+str(ppt2.real)+' '+str(ppt2.imag)+' '+str(rtp2x)+' '+str(rtp2y)
            rrtp2 = parse_path(td2)
            if orient == orientRight:
               # rotate the points theta degrees
               if slope < 0:
                  rtp1 = rrtp1.rotated(90+theta, ppt1)
                  rtp2 = rrtp2.rotated(90+theta, ppt2)
               else:
                  rtp1 = rrtp1.rotated(-90+theta, ppt1)
                  rtp2 = rrtp2.rotated(-90+theta, ppt2)
            if orient == orientLeft:
               # rotate the points theta degrees
               if slope < 0:
                  rtp1 = rrtp1.rotated(90+theta, ppt1)
                  rtp2 = rrtp2.rotated(90+theta, ppt2)
               else:
                  rtp1 = rrtp1.rotated(-90+theta, ppt1)
                  rtp2 = rrtp2.rotated(-90+theta, ppt2)
            rtp1x = rtp1[0][1].real
            rtp1y = rtp1[0][1].imag
            rtp2x = rtp2[0][1].real
            rtp2y = rtp2[0][1].imag
      print('Testing: '+str(ppt1.real)+','+str(ppt1.imag)+' '+str(rtp1x)+','+str(rtp1y)+' '+str(rtp2x)+','+str(rtp2y)+' '+str(ppt2.real)+','+str(ppt2.imag))
      if detectIntersect(ppt1.real, ppt1.imag, rtp1x, rtp1y, ppt2.real, ppt2.imag, rtp2x, rtp2y):
         print('Intersect: '+str(currTabAngle)+' degrees, '+str(currTabHt)+' inches, orientation '+str(orient))
         currTabAngle = currTabAngle - 1.0
         if currTabAngle < 2.0:
            currTabHt = currTabHt - 0.1
            currTabAngle = tab_angle
      else:
         print('No Intersect: '+str(currTabAngle)+' degrees, '+str(currTabHt)+' inches, orientation '+str(orient))
         tabDone = True
   p1 = complex(rtp1x,rtp1y)
   p2 = complex(rtp2x,rtp2y)
   if switched == 0:
      return p1, p2
   else:
      return p2, p1

def detectIntersect(x1, y1, x2, y2, x3, y3, x4, y4):
   td = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
   if td == 0:
      # These line segments are parallel
      return false
   t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/td
   if (0.0 <= t) and (t <= 1.0):
      return True
   else:
      return False

def makescore(ipt1, ipt2, dashlength):
   # Need pt1y > pt2y
   # Dash = dashlength (in inches) space followed by dashlength mark
   # if dashlength is zero, we want a solid line
   if ipt1.y < ipt2.y:
      pt1 = ipt2
      pt2 = ipt1
   elif ipt1.y == ipt2.y:
      if ipt1.x < ipt2.x:
         pt1 = ipt1
         pt2 = ipt2
      else:
         pt1 = ipt2
         pt2 = ipt1
   else:
      pt1 = ipt1
      pt2 = ipt2
   if dashlength == 0:
      ddash = 'M '+str(pt1.x)+','+str(pt1.y)+' L '+str(pt2.x)+','+str(pt2.y)
   else:
      if pt1.y == pt2.y:
         # We are drawing horizontal dash lines. Assume pt1x < pt2x
         xcushion = pt2.x - dashlength
         ddash = ''
         xpt = pt1.x
         ypt = pt1.y
         done = False
         while not(done):
            if (xpt + dashlength*2) <= xcushion:
               xpt = xpt + dashlength
               ddash = ddash + 'M ' + str(xpt) + ',' + str(ypt) + ' '
               xpt = xpt + dashlength
               ddash = ddash + 'L ' + str(xpt) + ',' + str(ypt) + ' '
            else:
               done = True
      elif pt1.x == pt2.x :
         # We are drawing vertical dash lines.
         ycushion = pt2.y + dashlength
         ddash = ''
         xpt = pt1.x
         ypt = pt1.y
         done = False
         while not(done):
            if(ypt - dashlength*2) >= ycushion:
               ypt = ypt - dashlength         
               ddash = ddash + 'M ' + str(xpt) + ' ' + str(ypt) + ' '
               ypt = ypt - dashlength
               ddash = ddash + 'L ' + str(xpt) + ' ' + str(ypt) + ' '
            else:
               done = True
      else:
         m = (pt1.y-pt2.y)/(pt1.x-pt2.x)
         theta = math.atan(m)
         msign = (m>0) - (m<0)
         ycushion = pt2.y + dashlength*math.sin(theta)
         xcushion = pt2.x + msign*dashlength*math.cos(theta)
         ddash = ''
         xpt = pt1.x
         ypt = pt1.y
         done = False
         while not(done):
            nypt = ypt - dashlength*2*math.sin(theta)
            nxpt = xpt - msign*dashlength*2*math.cos(theta)
            if (nypt >= ycushion) and (((m<0) and (nxpt <= xcushion)) or ((m>0) and (nxpt >= xcushion))):
               # move to end of space / beginning of mark
               xpt = xpt - msign*dashlength*math.cos(theta)
               ypt = ypt - msign*dashlength*math.sin(theta)
               ddash = ddash + 'M ' + str(xpt) + ' ' + str(ypt) + ' '
               # draw the mark
               xpt = xpt - msign*dashlength*math.cos(theta)
               ypt = ypt - msign*dashlength*math.sin(theta)
               ddash = ddash + 'L' + str(xpt) + ' ' + str(ypt) + ' '
            else:
               done = True
   return ddash

# Thanks to Gabriel Eng for his python implementation of https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
def findIntersection(x1,y1,x2,y2,x3,y3,x4,y4):
        px= ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) ) 
        py= ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
        return px, py
  
if __name__ == "__main__":
   main(sys.argv[1:])# Ensure that arguments are valid
