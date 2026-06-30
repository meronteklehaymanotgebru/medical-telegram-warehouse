select
    m.message_id,
    m.channel_key,
    m.date_key,
    y.detected_class,
    y.confidence,
    y.image_category
from {{ ref('fct_messages') }} m
join raw.yolo_results y on m.message_id = y.message_id