#!/usr/bin/env python3
"""Record ten distinct campaign treatments; no provider calls or video editing."""
import hashlib
import json
from pathlib import Path
import shutil

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'promo-ten-20261015'
for d in ['records','docs','assets/brand','sources','scripts','posters','review','tmp']:(ROOT/d).mkdir(parents=True,exist_ok=True)
logo=REPO/'native-campaign-20261015/assets/brand/onecool-logo.png'
shutil.copyfile(logo,ROOT/'assets/brand/onecool-logo.png')
shutil.copyfile(REPO/'native-campaign-20261015/records/brand-source.json',ROOT/'records/brand-source.json')

concepts=[
{
 'id':'09-the-snack-sized-blockbuster','title':'The Snack-Sized Blockbuster','style':'Photoreal macro adventure comedy',
 'cast':'A tiny adult East Asian woman director with a yellow rain jacket, dark bob and a miniature camera crew of human adults in cobalt workwear. Their scale stays thumb-sized throughout.',
 'world':'An ordinary kitchen becomes a spectacular practical movie set from a thumb-sized human viewpoint: enormous lemon rind cliffs, a stainless spoon bridge, translucent soda waterfalls, warm amber morning light. Convincing macro depth, tactile food textures, tiny humans with real faces.',
 'beats':[
 '0–3s hook: a giant popcorn kernel erupts beside the tiny director like a harmless white volcano; she ducks, then peers out delighted, low wide macro camera traveling with her.',
 '3–8s: she opens a small black equipment case bearing the supplied ONECOOL AIFX mark, takes a miniature cinema camera and signals her two-person crew toward a teaspoon bridging a cereal bowl.',
 '8–14s: tracking chase across the spoon as a rolling blueberry passes behind; camera swings under the bridge to a dizzying cereal-milk canyon, then follows the crew sliding safely down a curling lemon peel.',
 '14–20s: a soda bubble lifts their little camera platform; they steady it together and discover the entire tabletop from above, grinning as a simple snack becomes an epic location.',
 '20–27s: enormous cinematic push through a curtain of sparkling soda droplets into a sunset-lit popcorn landscape; tiny director frames the perfect shot while two crew members unfurl a silver reflector like a sail.',
 '27–30s: pull all the way back to an ordinary human-sized kitchen table; the tiny crew celebrates atop the black logo case, then one last popcorn puff gently knocks the director’s yellow hat sideways. End on the live comic reaction.'
 ],'audio':'Playful original orchestral adventure with pizzicato strings, triumphant miniature brass, huge popcorn pops, spoon pings, soda fizz and a light final comedy accent.'
},
{
 'id':'10-the-paper-street-parade','title':'The Paper Street Parade','style':'Handcrafted cut-paper stop-motion musical',
 'cast':'A cheerful original adult woman film director made from layered coral and cream paper, round human face, navy cropped hair and an indigo coat. Supporting people are adult HUMAN paper figures with expressive faces; never animal designs.',
 'world':'A tactile handmade pop-up city, visible paper fibers and folded edges, coral/indigo/saffron palette, warm tabletop theatre lighting. Elaborate handmade stop-motion animation with smooth camera movement, not a slideshow or a drawing being revealed.',
 'beats':[
 '0–3s hook: a flat paper pavement suddenly folds into stairs under the director’s feet; she bounds up with an astonished grin as a whole street pops open around her.',
 '3–8s: a black paper equipment case with the supplied gold ONECOOL AIFX mark opens to reveal a tiny camera; she lifts it, and a friend flips a blank folded sheet into a wonderfully absurd spiral street.',
 '8–14s: a joyful human street parade dances along the spiral; paper bicycles and a tiny red tram glide past, balconies accordion outward in rhythm and the camera tracks through layered paper depth.',
 '14–20s: the street runs out at a blank tabletop edge. Director and human friends hold hands and fold the pavement together into a huge curved bridge, solving the interruption through playful teamwork.',
 '20–27s: a continuous swooping camera crosses their bridge into an entire paper city blooming outward in intricate mechanical folds, human dancers tiny beneath beautiful radial skyscrapers, confetti made of pure blank color.',
 '27–30s: return to the director filming the parade beside the physical logo case; a little paper step folds under her, she does one accidental dance shuffle, regains her pose and laughs. Finish inside the animated world.'
 ],'audio':'Original joyous marimba, handclaps, brushed percussion and small brass-band melody; crisp paper folds and rhythmic foot taps timed to the animation.'
},
{
 'id':'11-the-corridor-that-danced','title':'The Corridor That Danced','style':'One-take live-action dance spectacle',
 'cast':'An original adult Black male location scout with close-cropped hair, cream suit, magenta sneakers and a small cinema camera; six adult human dancers in saturated monochrome outfits. Stylish athletic choreography, warm expressive faces.',
 'world':'An impossibly long boutique-hotel corridor with cherry wood, jade velvet and amber practical lamps. Photoreal live action, elegant 28mm moving camera, reflections carefully motivated. A single apparently continuous traveling shot with no title inserts.',
 'beats':[
 '0–3s hook: scout taps a magenta sneaker on the floor; every lamp snaps on in a perfect rhythmic ripple and he raises an eyebrow toward camera.',
 '3–8s: camera circles him beside a luggage trolley with a black ONECOOL AIFX equipment case; he takes his camera, begins a relaxed tap step and a human dancer slides out of a doorway to answer him.',
 '8–14s: camera glides backward as more human dancers join in precise playful call-and-response; the hallway’s decorative wall panels swing into shallow geometric wings synchronized to their footwork.',
 '14–20s: the floor seems to roll sideways like a gentle giant drum while everyone dances through the shifting perspective, playful and safe, architecture moving around coherent human bodies rather than distorted limbs.',
 '20–27s: camera passes through a turning doorway into a huge sunlit courtyard where the corridor has unfolded into a circular dance stage; the scout captures the ensemble’s exuberant synchronized final phrase.',
 '27–30s: push back toward his proud close-up; he tries a tiny final toe tap, one wall lamp does a cheeky late flicker, he smiles and catches the trolley rolling into frame. The real logo case is visible on it; finish on moving performance.'
 ],'audio':'Original infectious funk-jazz instrumental, syncopated bass and brass, clean tap-shoe percussion and coordinated handclaps, with one witty late percussion tick at the final lamp.'
},
{
 'id':'12-the-clay-set-catastrophe','title':'The Clay Set Catastrophe','style':'Premium claymation production comedy',
 'cast':'Three charming original adult HUMAN clay filmmakers: a woman director with purple bob and mustard dungarees, a tall human lighting technician in teal and a short human camera operator in burgundy. Visible clay fingerprints, rounded human noses and hands, no animal characters.',
 'world':'A lavish miniature clay film studio with a deliberately handmade lunar landscape, chunky practical lights and pastel blue cyclorama. Distinct high-end clay animation, tactile soft plasticine material, expressive character acting, smoothly animated cinematography.',
 'beats':[
 '0–3s hook: the director proudly points at a perfect clay moon, which immediately squashes into a pancake with a soft plop; the crew stares at it.',
 '3–8s: she opens a black clay camera case with the supplied gold ONECOOL AIFX logo, sets a little cinema camera and studies the flattened moon; a thoughtful eyebrow lifts, then she grins.',
 '8–14s: rapid satisfying human teamwork: technician bends a light into a sunshine arc, operator rolls the moon pancake into a curling ramp, director pushes tiny clay mountains into place, all actions clearly hand-crafted.',
 '14–20s: their original mistake becomes an ingenious circular moon racetrack; a miniature camera dolly swoops around the ramp and the three humans scramble aboard it, gleefully surfing their own set.',
 '20–27s: spectacular orbiting reveal of a whole whimsical clay planet made from the studio set, camera track wrapping around mountains and pastel cloud rings, the three tiny HUMAN filmmakers waving and filming together.',
 '27–30s: director poses proudly beside the real physical logo case; a pea-sized clay moon drops onto her purple hair with a gentle plop, she looks up cross-eyed and laughs with the crew. End with animated character motion.'
 ],'audio':'Original bouncy tuba, mallet percussion and pizzicato score, tactile clay squishes, wooden dolly rattles and a precisely timed soft final plop.'
},
{
 'id':'13-the-neon-lens-run','title':'The Neon Lens Run','style':'Immersive cyberpunk courier ride',
 'cast':'An original adult Southeast Asian woman camera courier with silver cropped hair, electric-blue windbreaker and coral helmet; human film crew waiting on an enormous rooftop production set. Expressive confident human faces, no masked monsters.',
 'world':'A rain-wet futuristic city at violet night, enormous clean geometric towers, luminous color with NO readable billboards. Photoreal cinema, practical camera vibration, flowing first-person-to-third-person transitions, exciting playful action without violence.',
 'beats':[
 '0–3s hook: a round cinema lens case rolls off a rooftop edge; the courier dives on her small hoverboard and catches it midair, camera plunging after her into the neon street canyon.',
 '3–8s: close tracking alongside her as she clips the black case to her board; the authentic supplied ONECOOL AIFX gold logo is clearly physically printed on the case. She laughs at the narrow escape and accelerates.',
 '8–14s: exhilarating low glide through a safe empty lane, under a descending cargo platform and up a spiraling parking ramp; colored rain beads slide across the lens, coherent body and board physics.',
 '14–20s: a gap opens between two rooftops; she rides a gently curving maintenance rail, skims through a bright circular architectural opening and lands lightly on the waiting film set.',
 '20–27s: one sweeping reveal shows that the entire city chase has arrived at a magnificent rooftop filmmaking moment: human crew, giant practical lights and a projected abstract aurora filling the skyline; she hands over the lens, the camera operator snaps it into place and captures the wonder.',
 '27–30s: crew celebrates; courier leans casually on her hoverboard, it drifts twenty centimeters away and she takes one quick comic balancing step before recovering with a grin. End beside the physical logo case in the spectacular city.'
 ],'audio':'Original energetic synthwave breakbeat, soft hover-motor hum, rain, air rush, mechanical lens click and a joyful rhythmic finish, no sirens or speech.'
},
{
 'id':'14-the-ink-and-silk-set','title':'The Ink and Silk Set','style':'Painterly wuxia dance fantasy',
 'cast':'An original adult East Asian woman movement director with a vermilion silk costume and long tied dark hair; two adult human performers in ivory. Graceful human faces and athletic nonviolent choreography, no weapons or combat.',
 'world':'A beautiful hybrid of realistic human performance and Chinese ink-wash landscapes: ivory mist, charcoal mountain silhouettes, flowing vermilion silk and tactile water reflections. Cinematic natural faces, sumptuous high-speed fabric motion and painterly world transformations.',
 'beats':[
 '0–3s hook: the heroine snaps open a long red silk ribbon and the empty white space behind her ripples into a vast ink-painted mountain valley; camera follows the ribbon into depth.',
 '3–8s: she steps past a real black film-equipment case bearing the supplied ONECOOL AIFX mark, lifts a small cinema camera and gestures for two human performers to follow her onto a stone terrace.',
 '8–14s: joyful flowing choreography: the human performers leap through trailing silk arcs while ink mountains bloom in their wake, camera tracks close to grounded feet then rises with the ribbon, no fighting.',
 '14–20s: a misty ravine interrupts the dance; the heroine and performers toss their long red fabrics across it, which become an elegant suspended silk bridge. They cross together with playful synchronized steps.',
 '20–27s: glorious sweeping panorama reveals red silk winding through an immense black-and-white painted valley, real human silhouettes dancing across layered terraces, the heroine filming them as her simple motion creates a spectacular world.',
 '27–30s: silk settles back around the heroine beside the logo case; one ribbon tip mischievously lands on her nose, she blows it away and exchanges a delighted human smile with her performers. End in the moving landscape.'
 ],'audio':'Original modern cinematic score using plucked strings, airy flute, restrained hand percussion and rising orchestral warmth, close silk swishes, light footsteps and a playful final breath-like flourish.'
},
{
 'id':'15-the-popcorn-orbit','title':'The Popcorn Orbit','style':'Retro-futurist space comedy',
 'cast':'Two original adult human space filmmakers: a South Asian woman cinematographer with curly dark hair and a burnt-orange flight suit, and an older white male sound recordist with round glasses and a teal suit. Cheerful, believable human performances.',
 'world':'An optimistic 1970s-inspired spaceship cinema cabin: cream molded panels, orange cushions, brushed steel, enormous curved window. Practical miniature space exteriors, gorgeous cosmic color, photoreal tactile interior. All panels blank or geometric without lettering.',
 'beats':[
 '0–3s hook: a single popcorn piece floats out of a bowl; the cinematographer tries to catch it with her mouth, misses, and it drifts toward the giant window.',
 '3–8s: she gently pushes off a seat, collects a cinema camera from a floating black equipment case with the supplied gold ONECOOL AIFX mark, while the recordist steadies a boom microphone and points outside.',
 '8–14s: camera glides with them in convincing zero gravity as they playfully chase the floating popcorn through the cabin; their bodies remain coherent and their human faces expressive, shoes tapping cushions gently.',
 '14–20s: they reach the window and discover an enormous luminous ringed planet; the tiny popcorn aligns with the planet for a funny forced-perspective eclipse. She realizes the shot, raises her camera and carefully frames it.',
 '20–27s: magnificent pull through the curved window to reveal their small spaceship skimming a vast sparkling planetary ring, then back to the two filmmakers capturing cosmic wonder together; nebula colors echo orange and teal.',
 '27–30s: recordist finally catches the popcorn, looks triumphant, then dozens more float out of the bowl behind him. The cinematographer silently laughs, camera still rolling beside the logo case. Finish on the human comic payoff.'
 ],'audio':'Original playful analog-synth space score with warm orchestral strings, soft cabin hum, popcorn taps and a light sparkling percussion cascade for the final gag.'
},
{
 'id':'16-the-desert-ribbon-rally','title':'The Desert Ribbon Rally','style':'Sunlit kinetic fashion-adventure promo',
 'cast':'An original adult Arab woman camera driver with short dark hair, saffron scarf and cream utility suit; two adult human performer friends in cobalt and scarlet on low electric land-sailing boards. Confident friendly faces, protective practical gear.',
 'world':'A pristine sunlit salt flat surrounded by peach sandstone arches, monumental long colored fabrics fluttering in warm wind. Premium photoreal automotive/fashion cinematography, ultra-low tracking cameras, heat shimmer and golden-hour aerials. No other vehicles or hazards.',
 'beats':[
 '0–3s hook: a huge scarlet ribbon whips past camera and reveals the driver skimming inches above the bright salt flat on a low camera buggy, her saffron scarf snapping in the wind.',
 '3–8s: close detail of the real black ONECOOL AIFX equipment case secured on the buggy, then her smiling eyes as she swings the cinema camera toward two human friends sailing alongside.',
 '8–14s: kinetic tracking race through broad sandstone arches, the friends’ long scarlet and cobalt streamers tracing elegant flowing paths; clear human control, graceful safe stunts and rhythmic cuts.',
 '14–20s: a flat empty horizon becomes their opportunity; all three spiral around one another, choreographing long fabric trails that rise on the wind like an enormous floating sculpture.',
 '20–27s: breathtaking aerial climbs from the driver’s delighted face to reveal a kilometer-scale red-and-blue ribbon spiral suspended above the salt mirror, three tiny human creators at its center, real reflected sunlight and tangible fabric texture.',
 '27–30s: they coast to a stop together beside the camera buggy and physical logo case; a loose end of saffron cloth gently covers the driver’s lens, she flips it away with a laugh and catches one last beautiful shot. End on motion.'
 ],'audio':'Original driving hand percussion, pulsing bass and jubilant strings, electric wheel whir, broad wind, taut fabric snaps, warm energetic final musical cadence.'
},
{
 'id':'17-the-museum-of-maybe','title':'The Museum of Maybe','style':'Whimsical live-action match-cut wonder',
 'cast':'An original adult Latina art installer with short dark curls, emerald overalls and white sneakers; a dignified older East Asian male museum guard with navy uniform. Warm expressive adult human performances.',
 'world':'A quiet ivory contemporary art museum at dawn, highly polished stone, huge skylights and surreal practical sculptures. Photoreal elegant symmetrical compositions that become fluid immersive camera moves, rich jewel-color surprises and visual humor.',
 'beats':[
 '0–3s hook: installer balances a tiny red cube on its corner; every enormous sculpture behind her gently tips onto one corner in sympathy. She freezes, eyes widening.',
 '3–8s: she reaches into a black camera case marked with the supplied ONECOOL AIFX logo and starts filming; the guard appears, looks at the impossible balance, then quietly adjusts his hat and joins her.',
 '8–14s: she walks around a hollow circular sculpture and the camera match-moves through it into a sunlit marble canyon; they step through another frame into a room of liquid mirrored curtains, playful discovery rather than danger.',
 '14–20s: a long staircase folds down into a giant spiral slide; she looks at the guard, he gives a tiny dignified nod, and they glide down together with delighted human reactions, camera sweeping alongside.',
 '20–27s: the slide delivers them to a monumental hall where all sculptures slowly orbit in perfect elegant balance, skylight beams creating huge moving patterns; she captures the wondrous scene while the guard does a surprisingly graceful little dance.',
 '27–30s: return to the original tiny cube beside the physical logo case. Guard gently nudges it flat, everything lands neatly back in place, then one small pedestal rotates a final cheeky quarter-turn. The two exchange amused smiles.'
 ],'audio':'Original playful chamber-orchestra score with ticking marimba, sweeping waltz strings and soft bass, polished-stone footfalls, airy transitions and one precise wooden tick at the final pedestal.'
},
{
 'id':'18-the-midnight-light-kitchen','title':'The Midnight Light Kitchen','style':'Saturated culinary VFX comedy',
 'cast':'An original adult Black woman film-lighting artist with close-cropped hair, tangerine chef-style jacket and indigo apron; two adult human crew friends in simple cream workwear. Expressive human faces, no animal ingredients or animal figures.',
 'world':'A sleek midnight studio kitchen with cobalt tile, copper cookware, warm steam and jewel-colored practical lighting. Photoreal food cinematography blended with surreal light effects, dynamic macro transitions, playful human craft and a warm communal payoff.',
 'beats':[
 '0–3s hook: she cracks an ordinary egg-shaped ceramic prop over a pan and a miniature golden sunrise spills out as pure light; her surprised eyes glow warmly in the reflection.',
 '3–8s: she places a black film-lighting case bearing the authentic ONECOOL AIFX mark on the counter, takes a small prism and suddenly grins with an idea; her friends bring a camera and a plain white plate.',
 '8–14s: a joyful rhythmic montage of creating light rather than food: she tosses a ribbon of aurora in a wok, her friend catches rainbow steam in a glass bowl, another films luminous droplets bouncing on a copper spoon.',
 '14–20s: the light grows into an enormous cloud above the counter; instead of panicking they tilt mirrors and the prism together, carefully folding the glow into a perfect beautiful floating sphere above the white plate.',
 '20–27s: camera dives through the luminous sphere into a vast immersive galaxy of color and sparkling abstract light, then pulls back to reveal the three human filmmakers proudly framing this impossible tiny universe in their humble kitchen.',
 '27–30s: they lean in to admire it beside the logo case; one tiny spark leaps onto her tangerine sleeve and turns into a harmless glowing button. She gives it a bemused tap and shares a delighted laugh. Finish on living action, no slate.'
 ],'audio':'Original upbeat percussion-and-brass groove with warm cinematic strings, copper pan rings, prism chimes, gentle magical sizzles and a bright satisfying musical finish.'
}
]

# The user's latest steering makes human casts optional. Three treatments now
# have no people at all, with distinct object-led narrative and visual comedy.
concepts[1].update(cast='No human cast. A palm-sized indigo paper cinema camera on tiny folded wheels is the curious protagonist; it has a lens and moving mechanical parts but no face, limbs or animal features.',beats=[
 '0–3s hook: a tiny paper cinema camera rolls along a flat tabletop; the paper pavement suddenly folds into a staircase and carries it upward like an ingenious mechanical escalator.',
 '3–8s: a black paper equipment case bearing the supplied ONECOOL AIFX mark unfolds, releasing the camera onto a spiral street; a red paper tram glides alongside as the camera tilts its lens in curiosity.',
 '8–14s: an exuberant parade of colorful geometric props dances through the street: folded cones hop, paper wheels spin, balconies accordion open, the viewpoint dives between layers of tactile paper depth.',
 '14–20s: the parade reaches the bare tabletop edge. The little camera nudges a loose paper corner, setting off a satisfying chain reaction that folds the entire road into a giant curved bridge.',
 '20–27s: immersive swoop across the bridge as an elaborate city blooms from a single sheet into radial towers and curved streets; the little camera films the cascading handmade transformation.',
 '27–30s: camera returns beside the physical logo case; a tiny paper step folds unexpectedly under one wheel, it wobbles, catches its balance and gives a playful lens tilt. End with the handmade world still moving.'
])
concepts[3].update(cast='No human or animal cast. Three expressive original clay filmmaking objects: a mustard cinema camera on chunky wheels, a teal articulated studio lamp and a burgundy boom microphone on a little rolling stand. Convey personality through mechanical movement; no faces or animal parts.',beats=[
 '0–3s hook: a tiny wheeled clay cinema camera aims proudly at a perfect clay moon; the moon immediately squashes into a pancake with a soft plop, and the camera lens slowly droops in dismay.',
 '3–8s: the camera rolls out of its black clay equipment case, clearly bearing the supplied gold ONECOOL AIFX mark; the teal lamp bends over the pancake while the burgundy microphone leans in like a curious friend.',
 '8–14s: joyful object teamwork: the lamp warms and bends the pancake into a curved ramp, the microphone nudges little mountains into place, and the camera rolls a circular dolly path around the set.',
 '14–20s: their mistake becomes an ingenious circular moon racetrack; all three filmmaking objects glide along it, bouncing in rhythmic stop-motion as the little camera films their extraordinary playground.',
 '20–27s: spectacular orbit reveals an entire whimsical clay planet made from the studio set, circular track weaving between tactile mountains and pastel cloud rings, the three friendly objects riding together.',
 '27–30s: the camera proudly settles beside the physical logo case; a pea-sized clay moon drops onto its lens hood with a soft plop. The camera tilts up, the lamp bends as if laughing, and the microphone catches the tiny final bounce.'
])
concepts[9].update(cast='No cast and no human hands. The playful protagonists are a copper pan, a small optical prism and ribbons of living colored light. Objects move through clean invisible practical mechanisms, with personality expressed by timing and physical movement, never faces or animal forms.',beats=[
 '0–3s hook: an egg-shaped white ceramic prop rocks, cracks open over a copper pan and spills a tiny golden sunrise made of light; the pan rocks backward in a delighted visual reaction.',
 '3–8s: a black film-lighting equipment case bearing the supplied gold ONECOOL AIFX logo clicks open; a little glass prism slides out onto the counter and catches the sunrise in a brilliant spectrum.',
 '8–14s: joyful rhythmic object choreography: the pan tosses a ribbon of aurora, a glass bowl catches rainbow steam and luminous droplets bounce from spoon to spoon; camera swoops close through jewel-colored reflections.',
 '14–20s: the glow swells into an unruly cloud; the prism rotates, copper lids tilt like mirrors and together they fold the color into one perfectly balanced floating sphere above a plain white plate.',
 '20–27s: camera dives through the sphere into an enormous immersive galaxy of color, flowing light tunnels and sparkling geometric constellations, then pulls back to reveal this tiny universe in the modest studio kitchen.',
 '27–30s: the prism and pan settle proudly beside the logo case; a small loose spark lands in the pan and makes it give one surprised little hop. The sphere pulses warmly in response, a playful visual call-and-response to the final frame.'
])
common_start='''Create a complete ORIGINAL 30-second immersive, FUN campaign film promoting ONECOOL AIFX through imaginative filmmaking and playful visual discovery. Deliver native 1080p, 21:9 MP4 with synchronized original audio. This must be an engaging moving film, not a logo animation, not a mood reel, not a still-image slideshow. Establish a clear protagonist, surprising hook, playful escalation, clever creative action, spectacular payoff and a final comic visual button. Audience should feel inside the action. '''
common_end=''' @Image1 is the supplied AUTHENTIC golden ONE COOL / AIFX brand logo, NOT an environment reference. Use only that exact mark, with its original arrangement and proportions, physically printed on the black filmmaking equipment case described in the story. Give the case a naturally readable medium-close glimpse during seconds 3–8 and a second glimpse in the final scene; the logo must stay on the prop inside the world. It is the ONLY permitted readable lettering. NEVER turn the logo reference into a full-screen still or closing card. No title, subtitle, caption, text box, words, numbers, credits, readable signage, UI, border, watermark, end slate or overlaid graphic. Finish with moving action until the last frame. No dialogue, narration, singing, lyrics or borrowed melodies; use only the original instrumental music and motivated sound effects described. Follow the specified cast exactly: people, animated objects or no cast as the treatment requires. Any human characters must be original fictional adults. No animals, animal characters or animal-shaped mascots. Maintain identity, costume, props and spatial continuity. Build a polished campaign experience with energetic but legible pacing, tangible materials, playful surprises and memorable images. No references to existing franchises, celebrities or copyrighted characters.'''
films=[]
for i,c in enumerate(concepts):
 prompt=common_start+'STYLE: '+c['style']+'. CAST: '+c['cast']+' WORLD AND PHOTOGRAPHY: '+c['world']+' EXACT 30-SECOND STORY: '+' '.join(c['beats'])+' ORIGINAL SOUNDTRACK: '+c['audio']+common_end
 films.append({'id':c['id'],'title':c['title'],'format':c['style'],'reference':'assets/brand/onecool-logo.png','duration':30,'seed':909151+i*101,'prompt':prompt,'creative':c})

def save(p,v):(ROOT/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
save('records/films.json',films)
save('records/campaign.json',{'campaign_name':'ONECOOL AIFX — Ten Ways Into Wonder','campaign_id':'20261015T090200Z-promo-ten','r2_prefix':'campaigns/20261015T090200Z-promo-ten/','bucket':'aifx-studio-campaign','cloudflare_account_id':'74b26d7d5321c33aa49d23709d489ec4','status':'creative_prepared','delivery_mode':'Unmodified native Seedance MP4; no transcoding or post-editing','requested_duration_seconds':30,'requested_resolution':'1080p','requested_ratio':'21:9','purpose':'Fun, immersive ONECOOL AIFX campaign/promotion','reference_strategy':'Authentic logo-only image input; all worlds, faces and performances generated natively from original written treatments.'})
save('records/reference-manifest.json',[{'path':'assets/brand/onecool-logo.png','sha256':hashlib.sha256(logo.read_bytes()).hexdigest(),'purpose':'Authentic brand mark on physical filmmaking equipment; no human-face reference input.'}])
lines=['# Ten Ways Into Wonder','', 'Ten additional 30-second original ONECOOL AIFX campaign/promo films. Each has its own visual medium, setting, comic hook and immersive payoff. Human casts are optional: seven people-led films and three object-led films. No animals or titles/subtitles/text boxes. The authentic logo is supplied as the only image reference for physical in-scene branding. All finished MP4 bytes are delivered unchanged from Seedance.','']
for c in concepts:
 lines+=['## '+c['id']+' — '+c['title'],'',c['style']+'. '+c['world'],'',c['cast'],'',*['- '+b for b in c['beats']],'','Audio: '+c['audio'],'']
(ROOT/'docs/treatments.md').write_text('\n'.join(lines))
(ROOT/'README.md').write_text('# ONECOOL AIFX · Ten Ways Into Wonder\n\nTen distinct fun, immersive campaign films. Requested: 30 seconds, 1080p, 21:9, native synchronized music/effects, no watermark. Casts include people, animated objects and abstract light; no animals or titles/subtitles/text boxes. The authentic brand mark is requested on physical film equipment.\n\nSee [treatments](docs/treatments.md) and [exact API prompts](records/films.json). Each MP4 will be uploaded to private R2 unchanged from Seedance, with no transcoding or post-editing. Native codec, exact dimensions and timing are retained and documented. Videos, signed URLs and credentials are excluded from Git.\n')
for name in ['verify_native.py','prepare_transfer.py','build_manifest.py']:
 src=(REPO/'native-campaign-20261015/scripts'/name).read_text()
 src=src.replace('only the four unmodified','only the unmodified').replace('complete=len(delivered)==4','complete=len(delivered)==len(films)')
 (ROOT/'scripts'/name).write_text(src)
print('Prepared',len(films),'original film treatments in',ROOT)
