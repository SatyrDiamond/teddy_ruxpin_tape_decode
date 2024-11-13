import av
import cv2
import threading
import numpy as np

import sounddevice as sd
sd.default.samplerate = 44100
sd.default.channels = 2

inframe = np.zeros((500, 1000, 3), dtype=np.uint8)
outframe = np.zeros((500, 1000, 3), dtype=np.uint8)

finished = False

def gfx_drawsquare(inframe, x, y, w, h, val):
	inframe[x:x+w, y:y+h] = val

def gfx_drawsquare_color(inframe, x, y, w, h, b,g,r):
	inframe[x:x+w, y:y+h] = [r,g,b]

def gfx_printimage(inframe, source, x, y, w, h, sx, sy):
	inframe[x:x+w, y:y+h] = source[sx:sx+w, sy:sy+h]

padding = 5

class pos_base:
	def __init__(self, x, y):
		self.base_x = x
		self.base_y = y

	def gfx_drawsquarefree_color(self, x, y, w, h, b,g,r):
		gfx_drawsquare_color(inframe, self.base_x+x, self.base_y+y, w, h, b, g, r)

	def gfx_drawsquaremirror_color(self, inframe, x, y, size, b,g,r):
		gfx_drawsquare_color(inframe, (self.base_x+x)-(size//2), (self.base_y+y)-(size//2), size, size, b, g, r)
		gfx_drawsquare_color(inframe, (self.base_x+x)-(size//2), (self.base_y-y)-(size//2), size, size, b, g, r)

	def gfx_drawsquare_color(self, inframe, x, y, size, b,g,r):
		gfx_drawsquare_color(inframe, (self.base_x+x)-(size//2), (self.base_y+y)-(size//2), size, size, b, g, r)

	def gfx_drawsquare_color_s(self, inframe, x, y, sizex, sizey, b,g,r):
		gfx_drawsquare_color(inframe, (self.base_x+x)-(sizex//2), (self.base_y+y)-(sizey//2), sizex, sizey, b, g, r)

def gfx_drawblock(column, value):
	posval = (column+6)*50 + 1
	gfx_drawsquare(inframe, 50+1, posval, 300-1, 50-1, 0)
	gfx_drawsquare(inframe, 50, posval+(padding//2), value, 50-(padding), 200)

def gfx_init():
	inframe[:] = 0
	inframe[0::50] = 130
	inframe[:, 0::50] = 130
	inframe[:, 0:300:1] = 0

	inframe[351::1] = 0
	inframe[:, 701::1] = 0

gfx_init()

# teddy_eye
teddy_eye = np.empty((100, 50, 3), dtype=np.uint8)
gfx_drawsquare_color(teddy_eye, 0, 0, 100, 100, 169-10, 112-10, 67-10)
gfx_drawsquare_color(teddy_eye, 48, 0, 2, 50, 0, 0, 0)
gfx_drawsquare_color(teddy_eye, 50, 0, 50, 50, 200, 200, 200)
teddy_eye_gfx_base = pos_base(75, 25)
teddy_eye_gfx_base.gfx_drawsquare_color(teddy_eye, 0, 0, 35, 57*2, 16*2, 6*2)
teddy_eye_gfx_base.gfx_drawsquare_color(teddy_eye, 0, 0, 20, 0, 0, 0)

# grubby_eye
grubby_eye = np.empty((100, 50, 3), dtype=np.uint8)
gfx_drawsquare_color(grubby_eye, 0, 0, 100, 100, 241, 196, 136)
gfx_drawsquare_color(grubby_eye, 48, 0, 2, 50, 0, 0, 0)
gfx_drawsquare_color(grubby_eye, 50, 0, 50, 50, 200, 200, 200)
grubby_eye_gfx_base = pos_base(75, 25)
grubby_eye_gfx_base.gfx_drawsquare_color(grubby_eye, 0, 0, 35, 57, 74, 135)
grubby_eye_gfx_base.gfx_drawsquare_color(grubby_eye, 0, 0, 20, 0, 0, 0)

# main
teddy_gfx = pos_base(250, 150)
teddy_gfx.gfx_drawsquare_color(inframe, 0, 0, 200, 169, 112, 67)
teddy_gfx.gfx_drawsquaremirror_color(inframe, -100, 90, 80, 189, 112, 67)
teddy_gfx.gfx_drawsquaremirror_color(inframe, -90, 80, 50, 223, 205, 181)
def drawmouth(inframe, mouthup, mouthdown):
	teddy_gfx.gfx_drawsquare_color_s(inframe, 30+mouthup, 0, 50, 80, 223, 205, 181)
	teddy_gfx.gfx_drawsquare_color_s(inframe, 20+mouthup, 0, 20, 40, 0, 0, 0)
	teddy_gfx.gfx_drawsquare_color_s(inframe, 70+mouthdown, 0, 20, 80, 223, 205, 181)

# grubby
grubby_gfx = pos_base(250, 850)
grubby_gfx.gfx_drawsquare_color(inframe, 0, 0, 200, 241, 196, 136)
def drawmouth_grubby(inframe, mouthup, mouthdown):
	grubby_gfx.gfx_drawsquare_color_s(inframe, 30+mouthup, 0, 55, 105, 205, 117, 67)
	grubby_gfx.gfx_drawsquare_color_s(inframe, 30+mouthup, 0, 50, 100, 222, 199, 179)
	grubby_gfx.gfx_drawsquare_color_s(inframe, 20+mouthup, 0, 20, 50, 218, 92, 42)
	grubby_gfx.gfx_drawsquare_color_s(inframe, 70+mouthdown, 0, 25, 105, 205, 117, 67)
	grubby_gfx.gfx_drawsquare_color_s(inframe, 70+mouthdown, 0, 20, 100, 222, 199, 179)

for n in range(8):
	gfx_drawblock(n, 0)

procframe = np.copy(inframe)

class valsmooth:
	def __init__(self, intval, smoth):
		self.val = intval
		self.smoth = smoth

	def set(self, intval):
		outv = 1/self.smoth
		self.val = (self.val*(1-outv)) + (intval*outv)

focus_char = valsmooth(0, 6)
t_mouthup = valsmooth(0, 3)
t_mouthdown = valsmooth(0, 3)
g_mouthup = valsmooth(0, 3)
g_mouthdown = valsmooth(0, 3)
t_eyeout = valsmooth(0, 5)
g_eyeout = valsmooth(0, 5)

pan = valsmooth(0, 3)

def callback(values):
	global finished
	global pan
	if len(values) >= 8:

		procframe[:] = inframe[:]

		mul = 1

		for n, x in enumerate(values[0:8]):
			gfx_drawblock(n, x)

			x /= mul

			if n == 0:
				mul = x/56
				#print(x, mul)

			if n == 1:
				eyeout = 100+((50-x)*4)
				t_eyeout.set(max(0, min(eyeout, 50)))
				gfx_printimage(procframe, teddy_eye, 200-10, 80, 50, 50, int(t_eyeout.val), 0)
				gfx_printimage(procframe, teddy_eye, 200-10, 170, 50, 50, int(t_eyeout.val), 0)

			if n == 2: t_mouthup.set(-(50-x)*2)
			if n == 3: t_mouthdown.set(-(40-x)*2)

			if n == 4:
				dpan = x-52
				focus_char.set(dpan)
				dpan /= 20
				pan.set(dpan)

			if n == 5:
				eyeout = 100+((50-x)*4)
				g_eyeout.set(max(0, min(eyeout, 50)))
				gfx_printimage(procframe, grubby_eye, 200-10, 700+80, 50, 50, int(g_eyeout.val), 0)
				gfx_printimage(procframe, grubby_eye, 200-10, 700+170, 50, 50, int(g_eyeout.val), 0)
			if n == 6: g_mouthup.set(-(50-x)*2)
			if n == 7: g_mouthdown.set(-(40-x)*2)

		drawmouth(procframe, -(int(t_mouthup.val)//6), (int(t_mouthdown.val)//3))
		drawmouth_grubby(procframe, -(int(g_mouthup.val)//6), (int(g_mouthdown.val)//3))
		gfx_drawsquare(procframe, 400, max(400+int(focus_char.val*18), 0), 50, 200, 200)

		outframe[:] = procframe[:]

		finished = True

class pulselistener:
	def __init__(self):
		self.prev = False
		self.count = 0
		self.values = []

	def inframe(self, sample):
		sampbool = sample<-0.08
		if sampbool:
			if self.count: 
				if self.count>200: 
					callback(self.values)
					self.values = []
				else:
					self.values.append(self.count)
						
			self.count = 0
		else:
			self.count += 1
		self.prev = sampbool

def showvisual():
	global finished
	cv2.imshow('inframe', procframe)
	while True:
		if finished: 
			cv2.imshow('inframe', procframe)
			finished = False
		cv2.waitKey(1)

threading.Thread(target=showvisual).start()

pl_obj = pulselistener()


def print_sound(indata, outdata, inframes, time, status):
	for l, r in indata:
		pl_obj.inframe(r)
	#print(max(pan, 0), abs(min(pan, 0)))

	teddy_mute = min(1, max(pan.val, 0))
	grubby_mute = min(1, abs(min(pan.val, 0)))

	l = indata[:, 0]*(1-grubby_mute)
	r = indata[:, 0]*(1-teddy_mute)
	outdata[:, 1] = l
	outdata[:, 0] = r

with sd.Stream(callback=print_sound):
    sd.sleep(10000000)

#for x in range(blocks):
#	d = data[x*blocksize:(x+1)*blocksize]
#	print(d)
#	for l, r in d:
#		pl_obj.inframe(r)
#		#sd.play(r, 44100)
