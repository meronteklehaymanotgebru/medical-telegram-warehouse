select
    row_number() over (order by channel_name) as channel_key,
    channel_name,
    count(*) as total_posts,
    min(date) as first_post_date,
    max(date) as last_post_date,
    avg(views) as avg_views
from {{ ref('stg_telegram_messages') }}
group by channel_name