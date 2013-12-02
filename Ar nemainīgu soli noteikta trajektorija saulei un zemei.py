# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 10:57:02 2013

@author: akels
"""
from __future__ import division, print_function
from os import sys
from pylab import *
from math import sqrt

class rksolve:

	#h = 1

	def __init__(self,f):

		self.f = f #self.array_decorator(f)

		self.initial_conditions = None
		self.solution = None

# Ar Eilera metodi
	def estimate_delta_euler(self,r,t,h):

		f = self.f
		delta = h*f(r,t)
		return delta


	def iterate(self,a,b):

		r0 = array(self.initial_conditions,float96)

		h = (b-a)/50

		r = r0
		t = a

		solution = []
		time = []
		solution.append(copy(r))
		time.append(t)

		# Kamēr apskatītais laika moments
		# nav lielāks par beigu laiku
		while t<b:

			# Vieta, kur mainīt soļa izmēru
			# un novērtēt soļa precizitāti
			r1 = r + self.estimate_delta_euler(r,t,h)

			# Noraidīt vai apstiprināt iegūto r1 vērtību
			if True:
				t +=h
				r = r1
				solution.append(copy(r))
				time.append(t)

		self.solution = array(solution)
		self.t = time


G = 6.67e-11
M = 1.9e30

def f(r,t):

	x,y,vx,vy = r

	Dx = vx
	Dy = vy

	R = sqrt(x**2 + y**2)
	Dvx = -G*M*x/R**3
	Dvy = -G*M*y/R**3

	return array([Dx,Dy,Dvx,Dvy])

prob = rksolve(f)


R = 1.496e11
T = 3.156e7
v = 2*pi*R/T
prob.initial_conditions = [4e12,0,0,500]

delta = 1e3/365/24/60/60
prob.iterate(0,T*27)

fig = figure()

x = prob.solution[:,0]
y = prob.solution[:,1]

plot(x,y,'.-')
show()
