# Personalization

1. Copy `neutral.example.json` or `orbit.example.json` using `init_profile.py`.
2. Edit the resulting ignored `config/profile.local.json`. That local file is the active profile; a request-specific approved override may replace a value, but record the effective profile in the episode. Scripts do not silently merge arbitrary nested profiles.
3. Replace studio name, narration language/tone, palette, font file/weights, mascot or `enabled:false`, output format, approved backgrounds, renderer/template locations, sound targets and destinations.
4. Add only non-secret account selectors if needed. Use a secret manager/environment/connection provider for credentials, never the JSON file. No actual creator account IDs are included.
5. Run `check_profile.py`, then inspect reported missing files/tools before production. Validation checks structure and asset availability, not aesthetics or renderer compatibility.

## Original Orbit preset, now an example

The example uses a graphite floating robot, teal accent, Geist 600/500, Hinglish narration, 1080×1920 at 60fps, character-led humor, light teaching scenes and sparse UI ticks. Names such as Vinayak Voxel and sample Black_White filenames illustrate the creator's preset; they are not required identities/files for everyone. The actual approved rig/background files are not bundled. Reuse another user's profile only with their assets and permissions; never claim the repository ships a canonical robot it does not contain.

Default tool examples are EffectCraft and optional Composio. Choose another renderer/provider by editing the profile and verifying capabilities. XeroPC is an example of an optional desktop adapter, not a dependency or a public endpoint. Old local Windows paths, machine manifests, connected-account IDs, Composio skill IDs and real reel recordings were intentionally excluded.

Publishing remains a separate explicit authorization even when a profile lists Instagram/YouTube. An episode destination/visibility should be reviewed before upload. Public examples contain no actual publish receipt.
