# Validation

The standard-library utility suite covers 17 tests: profile presets, secret-field rejection, explicit publishing approval, no automatic spending, valid frame rates, path traversal and overwrite protection, missing-asset reporting, native template copying, scaffold status, pause mapping boundaries, finite timing values, duplicate/reversed cues, generated output consistency and relative documentation links.

Run locally:

```bash
python -m unittest discover -s tests -v
```

Profile initialization, profile checking, episode scaffolding and retiming were executed locally. The committed retiming output and scaffold receipt come from those utilities. Scaffolding is not rendering.

External renderer execution, collected-project portability, audiovisual inspection and platform publishing have **not** been validated by this public utility test suite. The original creator's private rig, reel, audio and background files are not distributed here. GitHub Actions is configured; local success is not a claim that a hosted CI run has completed.
