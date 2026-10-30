# Native adapter: EffectCraft example

These are historical command shapes from the original production workflow. Verify your installed executable's help/schema and test a small comp before production. No EffectCraft binary/license or `.ecproj` library is included.

```text
EFFECTCRAFT script script.jsx --project source.ecproj --save-as result.ecproj --json
EFFECTCRAFT render-frame --project result.ecproj --comp COMP --time 3.2 --max-side 1280 --out proof.png --json
EFFECTCRAFT render --project result.ecproj --comp COMP --out draft.mp4 --format h264 --fps 30 --resolution half --audio on --json
EFFECTCRAFT render --project result.ecproj --comp COMP --out chunk.mp4 --format h264 --fps 60 --resolution full --audio off --start START --end END --json
```

Native example patterns, not promises about other editors:

```javascript
var t = layer.property('ADBE Transform Group');
t.property('ADBE Position').setValue([540,875,0]);
var d = new TextDocument('Explain one idea');
d.font='Geist'; d.fontStyle='SemiBold'; d.__set('variations',{wght:600});
layer.property('ADBE Text Properties').property('ADBE Text Document').setValue(d);
__call('layer.timing',{comp:comp.id,layers:[layer.id],start:0,'in':startSeconds,out:endSeconds});
```

Substitute the active profile's font/weight/geometry. Use atomic layer timing; separate start/in/out mutations previously produced clamping/ghost poses. Preserve parent anchors and the rig's source coordinate system; scale the precomp, not each limb. Global-time expressions and source-local expressions need deliberate clocks. Changing only `inPoint` does not retime hard-coded expression anchors.

Check return code AND JSON `ok`. A failed script may save a partial project; restart from known-good input or use a verified idempotent edit. Reuse validated chunks only. Use native dependency collection if supported, inspect its errors, reopen and render a proof. Same-machine success does not prove a clean installation with missing fonts.

Original kit examples include HYPE/POINT/SHRUG/PHONE/REFUSAL/LASER/TYPE/VICTORY poses and hero/teaching/dialogue/CTA/text/flash comps. REFUSAL denotes a surprised expression, not behavioral instructions. Resolve names from your actual supplied catalog; do not assume the original creator's comp IDs, 800×480 rig or eight-second templates exist.

If using another renderer, document the corresponding verified operations, editable format, timing semantics, render/QC path and portability limits. Do not relabel a flattened MP4 as an editable native project.
