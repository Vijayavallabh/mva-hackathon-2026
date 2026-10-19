#!/usr/bin/env python3
"""Create a local timed teleprompter for the owner's own-voice recording."""
import argparse
import html
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def rendered():
    pitch=(ROOT/'notes/track2-pitch-v39.md').read_text().split('## Narration\n')[1].split('## Recording notes')[0]
    rows=re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)',pitch.strip(),re.S)
    cards=[];data=[]
    for head,body in rows:
        num,times,title=head.split(' / ');start,end=times.split('-')
        seconds=lambda t:sum(int(x)*m for x,m in zip(t.split(':'),[60,1]))
        data.append(dict(slide=int(num),start=seconds(start),end=seconds(end)))
        cards.append(f'<article id="cue-{num}" tabindex="-1"><h2>Slide {num} · {html.escape(times)} · {html.escape(title)}</h2><p>{html.escape(body)}</p></article>')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-pitch37'; base-uri 'none'; form-action 'none'"><title>Track 2 own-voice rehearsal</title><style>
*{box-sizing:border-box}body{margin:0;background:#f2f7f8;color:#142c3c;font:22px/1.55 Ubuntu,system-ui,sans-serif}header{position:sticky;top:0;background:#123a40;color:white;padding:18px max(20px,calc((100vw - 1000px)/2));z-index:2}h1{font-size:28px;margin:0 0 10px;font-weight:500}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap}button{font:inherit;min-height:48px;padding:8px 16px;border:1px solid #d8eee5;border-radius:5px;color:#123a40;background:#d8eee5;cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid #eae9f6;outline-offset:4px}#clock{font-size:38px;font-variant-numeric:tabular-nums;min-width:120px}main{max-width:1000px;padding:25px 24px;margin:auto}.help{font-size:17px;color:#425c6b}article{padding:22px 0 26px;border-bottom:1px solid #bdcdd4;scroll-margin-top:var(--cue-offset,180px)}article.active{border-left:5px solid #176359;padding-left:20px}h2{font-size:20px;color:#176359;font-weight:500}article p{font-size:clamp(24px,3.2vw,32px);line-height:1.5;max-width:68ch}.timing{color:#d8eee5;font-size:17px;margin:8px 0 0}a{color:#176359}progress{width:100%;height:8px;accent-color:#d8eee5}footer{font-size:15px;margin:28px 0}@media(max-width:500px){header{padding:15px}h1{font-size:23px}button{font-size:17px}main{padding:20px}article{scroll-margin-top:var(--cue-offset,350px)}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style></head><body><header><h1>Your voice / three-minute rehearsal</h1><div class="controls"><output id="clock" aria-label="Rehearsal elapsed time">0:00</output><button id="play">Start rehearsal</button><button id="reset">Reset</button><button id="previous">Previous cue</button><button id="next">Next cue</button></div><p class="timing" id="status" aria-live="polite">Slide 1 of 9. Space starts or pauses. Arrow keys change cues.</p><progress id="progress" max="180" value="0" aria-label="Planned three-minute duration"></progress></header><main><p class="help">Read the paragraphs only. This page guides rehearsal; it does not record audio or video. Cue times are allocations, not measured narration. Rehearse naturally, then measure the final exported video including pauses, transitions and acknowledgement.</p>'''+''.join(cards)+'''<footer><p>364 narration words. Keep the full acknowledgement visible on slide 9. See the recording guide for pronunciation and final checks.</p><p>__ACK__</p></footer></main><script nonce="pitch37">
const cues=__CUES__;let elapsed=0,running=false,anchor=0,active=1;
function time(){return running?Math.min(180,elapsed+(performance.now()-anchor)/1000):elapsed}
function draw(scroll=false){document.documentElement.style.setProperty('--cue-offset',(document.querySelector('header').getBoundingClientRect().height+12)+'px');let t=time();if(t>=180&&running){elapsed=180;running=false}const c=cues.find(c=>t>=c.start&&t<c.end)||cues.at(-1);const changed=c.slide!==active;active=c.slide;document.getElementById('clock').textContent=Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0');document.getElementById('progress').value=t;document.getElementById('play').textContent=running?'Pause rehearsal':'Start rehearsal';document.getElementById('status').textContent=t>=180?'Planned three minutes reached. Measure your actual recording separately.':'Slide '+active+' of 9. Space starts or pauses. Arrow keys change cues.';document.querySelectorAll('article').forEach(a=>a.classList.toggle('active',a.id==='cue-'+active));if(scroll||changed)document.getElementById('cue-'+active).scrollIntoView({behavior:'auto',block:'start'})}
function seek(t){elapsed=Math.max(0,Math.min(180,t));anchor=performance.now();draw(true)}
function toggle(){if(running){elapsed=time();running=false}else{if(elapsed>=180)elapsed=0;anchor=performance.now();running=true}draw()}
function step(d){seek(cues[Math.max(0,Math.min(8,active-1+d))].start)}
document.getElementById('play').onclick=toggle;document.getElementById('reset').onclick=()=>{running=false;seek(0)};document.getElementById('previous').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);
document.addEventListener('keydown',e=>{if(['BUTTON','INPUT','SELECT'].includes(document.activeElement.tagName))return;if(e.code==='Space'){e.preventDefault();toggle()}if(e.code==='ArrowRight'){e.preventDefault();step(1)}if(e.code==='ArrowLeft'){e.preventDefault();step(-1)}});
setInterval(()=>draw(),100);draw();globalThis.Track2Pitch={seek,state:()=>({elapsed:time(),running,slide:active})};
</script></body></html>
'''.replace('__CUES__',json.dumps(data)).replace('__ACK__',' '.join((ROOT/'notes/track2-report-v36.md').read_text().split('## Acknowledgement\n')[1].split()))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    target=ROOT/'notes/track2-teleprompter-v39.html';text=rendered()
    if a.check:
        if target.read_text()!=text:raise ValueError('Teleprompter differs from narration')
    else:target.write_text(text)
    print(json.dumps(dict(generated_prompter_verified=True,bytes=len(text.encode()),video_recorded=False)))
