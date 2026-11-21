-- A named job is updated rather than duplicated when this script is reapplied.
create extension if not exists pg_cron;
select cron.schedule('jaynova-data-retention', '15 4 * * *', $job$
  delete from jaynova_private.download_rate_limits where hour_bucket < now() - interval '24 hours';
  delete from jaynova_private.daily_downloads where day < current_date - 365;
$job$);
