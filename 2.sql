select d.trackingNo, d.pickUpTime, d.dropOffTime,o.address
from deliveries d, orders o
where  	o.cid = 'sss' and
		o.oid = d.oid;
