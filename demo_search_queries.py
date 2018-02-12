# The search queries for demos using Tasks in Close.io


# The demo scheduled query
def demos_scheduled_query(date_created, creator):

	query = 'task(description:"DSCHED" created:"{}" creator:{})'.format(
				date_created, creator
			)

	return query


# The demo rescheduled query
def demos_rescheduled_query(date_created, creator):

	query = 'task(description:"DRS" created:"{}" creator:{})'.format(
				date_created, creator
			)

	return query


# The demo held query
def demos_held_query(date_updated, creator):

	query = 'task(description:"DHELD" updated:"{}" creator:{} is_complete:yes)'.format(
				date_updated, creator
			)

	return query


# The demo's held by query
def demos_conducted_query(date_updated, creator):

	query = 'task(description:"DHELD" updated:"{}" assigned_to:"{}" is_complete:yes)'.format(
				date_updated, creator
			)

	return query
