---
name: dbt-developer
description: Write, review and refactor dbt models. Use when adding or changing a model, choosing a layer, defining a surrogate key, grain, tests or masking, reconciling several sources into one business entity, or asking about staging/core/analytics conventions, technical columns, snapshots or materialisation.
---

# dbt Developer

A dbt project builds into a SQL warehouse (Snowflake, Postgres, BigQuery, …).
This skill covers writing a model that conforms to common layered conventions,
and recognising one that does not. Adapt the specifics (schemas, macros, ADR
numbers) to your platform.

## Layers

Five layers. A model belongs to exactly one, and reads only the layer below it.

| Layer | Job | Typical schema |
|---|---|---|
| Raw | Land data untouched. Read with `source()` | `raw` / `landing` |
| Staging | Technical normalisation, source-aligned | `<domain>_staging` |
| Core | Reconciled business model, relational | `<domain>_core` |
| Analytics | Consumption models, shared and per-consumer | `<domain>_analytics` |
| Semantic | Governed metrics (often not built yet) | — |

Never skip a layer. A shared Analytics model never reads a consumer model.

## Non-negotiable rules (adapt ADR numbers to your repo)

1. **Table names are plural.** `sales`, not `sale`.
2. **`_at` is a technical date, everything else is functional.** `ingested_at`,
   `created_at`, `updated_at` are platform events. Business times take
   `_timestamp` / `_date` / another unit: `order_timestamp`, `modification_date`.
3. **Surrogate keys use `generate_surrogate_key`** (dbt-utils), never MD5, never
   a sequence. The namespace in `dbt_project.yml` must never change.
4. **Declare the grain and test it.** A description sentence plus
   `dbt_utils.unique_combination_of_columns` over those columns. A `unique` test on
   the surrogate key does not test the grain.
5. **One YAML file per model**, beside the `.sql`.
6. **No `dim_` / `fct_` in Core.** Core is relational; dimensional prefixes belong
   in Analytics.
7. **`table` by default in Core.** `incremental` needs a volume justification
   (roughly a million rows, or a refresh over thirty seconds).
8. **Comments explain the code.** No measured row counts in comments; those go in
   the test record.
9. **A test that only code can fail is a unit test.** Ask whether any input data
   could make it fail without touching the SQL. If not, it is a unit test under
   `unit_tests:`, run in CI and disabled on scheduled targets. Keys, grain,
   `not_null` on sourced columns and referential integrity stay data tests, which
   gate the scheduled `dbt build`.

## Model skeleton

Every Core model follows the same four-part shape.

```sql
{{ config(materialized='table', tags=['<domain>', 'core']) }}

/*
  <model name>
  Grain   : one row per <what>
  Sources : ref('<staging model>'), ref('<staging model>')
  Rules   : <business logic in one or two lines>
*/

WITH source_a AS (          -- 1. Sources: one CTE per ref, nothing else
    SELECT * FROM {{ ref('...') }}
),

cleaned AS (                -- 2. Transformations: casts, CASE, COALESCE,
    ...                     --    joins, dedup, computed columns — all of it
),

renamed AS (                -- 3. Renamed: bare columns and macro calls only.
    SELECT                  --    NO logic here.
        cleaned.code,
        {{ generate_surrogate_key(['code'], var('ns_<domain>')) }} AS id,
        {{ technical_fields_core(['cleaned']) }}
    FROM cleaned
)

SELECT ... FROM renamed     -- 4. Final SELECT: column order, incremental guard
```

Two rules people get wrong:

- **`renamed` contains no transformations.** If you write `::TYPE`, `COALESCE`,
  `CASE` or `DATE_TRUNC` there, it belongs in a prior CTE.
- **Macro arguments are bare column names or table aliases, never expressions.**
  `generate_surrogate_key([UPPER(code)], ...)` is forbidden — compute `UPPER(code)`
  in a prior CTE and reference the result.

## Column order

Brand first (if applicable), then keys in clear, then business attributes, then
technical fields. Every variable input to a surrogate key is projected as a
column, or the key cannot be recomputed.

## Technical columns

Added by macro, never by hand. Adapt macro names to your platform.

| Layer | Macro (example) | Emits |
|---|---|---|
| Staging | `technical_fields_staging(source, tool)` | `source`, `created_at`, `updated_at` |
| Core | `technical_fields_core([tables])` | `sources` (array), `created_at`, `updated_at` |
| Analytics | `technical_fields_analytics([tables])` | `sources` (array), `created_at`, `updated_at` |

`created_at` is the **first** ingestion of a row, `updated_at` the **latest**.
Core and Analytics aggregate the sources they were built from into an array.

## Brands

Brands share tables, distinguished by a `brand` column. Brand belongs in the
declared grain wherever it is part of the key, and therefore in the grain test.
Never put a brand in a model name — exceptions: a source genuinely per brand, and
an export to a per-brand destination.

## Personal data

A model carrying identifying columns declares its own masking; masking is **per
model, not inherited down lineage**. Add a `post_hook` calling your masking
macro with each column and its type. Only the roles that may unmask should hold
the policy.

## References (optional)

Add `references/` files for layer-specific patterns (staging, core, analytics),
conventions, macros and testing ladder, following the `skill-creator` conventions.
