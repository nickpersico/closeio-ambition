# Close.io API Functions
# Functions to the Close.io API using the closeio-api wrapper
from closeio_api import Client
import json


# Generate an activity report for a specific user
def generate_user_activity_report(api_key, org_id, date_start, date_end, user_id):

    closeio_api = Client(api_key)

    user_activity_report = closeio_api.get(
        'report/activity/{}'.format(org_id),
        params={
            'date_start': date_start,
            'date_end': date_end,
            'user_id': user_id,
        }
    )

    return user_activity_report


# Get a list of users in your Close.io organization
def get_list_of_users(api_key):

    closeio_api = Client(api_key)

    has_more = True
    offset = 0
    limit = 100

    list_of_users = []

    while has_more:

        response = closeio_api.get(
            'user',
            params={'_skip': offset, '_limit': limit}
        )

        users = response['data']

        for user in users:
            list_of_users.append(user)

        has_more = response['has_more']
        offset += limit

    return list_of_users


# Get a list of leads using a search query
def get_list_of_leads_via_search_query(api_key, search_query):

    closeio_api = Client(api_key)

    has_more = True
    offset = 0
    limit = 100

    list_of_leads = []

    while has_more:

        response = closeio_api.get(
            'lead',
            params={'_skip': offset, '_limit': limit, 'query': search_query}
        )

        leads = response['data']

        for lead in leads:
            list_of_leads.append(lead)

        has_more = response['has_more']
        offset += limit

    return list_of_leads


# # Retrieve lead data from Lead ID
# def get_lead_data(api_key, lead_id):

#     closeio_api = Client(api_key)
#     api_url = 'lead/{}'.format(lead_id)
#     lead_data = closeio_api.get(api_url)

#     return lead_data