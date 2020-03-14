#!/usr/bin/env python

"""
    File name: dst.py
    Author: Eric Williams <wd6cmu@gmail.com>
    Date created: 3/09/2020
    Date last modified: Mar 12 2020
    Python Version: 2.7.3

    Description:
    Calculates if daylight savings time applies for a given time.
    Rules for DST are configurable.
    
    Bugs:
    Doesn't do European-style UTC-based transition
    Doesn't check for invalid parameters
"""
from __future__ import print_function

mName = ('JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC')
def m(name): return mName.index(name)+1

dName = ('SUN','MON','TUE','WED','THU','FRI','SAT')
def d(name): return dName.index(name)

def leap(year):
    return not ((year%4) and ((year%100) or not (year%400)))

def monthlen(year, month):
    monthDays = (31,28,31,30,31,30,31,31,30,31,30,31)
    days = monthDays[month-1]
    return days if month != m('FEB') else days+leap(year)

# Returns numeric day of week for given date, Sunday = 0
# Tomohiko Sakamoto’s Algorithm
def dow(year, month, mday):
    dow_table = [0,3,2,5,0,3,5,1,4,6,2,4]
    yy = year - (month < m('MAR'))
    return (yy + int(yy/4) - int(yy/100) + int(yy/400) + dow_table[month-1] + mday) % 7

# dst_rule has two tuples: one each for DST-start and DST-end
# Each tuple has four integer values:
#    Month (January = 1)
#    WeekSelect: N
#       if N > 0: Nth occurance of DOW DaySelect (1 = 1st)
#       if N < 0: Last occurance of DOW DaySelect
#       if N = 0: DaySelect is day of month
#    DaySelect:
#       if WeekSelect = 0: Day of month (i.e. date)
#       else: Day of week (0 = Sunday)
#    Hour of day to change, in adjusted local time
dst_rule = (
    (m('MAR'), 2, d('SUN'), 2),     # start: 2nd Sunday of March
    (m('NOV'), 1, d('SUN'), 2)      # end: 1st Sunday of November
)

# Given standard-time date+hour, return True if DST rule applies
def dst(year, month, mday, hour):
    start = True
    for (M,W,D,H) in dst_rule:
        if month == M: break
        start = False
    else:
        return (month > dst_rule[0][0]) and (month < dst_rule[1][0])
    if W > 0:       # Nth day-of-week
        ww = W * 7
        dd = ww + D - dow(year, month, ww)
    elif W == 0:    # date
        dd = D
    else:           # last day-of-week
        ldom = monthlen(year, month)    # last dom
        ldow = dow(year, month, ldom)   # dow of ldom
        dd = ldom - ((ldow - D) % 7)
    return \
        (mday > dd) or (mday == dd and hour >= H) if start \
        else (mday < dd) or (mday == dd and (hour+1) < H)

if __name__ == '__main__':

    def calendar(year, month):
        print('  %s  %d'%(mName[month], year))
        print('S M T W T F S')
        for day in range(0, dow(year, month, 1)): 
            print('  ', end='')
        for day in range (1, monthlen(year, month)+1):
            end = '\n' if dow(year, month, day) == 6 or \
                          monthlen(year, month) == day else ''
            print ('%d '%int(dst(year,month,day,12)), end=end)
        print()
        
    year = 2021
    calendar(year, m('MAR'))
    calendar(year, m('NOV'))
    calendar(year, m('FEB'))
