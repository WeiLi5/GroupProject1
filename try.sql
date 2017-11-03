
select  r2.sid,r2.name,r2.phone,r2.address,r1.uprice,r1.qty,ifnull(r3.num_orders,0) from
(
select *
from carries
where pid = '234576'
order by
case when qty = 0 then uprice end,
case when qty > 0 then uprice end
)as r1
left outer join
(
	select *
	from stores
)as r2
on r2.sid = r1.sid
left outer join
(
	select sid,count(*) as num_orders
	from orders o, olines l
	where odate > datetime('now','-7 days') and
	      l.pid = '234576' and
	       o.oid = l.oid
	group by l.sid
) as r3
on r2.sid = r3.sid

;
