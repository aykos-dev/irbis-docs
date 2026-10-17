# Brief places-5-irbis-app-fix — review fix: no endless skeleton on permission/cluster errors

- Spec: features/places.md · AC4, AC6 · Repo / branch: irbis-app · `feat/places` (on d5e2405)
- Files: Touch `src/features/places/hooks/useOrigin.ts`, `src/features/places/components/PlacesMap.tsx`,
  `src/app/__tests__/places/explore.test.tsx` (add cases only; don't change existing ones).
- Behaviour:
  - useOrigin (lines ~105-125): if the permission request, the permission check or the fix lookup throws (initial ask
    and the AppState re-check), fall back to `{ status: 'none', permission: 'denied' }` → Tashkent origin + banner
    (AC6), and log `location_permission { result: 'unavailable' }`. Never leave state `pending`.
  - PlacesMap (~79-87,115): if `getClusterExpansionZoom` rejects, zoom the camera in by +2 from the current zoom
    centred on the cluster; no unhandled rejection.
  - Add a test: permission request throws → banner shown, list query runs without coords. Add an Android-platform case
    (`Platform.OS = 'android'`): PermissionsAndroid denied → banner, no coords.
- Approved packages: none.
- Done when: `npm run check` green, one commit `fix(places): fall back to Tashkent when location calls fail`,
  reply ≤5 lines.
