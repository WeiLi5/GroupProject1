select s.sid, s.name, p.pid, p.name, l.qty, p.unit, l.uprice
from stores s, products p, olines l, orders o
where o.oid=101 and
	o.oid =l.oid and
	l.sid=s.sid and
	l.pid=p.pid;