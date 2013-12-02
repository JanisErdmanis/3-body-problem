# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 00:02:39 2013

@author: akels
"""
from __future__ import division, print_function
from os import sys
sys.path.append('cpresources')
from pylab import *


def r(r1,r2):

	delta = r1 - r2
	length = sqrt(delta[0]**2 + delta[1]**2)

	return delta/length**3

#G = 1
#m1 = 150
#m2 = 200
#m3 = 250

def f(r_,t):
	r1,r2,r3,v1,v2,v3 = r_

	Dr1 = v1
	Dr2 = v2
	Dr3 = v3

	Dv1 = m2*r(r2,r1) + m3*r(r3,r1)
	Dv2 = m1*r(r1,r2) + m3*r(r3,r2)
	Dv3 = m1*r(r1,r3) + m2*r(r2,r3)

	return array([Dr1,Dr2,Dr3,Dv1,Dv2,Dv3],float)



class rksolve:

	def __init__(self,f):

		self.f = f #self.array_decorator(f)

		self.initial_conditions = None
		self.solution = None


	def estimate_delta_rk4(self,r,t,h):

		f = self.f
		k1 = h*f(r,t)
		k2 = h*f(r+0.5*k1,t+0.5*h)
		k3 = h*f(r+0.5*k2,t+0.5*h)
		k4 = h*f(r+k3,t+h)
		return (k1+2*k2+2*k3+k4)/6

	def iterate(self,a,b,delta=1):


		r0 = array(self.initial_conditions,float96)

		h = (b-a)/10000
		solution = []
		time = []
		r = r0
		t = a



		ro = 1
		solution = []
		time = []
		solution.append(copy(r))
		time.append(t)

		# Kamēr apskatītais laika moments
		# nav lielāks par beigu laiku
		while t<b:
			# Vieta, kur mainīt soļa izmēru

			if ro<2:
				h = h*ro**(1/4)
			else:
				h*=2

			# un novērtēt soļa precizitāti
			r1 = r + self.estimate_delta_rk4(r,t,h)
			r1 += self.estimate_delta_rk4(r1,t+h,h)
			r2 = r + self.estimate_delta_rk4(r,t,2*h)
			ro = 30*h*delta/sqrt(sum((r1-r2)**2)) #self.distance(r1,r2)


			# Noraidīt vai apstiprināt iegūto r1 vērtību
			if ro>1:
				t +=2*h
				r = r1
				solution.append(copy(r))
				time.append(t)

		self.solution = array(solution)
		self.t = array(time)


prob = rksolve(f)

#r1 = [3,1]
#r2 = [-1,-2]
#r3 = [-1,1]

prob.initial_conditions = [r1,r2,r3,[0,0],[0,0],[0,0]]

prob.iterate(0,end,delta=1e-3)

fig = figure()
for i in range(3):
	x = prob.solution[:,i,0]
	y = prob.solution[:,i,1]
	plot(x,y,'-',label=i)
	plot(x[::10],y[::10],'k.',)
legend()
show()

from visual import sphere, rate

def radius(m):

	return m**(1/3)/100

s1 = sphere(radius=radius(150*5))
s2 = sphere(radius=radius(200*5))
s3 = sphere(radius=radius(250*5))

s = [s1,s2,s3]

C = 0.1
t = prob.t
h = t[1:] - t[:-1]
for h,pos in zip(h,prob.solution[:-1,:3]):
	rate(int(C/h))

	for si,posi in zip(s,pos):
		rx,ry = posi
		si.pos = rx,ry,0
