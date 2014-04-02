import BeautifulSoup
import os
import sys
import csv
import pprint

from collections import defaultdict

import redis
r_server = redis.Redis("localhost")

CE = 'Course Evaluations'
FE = 'Faculty Evaluations'


course_files = [os.path.join(os.curdir, CE , x) for x in os.listdir(os.path.join(os.curdir, CE))]
fac_files = [os.path.join(os.curdir, FE ,x) for x in os.listdir(os.path.join(os.curdir, FE))]

all_courses = []
all_faculty = []

for x in course_files:
    print x

    res = r_server.get(x)

    if res != None:
        soup = BeautifulSoup.BeautifulSoup(res)
        print 'Retrieving from redis', len(res)
    else:
        with open(x, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup.BeautifulSoup(contents)

        print 'Saving contents of', x
        r_server.set(x, contents)

    tables = soup.findAll('table')

    for t in tables:

        c = defaultdict(dict)

        trs = t.findAll('tr')

        #Course Semester
        sem = trs[0].find('td').text.split(":")[1].strip()
        c['sem'] = sem

        #Course Code
        code = trs[0].find('td').text.split(":")[0].strip()
        c['code'] = code

        #Course Title
        title = trs[1].find('td').text.split(',')[1].strip()
        c['title'] = title

        evals = defaultdict(dict)

        # Course Content Matched Goals?

        n, avg, low, high = (x.text for x in trs[3].findAll('td')[1:])

        evals['matched_goals']['n'] = n
        evals['matched_goals']['avg'] = avg
        evals['matched_goals']['low'] = low
        evals['matched_goals']['high'] = high

        # Exams Covered Material?

        n, avg, low, high = (x.text for x in trs[4].findAll('td')[1:])

        evals['exams_covered_materials']['n'] = n
        evals['exams_covered_materials']['avg'] = avg
        evals['exams_covered_materials']['low'] = low
        evals['exams_covered_materials']['high'] = high

        # Assignment Covered Material?

        n, avg, low, high = (x.text for x in trs[5].findAll('td')[1:])

        evals['assignments_covered_materials']['n'] = n
        evals['assignments_covered_materials']['avg'] = avg
        evals['assignments_covered_materials']['low'] = low
        evals['assignments_covered_materials']['high'] = high

        # Lectures, readings helped learn?

        n, avg, low, high = (x.text for x in trs[6].findAll('td')[1:])

        evals['lectures-readings_helped_learn']['n'] = n
        evals['lectures-readings_helped_learn']['avg'] = avg
        evals['lectures-readings_helped_learn']['low'] = low
        evals['lectures-readings_helped_learn']['high'] = high

        # Discussions/Readings helped?

        n, avg, low, high = (x.text for x in trs[7].findAll('td')[1:])

        evals['discussion-readings_helped_learn']['n'] = n
        evals['discussion-readings_helped_learn']['avg'] = avg
        evals['discussion-readings_helped_learn']['low'] = low
        evals['discussion-readings_helped_learn']['high'] = high

        # Relevent to the curriculum?

        n, avg, low, high = (x.text for x in trs[8].findAll('td')[1:])

        evals['relevant_curriculum']['n'] = n
        evals['relevant_curriculum']['avg'] = avg
        evals['relevant_curriculum']['low'] = low
        evals['relevant_curriculum']['high'] = high

        # Overall rating of this course

        n, avg, low, high = (x.text for x in trs[9].findAll('td')[1:])

        evals['overall_rating']['n'] = n
        evals['overall_rating']['avg'] = avg
        evals['overall_rating']['low'] = low
        evals['overall_rating']['high'] = high

        c['evals'] = evals

        all_courses.append(c)



for x in fac_files:
    print x

    res = r_server.get(x)

    if res != None:
        soup = BeautifulSoup.BeautifulSoup(res)
        print 'Retrieving from redis', len(res)

    else:
        with open(x, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup.BeautifulSoup(contents)

        print 'Saving contents of', x
        r_server.set(x, contents)

    tables = soup.findAll('table')

    for t in tables:

        c = defaultdict(dict)

        trs = t.findAll('tr')

        #Instructor Name
        c['name'] = trs[0].find('td').text.split(":")[1].strip()
        print c['name']

        #Course Semester
        c['sem'] = trs[1].find('td').text.split(":")[1].strip()
        print c['sem']

        #Course Title
        c['title'] = trs[2].find('td').text.split(':')[1].strip()
        print c['title']


        evals = defaultdict(dict)

        # Was Instructor Enthusiastic?

        n, avg, low, high = (x.text for x in trs[4].findAll('td')[1:])

        evals['enthusiastic']['n'] = n
        evals['enthusiastic']['avg'] = avg
        evals['enthusiastic']['low'] = low
        evals['enthusiastic']['high'] = high

        # Did Instructor Provide Feedback?

        n, avg, low, high = (x.text for x in trs[5].findAll('td')[1:])

        evals['provide_feedback']['n'] = n
        evals['provide_feedback']['avg'] = avg
        evals['provide_feedback']['low'] = low
        evals['provide_feedback']['high'] = high

        # Instructor demand critical thinking?

        n, avg, low, high = (x.text for x in trs[6].findAll('td')[1:])

        evals['demand_original_thinking']['n'] = n
        evals['demand_original_thinking']['avg'] = avg
        evals['demand_original_thinking']['low'] = low
        evals['demand_original_thinking']['high'] = high

        # Overall Rating of Instructor

        n, avg, low, high = (x.text for x in trs[7].findAll('td')[1:])

        evals['overall_rating']['n'] = n
        evals['overall_rating']['avg'] = avg
        evals['overall_rating']['low'] = low
        evals['overall_rating']['high'] = high

        c['evals'] = evals

        all_faculty.append(c)

with open('course_evals_output.txt', 'w') as o:
    pprint.pprint(all_courses, o)

with open('faculty_evals_output.txt', 'w') as o:
    pprint.pprint(all_faculty, o)








