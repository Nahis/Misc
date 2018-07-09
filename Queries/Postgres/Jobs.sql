select * from jobs
where source_id = 1


update Contractor_API 
set Dispatch_Address_ID = null, Dispatch_Org_ID = null, Dispatch_Provisioned_Flag = null, Dispatch_User_ID = null, process_status = 'P'
where service_provider_id       = 'MAV001'                            
