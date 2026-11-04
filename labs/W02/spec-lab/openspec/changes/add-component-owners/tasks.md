# Tasks: add-component-owners

## 1. Ownership table
- [ ] 1.1 Create `config/owners.toml` for the three dataset repositories
- [ ] 1.2 Load it in `router.py`

## 2. Routing
- [ ] 2.1 Look up the owner of `record.component`; build `eng-<team>`
- [ ] 2.2 Fall back to `engineering` when there is no owner
- [ ] 2.3 Tests: owned component, unowned component, `component = null`
