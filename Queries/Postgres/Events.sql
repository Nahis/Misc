-- notifications
select entity_type as type, event, timestamp,entity_id as id, e.organization_id, e.job_id, e.appointment_id, e.data, e.actor_id, e.actor_type, data->>'message' message,data->>'rating' rating, j.external_id job_external_id, j.customer_external_id
from eventbus_events e
inner join accounts a on a.id = e.account_id
left join jobs j on j.id = e.job_id
where event like 'notification%'
and e.job_id = 12907974
order by timestamp



-- between times
select entity_type as type, event, timestamp,entity_id as id, e.organization_id, e.job_id, e.appointment_id, e.customer_id, e.actor_id, e.actor_type, data->>'message' message,data->>'rating' rating, j.external_id job_external_id, j.customer_external_id
from eventbus_events e
inner join accounts a on a.id = e.account_id
left join jobs j on j.id = e.job_id
where a.id = 4
and event in ('appointment.canceled','appointment.complete','appointment.enroute','appointment.scheduled','appointment.started',
'job.canceled','job.closed','job.complete','job.paused','job.rejected','job.unscheduled','attachment.created','survey_response.submitted',
'job_offer.entity_offered','job_offer.entity_accepted','job_offer.entity_declined')
and e.job_id = 2776075
order by timestamp


select entity_type as type, event, timestamp,entity_id as id, e.organization_id, e.job_id, e.appointment_id, e.customer_id,data->>'message' message,data->>'rating' rating, j.external_id job_external_id, j.customer_external_id,app.started_at,app.duration
from eventbus_events e
inner join accounts a on a.id = e.account_id
left join jobs j on j.id = e.job_id
left join appointments app on j.first_appointment_id = app.id
where a.id = 4
and event in ('appointment.canceled','appointment.complete','appointment.enroute','appointment.scheduled','appointment.started',
'job.canceled','job.closed','job.complete','job.paused','job.rejected','job.unscheduled','attachment.created','survey_response.submitted')
and e.timestamp <= '03/01/2017 18:34:19'
and e.timestamp >= '03/01/2017 16:13:56'
order by timestamp


-- attachments
select a.id attachment_id, a.file_token, a.created_at as timestamp, a.description, a.entity_id job_id, j.external_ids job_external_id, c.external_ids customer_external_id
from attachments a
inner join jobs j on j.id = a.entity_id and a.entity_type = 'Job'
inner join customers c on c.id = j.customer_id
where a.created_at >= '2017-02-06 13:00:00'
and a.created_at >= '2017-02-07 17:00:00'
and j.source_id = 11

--appointment created
select entity_type as type, event, timestamp,entity_id as id, e.organization_id, e.job_id, e.appointment_id, e.customer_id, e.actor_id, e.actor_type, data->>'message' message,data->>'rating' rating, j.external_id job_external_id, j.customer_external_id
from eventbus_events e
left join jobs j on j.id = e.job_id
where e.account_id = 2
and event in ('appointment.canceled','appointment.complete','appointment.enroute','appointment.scheduled','appointment.started', 'appointment.created',
'job.canceled','job.closed','job.complete','job.paused','job.rejected','job.unscheduled','attachment.created','survey_response.submitted',
'job_offer.entity_offered','job_offer.entity_accepted','job_offer.entity_declined',
'estimate.updated','estimate.won','estimate.lost','invoice.updated','invoice.paid','invoice.balance_outstanding','payment.created','attachment.created')
and e.timestamp >= '04/13/2017 16:00:00'
and e.timestamp <= '04/13/2017 18:25:00'
order by timestamp