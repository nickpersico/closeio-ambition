# Send a Close.io Activity Report to Ambition
# A script that generates an Activity Report + other data from Close.io and
# uploads it to an Ambition endpoint

import json
import datetime
import sys
import time
from dateutil import tz

# Close.io
from _closeio import generate_user_activity_report
from _closeio import get_list_of_users
from _closeio import get_list_of_leads_via_search_query

# Ambition
from _ambition import upload_data_to_ambition

# Credentials
from _credentials import api_key
from _credentials import org_id
from _credentials import ENDPOINT
from _credentials import AUTH_TOKEN

# Demo Search Queries
from demo_search_queries import demos_scheduled_query
from demo_search_queries import demos_rescheduled_query
from demo_search_queries import demos_held_query
from demo_search_queries import demos_conducted_query

tz_off = (-time.timezone/60/60)


# Set up the amount of days in the past, set up report
day_list = []
PAST_DAYS = int(sys.argv[1])
TODAY = datetime.datetime.now()

count = 0

while count <= PAST_DAYS:
	d = datetime.datetime(TODAY.year, TODAY.month, TODAY.day, tzinfo=tz.tzutc()) - datetime.timedelta(days=count) - datetime.timedelta(hours=tz_off)
	day_list.append(d)
	count += 1


# Set up the list that will hold the report that's sent to Ambition
ambition_report = []

# Retrieve all of the users in your Close.io organization, build customized list
closeio_users = get_list_of_users(api_key)
user_list = []

for user in closeio_users:

	user_list.append({
		'first_name': user['first_name'],
		'last_name': user['last_name'],
		'email': user['email'],
		'user_id': user['id']
	})


# Iterate through each day, retrieving all the Activity data for each user
for day in day_list:
	start = day.strftime("%Y-%m-%dT%H:%M:%S")
	end = (day + datetime.timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")
	day = str(start).split('T')[0]

	for user in user_list:

		# Generate Activity Reports for each user
		print "Generating Activity Report for {} {} on {} ...".format(
			user['first_name'], user['last_name'], day
		)

		# Retrieve a User Activity Report from Close.io
		user_activity_report = generate_user_activity_report(
			api_key=api_key,
			org_id=org_id,
			date_start=start,
			date_end=end,
			user_id=user['user_id']
		)

		# Generate the number of Demos Scheduled, Rescheduled, & Held

		# Demo / Task Queries
		task_queries = [
			{
				'query': demos_scheduled_query(date_created=day, creator=user['user_id']),
				'query_name': "demos_scheduled"
			},
			{
				'query': demos_rescheduled_query(date_created=day, creator=user['user_id']),
				'query_name': "demos_rescheduled"
			},
			{
				'query': demos_held_query(date_updated=day, creator=user['user_id']),
				'query_name': "demos_held"
			},
			{
				'query': demos_conducted_query(date_updated=day, creator=user['user_id']),
				'query_name': "demos_conducted"
			}
		]

		for query in task_queries:

			leads_with_tasks = get_list_of_leads_via_search_query(
				api_key=api_key,
				search_query=query['query']
			)

			if query['query_name'] == "demos_scheduled":
				demos_scheduled = len(leads_with_tasks)
			if query['query_name'] == "demos_rescheduled":
				demos_rescheduled = len(leads_with_tasks)
			if query['query_name'] == "demos_held":
				demos_held = len(leads_with_tasks)
			if query['query_name'] == "demos_conducted":
				demos_conducted = len(leads_with_tasks)

		# Combine Demos Scheduled and Demos Rescheduled for a "total demos scheduled" for the day
		total_demos_scheduled = demos_scheduled + demos_rescheduled

		# Add the user's Activity Report data to the report going to Ambition
		ambition_report.append({
			"email": user['email'],
			"date": day,
			"calls": user_activity_report['calls'],
			"leads_contacted": user_activity_report['leads_contacted'],
			"emails_sent": user_activity_report['emails_sent'],
			"emails_received": user_activity_report['emails_received'],
			"call_duration": user_activity_report['calls_duration_total'],
			"call_duration_avg": user_activity_report['calls_duration_average'],
			"sms_sent": user_activity_report['sms_sent'],
			"sms_received": user_activity_report['sms_received'],
			"opportunities_created": user_activity_report['opportunities_created_created'],
			"revenue_created_one_time": user_activity_report['revenue_created_one_time_created']/100.0,
			"revenue_created_monthly": user_activity_report['revenue_created_monthly_created']/100.0,
			"revenue_created_annual": user_activity_report['revenue_created_annual_created']/100.0,
			"opportunities_lost": user_activity_report['opportunities_lost'],
			"revenue_lost_one_time": user_activity_report['revenue_lost_one_time']/100.0,
			"revenue_lost_monthly": user_activity_report['revenue_lost_monthly']/100.0,
			"revenue_lost_annual": user_activity_report['revenue_lost_annual']/100.0,
			"revenue_won_one_time": user_activity_report['revenue_won_one_time']/100.0,
			"revenue_won_monthly": user_activity_report['revenue_won_monthly']/100.0,
			"revenue_won_annual": user_activity_report['revenue_won_annual']/100.0,
			"opportunities_won": user_activity_report['opportunities_won'],
			"demos_scheduled": demos_scheduled,
			"demos_rescheduled": demos_rescheduled,
			"demos_held": demos_held,
			"total_demos_scheduled": total_demos_scheduled,
			"demos_conducted": demos_conducted
		})


# Send Activity Report to Ambition
send_report = upload_data_to_ambition(
	endpoint=ENDPOINT,
	auth_token=AUTH_TOKEN,
	payload=json.dumps(ambition_report)
)
