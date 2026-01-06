-- 1️⃣ Recruiters table (linked to auth.users)
create table if not exists recruiters (
  id uuid primary key references auth.users(id) on delete cascade,
  email text unique not null,
  created_at timestamp default now()
);

-- 2️⃣ Update jobs table to enforce recruiter ownership
alter table jobs
add column if not exists recruiter_id uuid references recruiters(id);

-- 3️⃣ Enable RLS
alter table recruiters enable row level security;
alter table jobs enable row level security;

-- 4️⃣ Recruiter can read own profile
create policy "Recruiter can view own profile"
on recruiters
for select
using (auth.uid() = id);

-- 5️⃣ Recruiter can insert own profile
create policy "Recruiter can insert own profile"
on recruiters
for insert
with check (auth.uid() = id);

-- 6️⃣ Recruiter can CRUD own jobs
create policy "Recruiter can manage own jobs"
on jobs
for all
using (auth.uid() = recruiter_id)
with check (auth.uid() = recruiter_id);
