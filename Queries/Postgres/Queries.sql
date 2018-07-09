-- find users updating appointments
select a.id, a.status, a.updated_at, upd.email updated_by, cre.email created_by, j.id job_id, a.created_at
from appointments a 
inner join jobs j on j.id = a.job_id
inner join users upd on upd.uid =substr(a.updated_by,6,100) 
inner join users cre on cre.uid =substr(a.updated_by,6,100)
where j.organization_id = 1740
and left(a.updated_by,4) = 'user'
order by a.created_at desc

-- find users updating jobs
select j.id, j.status, j.updated_at, upd.email updated_by, cre.email created_by, j.created_at
from jobs j 
left join users upd on upd.uid =substr(j.updated_by,6,100) 
left join users cre on cre.uid =substr(j.updated_by,6,100)
where j.organization_id = 1740
and left(j.updated_by,4) = 'user'
order by j.created_at desc

-- unscheduled jobs without open appointments
select j.*
from jobs j
left join 
	(select cnt,status,job_id from
		(select count(*) cnt, a.status, a.job_id
		 from appointments a
		 inner join jobs j on a.job_id = j.id
		 where j.source_id = 2
		 group by a.status, a.job_id) a
	 where status not in ('canceled','complete')) b
	 on j.id = b.job_id
where  j.source_id = 2
and j.status not in ('complete','canceled')
and b.status is null

-- Job By title
select j.id,a.id appointment_id, j.status, j.title,j.created_at,j.source, o.NAME, a.created_at,  u.full_name assigned_to 
from jobs j
left join appointments a on a.job_id = j.id
left join organizations o on o.id = j.organization_id  
left join users u on u.id = a.user_id
where j.title like '%000801380/001%'
and j.source = 'homeserve';

-- Job By Id
select j.id job_id, a.id appointment_id, j.status job_status, j.title,j.created_at job_created,j.source, o.NAME, a.created_at appointment_created, u.full_name assigned_to 
from jobs j
left join appointments a on a.job_id = j.id
left join organizations o on o.id = j.organization_id  
left join users u on u.id = a.user_id
where j.id = 17095
and j.source = 'homeserve';

-- Events
select u.full_name assigned_to, e.*
from events e
inner join jobs j on j.id = e.event_entity_id
left join users u on u.id = e.creator_id
where j.id = 17095
and event in ('appointment.canceled','appointment.complete','appointment.enroute','appointment.paused','appointment.scheduled','appointment.started','comment','job.rejected','job.unscheduled','appointment.created')
order by e.id;

-- Appointments
select a.status AppointmentStatus, j.status JobStatus
from appointments a
inner join jobs j on j.id = a.job_id
where j.source = 'hc';

-- users
select first_name, last_name, phone_number, email
from users
where id = 957


-- job stats between 2 dates
select count(*) CountJobs, j.source, o.name
from jobs j
left join organizations o on o.id = j.organization_id 
where j.status in ('complete','closed')
and j.created_at between LOCALTIMESTAMP - INTERVAL '7 days' and localtimestamp
group by j.source, o.name
order by j.source, o.name


-- check duplicates
select distinct u.email, first_name, last_name, o.id org_id, o.name org_name, a.account_id
from users u
inner join organizations o on o.id = u.organization_id
left join account_organizations a on a.organization_id = o.id 
where u.email in ('acplusllc@yahoo.com','upayless@bellsouth.net','advanced9244186@aol.com','bassplumbing10@gmail.com','info@rivercityheatingair.com')

select distinct u.phone_number, first_name, last_name, o.id org_id, o.name org_name, a.account_id, a2.name
from users u
inner join organizations o on o.id = u.organization_id
left join account_organizations a on a.organization_id = o.id
left join accounts a2 on a2.id = a.account_id 
where u.phone_number in ('17177625988','+15712201438','+15717488422','+16155574255','+17036408609')


-- removed from xplenty label mapping
delete from job_labels 
where link_id in (
select jl.link_id
from job_labels jl
left join  rep_label_links rll on jl.link_id = rll.id
where rll.id is null)