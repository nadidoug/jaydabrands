-- Isolated JayNova download counters. No email, name, raw IP, or user agent.
create schema if not exists jaynova_private;
revoke all on schema jaynova_private from public, anon, authenticated;
grant usage on schema jaynova_private to service_role;

create table if not exists jaynova_private.daily_downloads (
  day date not null,
  product_slug text not null check (product_slug = 'starter-guide'),
  downloads integer not null default 0 check (downloads >= 0),
  primary key (day, product_slug)
);
create table if not exists jaynova_private.download_rate_limits (
  visitor_hash text not null check (visitor_hash ~ '^[0-9a-f]{64}$'),
  hour_bucket timestamptz not null,
  requests integer not null default 1 check (requests between 1 and 15),
  primary key (visitor_hash, hour_bucket)
);
alter table jaynova_private.daily_downloads enable row level security;
alter table jaynova_private.download_rate_limits enable row level security;
revoke all on all tables in schema jaynova_private from public, anon, authenticated;
grant select, insert, update, delete on all tables in schema jaynova_private to service_role;

create or replace function public.jaynova_record_download(
  p_product_slug text, p_visitor_hash text, p_consent_version text
) returns boolean
language plpgsql security invoker set search_path = '' as $$
declare
  accepted integer;
  current_hour timestamptz := date_trunc('hour', now());
begin
  if p_product_slug is distinct from 'starter-guide'
     or p_consent_version is distinct from '2026-11-21'
     or p_visitor_hash is null or p_visitor_hash !~ '^[0-9a-f]{64}$' then
    raise exception 'Invalid download event' using errcode = '22023';
  end if;
  delete from jaynova_private.download_rate_limits where hour_bucket < now() - interval '24 hours';
  delete from jaynova_private.daily_downloads where day < current_date - 365;
  insert into jaynova_private.download_rate_limits(visitor_hash, hour_bucket, requests)
    values (p_visitor_hash, current_hour, 1)
    on conflict (visitor_hash, hour_bucket) do update
      set requests = jaynova_private.download_rate_limits.requests + 1
      where jaynova_private.download_rate_limits.requests < 15
    returning requests into accepted;
  if accepted is null then return false; end if;
  insert into jaynova_private.daily_downloads(day, product_slug, downloads)
    values (current_date, p_product_slug, 1)
    on conflict (day, product_slug) do update
      set downloads = jaynova_private.daily_downloads.downloads + 1;
  return true;
end;
$$;
revoke all on function public.jaynova_record_download(text, text, text) from public, anon, authenticated;
grant execute on function public.jaynova_record_download(text, text, text) to service_role;
