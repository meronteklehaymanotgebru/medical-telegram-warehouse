select distinct
    date_day as date_key,
    date_day as full_date,
    extract(dow from date_day) as day_of_week,
    to_char(date_day, 'Day') as day_name,
    extract(week from date_day) as week_of_year,
    extract(month from date_day) as month,
    to_char(date_day, 'Month') as month_name,
    extract(quarter from date_day) as quarter,
    extract(year from date_day) as year,
    case when extract(dow from date_day) in (0,6) then true else false end as is_weekend
from {{ ref('stg_telegram_messages') }}