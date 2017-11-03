select o.oid, o.odate, p.name, l.qty, l.qty*l.uprice from 
orders o, olines l, products p
where o.cid= 'sss' and
o.oid = l.oid and
l.pid = p.pid
order by o.odate DESC;

