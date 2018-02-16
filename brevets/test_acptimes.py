'''
Nose tests for acp_times.py
'''

import acp_times
import nose
import logging
import arrow

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.WARNING)
log = logging.getLogger(__name__)


def test_small():
	'''
	Tests a control value which is less than or equal to the first value 
	in the acp table (ie. less than to 200), thus requiring only
	one calculation to determine time
	'''
	date = arrow.Arrow(2013,5,5)
	
	assert acp_times.open_time(150, 200, arrow.get(date)) == (date.shift(hours=4,minutes=25)).isoformat()
	assert acp_times.close_time(150, 200, arrow.get(date)) == (date.shift(hours=10)).isoformat()

def test_big():
	'''
	Tests a control value which contains multiple markers in the acp table, 
	requiring multiple calculations and additions of times in order to 
	determine the correct times
	'''
	date = arrow.Arrow(2013,5,5)
	
	assert acp_times.open_time(700, 1000, arrow.get(date)) == (date.shift(hours=22,minutes=22)).isoformat()
	assert acp_times.close_time(700, 1000, arrow.get(date)) == (date.shift(hours=48,minutes=45)).isoformat()

def test_boundry_case():
	'''
	Tests a control value that is exactly equal to one of the distance 
	values in the table - this should correctly determine which speed
	to use from the boundry case based off of the acp rules.
	'''
	
	date = arrow.Arrow(2013,5,5)
	
	assert acp_times.open_time(600, 600, arrow.get(date)) == (date.shift(hours=18,minutes=48)).isoformat()
	assert acp_times.close_time(600, 600, arrow.get(date)) == (date.shift(hours=40)).isoformat()

def test_medium():
	'''
	Tests a medium control value of 550 (a non boundry case).
	'''

	date = arrow.Arrow(2013,5,5)

	assert acp_times.open_time(550, 600, arrow.get(date)) == (date.shift(hours=17,minutes=8)).isoformat()
	assert acp_times.close_time(550, 600, arrow.get(date)) == (date.shift(hours=36,minutes=40)).isoformat()

def test_odd():
	'''
	Tests a brevet control length which is an odd number.
	'''
	
	date = arrow.Arrow(2013,5,5)

	assert acp_times.open_time(311, 400, arrow.get(date)) == (date.shift(hours=9,minutes=21)).isoformat()
	assert acp_times.close_time(311, 400, arrow.get(date)) == (date.shift(hours=20,minutes=44)).isoformat()
