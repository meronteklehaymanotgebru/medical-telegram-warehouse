select
    m.message_id,
    d.channel_key,
    dt.date_key,
    m.text as message_text,
    m.message_length,
    m.views,
    m.forwards,
    m.has_media
from {{ ref('stg_telegram_messages') }} m
left join {{ ref('dim_channels') }} d on m.channel_name = d.channel_name
left join {{ ref('dim_dates') }} dt on m.date_day = dt.date_key