# KitCode mascot assets

These transparent 512 x 512 WebP assets were created with the built-in
ImageGen workflow and normalized for web playback. `kit-chibi.webp` is Kit's
single cleaned, softly vectorized design throughout the product.

## Production animation sequences

Kit's animation player uses one aligned image at a time. The dense
sequences replace the earlier three-to-five-frame prototypes, so no pose is
made to reverse or morph through CSS.

| Files | Frames | Use |
| --- | ---: | --- |
| `kit-hunt-01.webp` through `kit-hunt-08.webp` | 8 | AI is finding an answer: crouch, launch, arc, reach, dive, then a same-side tail-up search hold |
| `kit-sleep-01.webp` through `kit-sleep-08.webp` | 8 | Inactivity or completed lesson: alert, drowsy, nod, lower, nestle, tuck, and curled sleep |
| `kit-happy-01.webp` through `kit-happy-07.webp` | 7 | Correct answer: anticipation, squash, lift, apex, descent, landing, and proud recovery |
| `kit-surprised.webp` | 1 | Encouraging startle after a script or test error |

The hunt sequence always travels nose-first toward screen-left with the tail on
screen-right. Its final pose uses a tiny continuous search sway instead of a
second mirrored drawing. The sleep sequence deliberately contains no
paw-to-face pose: every frame has one coherent fox and exactly four limbs. The
happy sequence keeps the same front three-quarter orientation from take-off to
landing.

Sleep registration is anatomy-led rather than silhouette-led. All eight poses
use one fixed 360px visible-height box and one shared 484px paw/ground line;
small horizontal offsets stop the changing tail silhouette from recentering
the fox. The builder ignores sub-visible alpha residue before measuring each
pose, which prevents a stray transparent pixel from shrinking the real art.
The final hold uses only a tiny brightness pulse—there is no sleep scaling or
zoom animation.

The settling transition uses `kit-sleep-settle-right.png`: its tail stays
behind Kit on screen-right, continuing the seated tail direction without
mirroring Kit, moving the scarf knot, or sweeping the tail across screen-left.

The correct-answer player adds responsive stage registration to those seven
drawings: a deeper anticipation squash, a 30% upward apex, a small horizontal
arc, an impact overshoot, and a shrinking ground shadow. This motion metadata
is intentionally kept out of the bitmap canvases so the same transparent
assets scale correctly in the rail, coach panel, and Settings preview. The
exact same registration is used by `kit-correct-answer.gif`.

Run `scripts/build_mascot_sequence_assets.py` to rebuild aligned WebP frames
from the lossless masters in `artwork/mascots/source/`. Run
`scripts/render_mascot_previews.py` to rebuild the exact review loops and frame
contact sheets in `artwork/mascots/previews/`.

## ImageGen prompt set

All new source drawings were generated with the built-in ImageGen editor. The
selected Kit illustration was the strict identity and style reference.
The shared prompt was:

```text
Use case: image edit / animation sprite frame
Asset type: transparent web mascot frame
Preserve exactly: the same single Kit red fox, rounded proportions,
orange and warm-cream markings, dark navy hand-drawn contour and paws, fluffy
cream-tipped tail, teal neckerchief, face, and softly vectorized 2D cel finish.
Composition: one complete coherent fox, centered on a square flat #FF00FF
chroma field, generous padding, stable camera, scale and ground line.
Constraints: anatomically correct fox with exactly four legs, only the limbs
that the pose exposes, clean silhouette, no cast shadow, dirt, prey, scenery,
text, logo, watermark, sticker border, photographic fur, glossy 3D treatment,
AI-like microtexture, merged limbs, duplicate paws, or extra anatomy.
```

The frame-specific direction was:

```text
Hunt (8 frames): maintain one left-facing direction throughout. Low alert
crouch; forward lift-off; airborne mousing-pounce arc; nose lowering; forepaws
reaching over the hole; head and shoulders entering; hips and rear legs above
the edge; only the attached rump, rear legs and tail standing up. Tail remains
on screen-right in every beat. Never mirror, turn around, reverse, or swap the
tail side. Real fox photographs are pose-mechanics references only.

Sleep (8 frames): awake seated pose; heavy eyelids; gentle head nod with both
front paws planted; side-sit lowering; settle onto the forelegs; nestle behind
the tail; compact tuck; fully curled sleep with tail wrapped around the body.
Never raise a paw to the face and never imply a fifth leg. Keep the tail on
screen-right throughout the settling transition; never flip or mirror it to
screen-left between frames.

Happy (7 frames): keep one consistent front three-quarter view and tail side.
Eager ready pose; deeper anticipation squash; toe push-off; compact airborne
apex; controlled descent; soft four-paw landing; proud smiling recovery with a
lifted tail. Do not rotate or flip the character between frames.
```

ImageGen supplied flat-magenta source renders. The installed ImageGen helper
converted the chroma field to true alpha with a soft matte and despill. The
normalizer then bottom-aligned, scaled, and WebP-encoded each frame.
