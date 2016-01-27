# Dictates the rhythm you tab using the space bar.
# '.' Stops the program. 
# sample run:
# arugments are in the following order: bpm, minimum_sub, beats_per_bar
# python dictation.py 120 8 4


from decimal import *
import datetime
from datetime import date, time
import re
import sys
import time

try: 

	from msvcrt import getch 

except ImportError:

	def getch( ): 

		import sys, tty, termios 
		fd = sys.stdin.fileno( ) 
		old_settings = termios.tcgetattr(fd) 

		try: 

			tty.setraw(fd) 
			ch = sys.stdin.read(1)

		finally: 

			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 

			return ch



def dictate():
	"""Handles the dictation of keyboard hits given bpm."""
	# Bpm (beats per minute) 
	# Timeline will store a list of tuples: (beat/hit, time)

	count = 0

	while True: 

		key = ord(getch())


		# Int value of spacebar in ascii is 32
		# First keyboard hit.
		if key == 32 and count == 0: 

			_START_TIME = datetime.datetime.time(datetime.datetime.now())
			_TIMELINE.append(datetime.timedelta(seconds=0))


		# All other kb hits
		elif key == 32:

			_TIMELINE.append(get_time(_START_TIME))


		if key == 46: # '.' key

			represent(_BPM, _SUB)

			break 

		count += 1

		print _TIMELINE


	return None


def get_time(start):
	"""Returns duration from argument, start."""
	now = datetime.datetime.time(datetime.datetime.now())

	return datetime.datetime.combine(date.today(), now) \
		- datetime.datetime.combine(date.today(), start)


def represent(bpm, subdivision):
	"""Prints global list, timeline, rounding values to the nearest subdivision."""

	seconds = Decimal(1 / Decimal((Decimal(bpm) / Decimal(60)))) # Seconds per beat.
	sub = Decimal(seconds) / Decimal(subdivision) # Seconds per subdivision

	print sub
	placement = None
	rhythm = [0]

	for hit in _TIMELINE:

		# Round the division by the subdivision to the nearest beat placement
		raw_placement = Decimal(hit.total_seconds()) / Decimal(sub)

		try:

			if int(str(raw_placement).split('.')[1][0]) >=5 : # first decimal place

				placement = int(raw_placement) + 1
				rhythm.append(placement)

			elif int(str(raw_placement).split('.')[1][0]) < 5: 

				placement = int(raw_placement)
				rhythm.append(placement)


		except IndexError:

			pass

	difference = [rhythm[i] - rhythm[i-1] for i in range(1, len(rhythm))]

	barred_rhythm = ''

	for d in difference: 

		try:

			barred_rhythm += 'X'
			barred_rhythm += d * '-'

		except IndexError:

			pass


	print barred_rhythm + 'X'

	
	return None


if __name__ == '__main__':

	_START_TIME = ''
	_TIMELINE = []
	_BPM = int(sys.argv[1])
	_SUB = int(sys.argv[2])
	_BPB = int(sys.argv[3])

	if len(sys.argv) != 4:

		print 'Enter beats per minute and the smallest desired subdivision, how many beats per bar.'

	else: 

		dictate()
