export const SOUNDINGS=Object.freeze({bridge:38,ford:16});
export const FORD_LIMIT=20;
export const RIG_LOAD={min:60,max:74};
export const newSurvey=()=>({readings:{}, compared:false, asked:false, corrected:false, interview:[], hints:[]});

export function readProbe(station,payout) {
  if(!Object.hasOwn(SOUNDINGS,station)||!Number.isFinite(payout)||payout<0)return null;
  const bed=SOUNDINGS[station];
  return {depth:Math.min(payout,bed),contact:payout>=bed};
}

export function recordDepth(survey,station,payout) {
  const reading=readProbe(station,payout);
  if(!reading?.contact)return false;
  survey.readings[station]=reading.depth;
  return true;
}

export function compareDepth(survey,station,relation) {
  if(Object.keys(SOUNDINGS).some(key=>survey.readings[key]!==SOUNDINGS[key]))return false;
  if(station!=='ford'||relation!=='below'||survey.readings[station]>=FORD_LIMIT)return false;
  survey.compared=true;
  return true;
}

function correctionIssue(sources,note) {
  if(sources.length!==2||!sources.includes('log')||!sources.includes('sounding'))return 'Show Lin the dated log and today’s sounding together.';
  const text=note.toLowerCase().replace(/[’']/g,"'").replace(/\s+/g,' ');
  const today=text.match(/\b(?:today|now|current)\b(?:(?!\byesterday\b)[^.!?]){0,62}/)?.[0]??'';
  const yesterday=text.match(/\byesterday\b(?:(?!\b(?:today|now|current)\b)[^.!?]){0,62}/)?.[0]??'';
  const current=/\b(?:16|sixteen)\b/.test(today)||/\b(?:16|sixteen)\b[^.!?]{0,25}\b(?:today|now)\b/.test(text);
  const below=/(?:\b(?:16|sixteen)\b[^.!?]{0,38}|\b(?:it|that|this|the ford|the water)\s+(?:is|lies)\s+)(?:below|under|less than|shallower than)\s+(?:the\s+)?(?:limit of\s+)?(?:20|twenty)\b/.test(text);
  const wrong=/\b(?:26|twenty[- ]six|38|thirty[- ]eight)\b/.test(today)||
    /\b(?:16|sixteen)\b/.test(yesterday)||/\b(?:not|isn't|isnt|never)\s+(?:be\s+)?(?:below|under|less|shallower)\b/.test(text);
  return current&&below&&!wrong?'':'Name today’s reading, then say how it compares with the posted limit.';
}

export function reviewLog(survey,selected,note) {
  const sources=[...new Set(selected.filter(id=>['log','sounding','rack'].includes(id)))];
  note=note.trim().slice(0,350);
  const issue=!survey.asked?'Ask Lin when she closed the ford.':!survey.compared?'Take and compare both soundings first.':correctionIssue(sources,note);
  survey.interview.push({sources,note,accepted:!issue,output:'constructed',assisted:survey.hints.includes('interview')});
  survey.interview=survey.interview.slice(-30);
  if(!issue)survey.corrected=true;
  return {ok:!issue,feedback:issue};
}

export function restoreSurvey(saved) {
  const survey=newSurvey();
  if(!saved||typeof saved!=='object')return survey;
  for(const [key,depth] of Object.entries(SOUNDINGS)){
    if(saved.readings?.[key]===depth)survey.readings[key]=depth;
  }
  if(saved.compared===true)compareDepth(survey,'ford','below');
  survey.asked=saved.asked===true;
  if(Array.isArray(saved.hints))survey.hints=saved.hints.filter(x=>['survey','interview','rig'].includes(x)).slice(-30);
  if(Array.isArray(saved.interview)){
    for(const attempt of saved.interview.slice(-30)){
      if(Array.isArray(attempt?.sources)&&typeof attempt.note==='string'){
        reviewLog(survey,attempt.sources,attempt.note);
        survey.interview.at(-1).assisted=attempt.assisted===true;
      }
    }
  }
  return survey;
}

export function readyForPermit(state) {
  return state.fieldEdition!==6||state.survey.corrected;
}

export function checkRig(path,cleat,load) {
  if(path!=='inner')return 'edge';
  if(!cleat)return 'cleat';
  if(!Number.isFinite(load)||load<RIG_LOAD.min)return 'slack';
  if(load>RIG_LOAD.max)return 'strain';
  return 'secure';
}
