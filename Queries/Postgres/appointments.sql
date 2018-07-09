-- find appointments assigned to organization
select c.first_name, c.last_name, j.title, a.id, a.scheduled_at, u.first_name user_first, u.last_name user_last, j.external_id
from appointments a
left join users u on u.id = a.user_id
inner join jobs j on j.id = a.job_id
inner join customers c on c.id = j.customer_id
where a.organization_id = 292317
and a.deleted_at is null
order by a.scheduled_at desc

-- find appointments assigned to user
select c.first_name, c.last_name, j.title, a.id, a.scheduled_at, u.first_name user_first, u.last_name user_last, j.external_id
from appointments a
left join users u on u.id = a.user_id
inner join jobs j on j.id = a.job_id
inner join customers c on c.id = j.customer_id
where a.user_id = 292317
and a.deleted_at is null
order by a.scheduled_at desc