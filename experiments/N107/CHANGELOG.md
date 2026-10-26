# N107 changelog

- Imported the exact N106 parser and guarded compiler and kept the source N100 archive unmodified.
- Added five context-free topological options with multi-click translation targets.
- Implemented time-aware SMDP backups over *actually executed* options, separate per-option global transfer priors, and safe rejection of invalid zero-duration proposals.
- Adapted the original B1 staging/observation interfaces so native rewards still update frozen B1 Bellman estimates while the meta table survives level transition.
- Fixed a synthetic Level-2 palette/object-enumeration bug by selecting the smaller movable object by role rather than palette ID.
- Optimized strict compiler analysis by skipping impossible proposal generation when no trusted rule exists and skipping already disqualified native action identities; no change to the underlying N106 trust criterion.
- Completed the final-code 10-family native matched A/B; obtained **zero native options / zero native meta updates**, the same 9 Level-1, 1 Level-2 completions, and identical 1,116 charged SDK actions per arm.
- Replayed the ten unique native family traces through a fresh SDK with exact observations/rewards/action parity (1,116/1,116).
- Added a fully separate two-level synthetic transfer test demonstrating four-step options and discounted level-persistent Q updates when a calibrated native action model is supplied.
- Frozen submission files remain unchanged and were not replaced with this non-improving experiment.