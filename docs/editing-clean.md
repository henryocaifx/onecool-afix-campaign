# Final clean-master edit

The user's latest direction is: **“the videos should be with out title/subtitle/text box.”** All added typography, trailer title graphics, subtitles, text boxes, product UI panels, campaign identification graphics, logos, and closing text cards are omitted from the delivered videos. Earlier branded drafts are superseded. Product identification remains in the filenames, package, and container metadata rather than over the images.

`python scripts/finish.py` reproduces the final clean masters:

- Trim each accepted native source to its first 27.000 seconds.
- Retiming: `setpts=(PTS-STARTPTS)/0.9`; normalize to 24 fps, 720 frames, exactly 30.000 seconds. Source frames are retained without synthetic motion interpolation.
- Audio: pitch-preserving `atempo=0.9`, source stereo channels preserved, 48 kHz resampling, short start/end fades, normalization toward −16 LUFS and −1.5 dBTP.
- Lanczos scale from actual 2206 × 946 source to cover 2520 × 1080, with minimal centered crop and square pixels.
- H.264 yuv420p, CRF 18, AAC stereo 256 kb/s, fast-start MP4.
- No burned-in titles, subtitles, graphics, boxes, branding, UI, or end cards. No subtitle track is muxed. Fictional papers, drawings, maps, and screen props already present in the scenes remain part of the cinematography.
- Final thumbnails are clean full-resolution extracted frames, without poster typography.

Use the per-film command vectors and technical verification records to reproduce and verify the exact exports. `docs/scripts.md` records the original pre-generation creative scripts. `docs/scripts-clean.md` records the final text-free timeline specification.
