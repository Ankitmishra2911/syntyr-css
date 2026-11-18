# Syntyr Go Resource Workbench

A runnable **server-rendered** enterprise resource workspace demonstrating how to compose existing Syntyr CSS classes without a frontend runtime. The records are fictional and held in a fixed in-memory slice.

## Run

Requires Go 1.24 or newer. From this directory:

```sh
go test ./...
go run . -addr 127.0.0.1:8767
```

Open http://127.0.0.1:8767/resources. The demo serves the repository's already-built CSS from `../../dist`. Run from `examples/go-resource-workbench/`; if your CSS is elsewhere, pass `-dist /absolute/path/to/dist`.

## Working behaviors

- Native GET search over resource name, ID, owner and region; status filtering; explicit name or updated-date sort.
- Column visibility controls (Owner and Region) stored in URL query parameters; resource ID, status and update date remain visible.
- Studio, Grid and Noir tokens selected via a GET control, preserved in inspector and selection-preview links.
- Per-resource detail links that retain current search, column and theme preferences; an inspector never shows a record excluded by the current filter.
- Checked-row bulk **preview** via a native GET form; the server validates IDs, removes duplicates and intersects the choices with the current filters.
- Explicit "Preview all matching" link using server-filtered results. It does **not** infer select-all from an empty checkbox form.
- Empty-results and empty-selection screens. Input validation, output escaping, method checks and no-store response headers.

This is a self-contained example, not a new Syntyr CSS component or a full backend. No authentication, tenant isolation, CRUD writes, audit persistence, pagination, virtualization, export or database connections are included. **Do not deploy it as a live multi-tenant business application.** Integrating real data requires server-side tenant/RBAC checks, stable query scope, per-record authorization, CSRF protection for mutations, transaction semantics and audit logs.

The `/preview` endpoint only describes a proposed selection. It never changes records. Large paginated selections need a server-owned query snapshot or select-all-except contract; unchecked IDs on unloaded pages cannot be inferred from checkboxes.

## Composition map

| Concern | Syntyr presentation |
| --- | --- |
| Workspace and responsive inspector | `syn-workspace`, `syn-detail-layout`, `syn-detail-main`, `syn-detail-aside` |
| Search/filter/sort/theme controls | `syn-filter-bar`, `syn-filter-field`, `syn-filter-actions` |
| Results and bulk previews | `syn-table`, `syn-table-wrap`, `syn-bulk-actions`, `syn-result-state` |
| Inspector metadata | `syn-record-fields`, `syn-surface--raised` |
| Themes and density | `data-syn-theme`, `data-syn-density` |

The Go application owns every query, state and link. Syntyr CSS only presents them. The same HTML can be adapted to other SSR frameworks.
