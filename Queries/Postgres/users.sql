-- find users
select id, email,mobile, first_name, last_name, is_tech, is_dispatcher
from users
where organization_id = 292317
and deleted_at is null
order by first_name