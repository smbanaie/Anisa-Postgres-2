```sql
select 
  	r.region_id ,
	r.region_description , 
	count(distinct  et.employee_id) as "Number od Employees"
from
	region r inner join territories t ON r.region_id = t.region_id  
	inner  join employee_territories et on et.territory_id = t.territory_id 
group by 
	1,2 
order by 3 desc 

select *
from employees e
where e.employee_id  not in (select employee_id from employee_territories et)

select *
from 
(
select 
	extract(year from o.order_date) as "Year" , 
	e.employee_id,
	e.first_name ,
	e.last_name ,
	count(*) as "Number Of Orders", 
	dense_rank() over(partition by extract(year from o.order_date)  order by count(*) desc) as "Rank"
from 
	employees e  left outer join  orders o on e.employee_id  = o.employee_id 
group  by 
	1,2,3,4
order by 
	1 asc , 5 desc
)
where "Rank" < 4


with order_volume as (
select 
	order_id , 
	sum (od.quantity * (1- od.discount) * od.unit_price ) as "order volume"
from 
	order_details od
group by od.order_id 
) 
select 
	extract(year from o.order_date) as "Year",
	o.employee_id ,
	sum(ov."order volume") as "Total Order volume"
from 
	orders o natural join order_volume ov
group by 1,2
order by 1, 3 desc 


with product_sales_monthly_rank_97 as(
select 
	extract(month from o.order_date) as "Month"
	, od.product_id 
	, sum(od.quantity) as "Sales Count"
	, dense_rank() over(partition by extract(month from o.order_date) order by sum(od.quantity) desc ) as "Rank"
from 
	orders o inner join order_details od ON od.order_id = o.order_id 
where 
	extract (year from o.order_date) = 1997
group by 
	1,2
order by 
	1, 3 desc 
), monthly_top_products as (
select *
from 
	product_sales_monthly_rank_97
where 
	"Rank" < 4
)
select 
	"Month"
	, p.product_name
	, "Sales Count"
from 
	products p natural join monthly_top_products 
order by 1, 3 desc



create view low_in_stock 
as (
select 
	product_id 
	, p.product_name 
	, p.units_in_stock 
	, p.reorder_level 
	, s.company_name 
	, s.contact_name 
	, s.country 
	, s.city 
from 
	products p join suppliers s on p.supplier_id  = s.supplier_id 
where 
	p.units_in_stock <= p.reorder_level 
order by 
	p.units_in_stock/nullif(p.reorder_level,0)  asc 
)


with Monthly_Diary_Sales_Volume as (
select 
	extract (month from o.order_date) as "Month"
	,   sum(
			case 
				when c.category_id = 4 then od.quantity* (1 - od.discount  ) * od.unit_price else 0 
			end  
			) as "Diary Monthly Sales Volume"
    ,   sum(
			case 
				when c.category_id = 6 then od.quantity* (1 - od.discount  ) * od.unit_price else 0 
			end  
			) as "Meat Monthly Sales Volume"
from 
	categories c join products p on c.category_id = p.category_id 
	join order_details od on od.product_id = p.product_id 
	join orders o  on o.order_id = od.order_id 
where 
	c.category_id in (4,6)
	and extract (year from o.order_date) = 1997
group by 1
order by 1
)
select 
	"Month"
	, "Diary Monthly Sales Volume"
	, "Diary Monthly Sales Volume" / lag("Diary Monthly Sales Volume") over(order by "Month") as "Diary Growth"
	, sum("Diary Monthly Sales Volume") over(order by "Month")   as "Diary Running Total"
	, avg("Diary Monthly Sales Volume") over(order by "Month" rows between 1 preceding and 1 following) as "3 Month Moving Average"
--	, sum("Meat Monthly Sales Volume") over(order by "Month")   as "Meat Running Total"
from 
	Monthly_Diary_Sales_Volume
order by 
	"Month"












)
select 
	tmp."Year", first_name, last_name, "Rank", "Number Of Orders", "Total Order volume"
from 
(
select 
	extract(year from o.order_date) as "Year" , 
	e.employee_id,
	e.first_name ,
	e.last_name ,
	count(*) as "Number Of Orders", 
	dense_rank() over(partition by extract(year from o.order_date)  order by count(*) desc) as "Rank"
from 
	employees e  left outer join  orders o on e.employee_id  = o.employee_id  
group  by 
	1,2,3,4
order by 
	1 asc , 5 desc
) 
as tmp inner join year_order_volume yov on tmp.employee_id=yov.employee_id and tmp."Year" = yov."Year"
--as tmp inner join year_order_volume yov using(employee_id, "Year")
where "Rank" < 4








```

