# itconverts

Karo Convert

## Toolchain
Node **v22.23.2** (system, LTS). Project requires: `unpinned`


## Commands
```bash
npm install
npm run dev      # check package.json scripts for the real names
npm test
```
npm cache is redirected to `/mnt/games2/devcache/npm`. `node_modules/` is regenerable — wipe with `dev clean itconverts`.

## Repo conventions
- Line endings are normalized to LF via `.gitattributes` (these files originated on Windows).
- Managed with the `dev` command: `dev ls`, `dev doctor`, `dev clean itconverts`, `dev rm itconverts`.
