with source as (
    select * from {{ source('raw', 'telegram_messages') }}
),

cleaned as (
    select
        message_id,
        channel_name,
        date,
        text,
        has_media,
        coalesce(views, 0) as views,
        coalesce(forwards, 0) as forwards,
        image_path,
        length(text) as message_length,
        date::date as date_day
    from source
    where text is not null and text != ''
)

select * from cleaned