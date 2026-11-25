import { checkRecommendation, cleanClaim } from './language.mjs';
import {checkRig, newSurvey, readyForPermit, restoreSurvey} from './survey.mjs';

export const ROUTES = {
  bridge: { clues: ['bridge', 'rack'], pieces: ['boardA', 'boardB', 'rope'] },
  ford: { clues: ['depth', 'sign'], pieces: ['postA', 'postB', 'pack'] },
};
export const SAVE_KEY = 'broken-bridge-v1';
export function fresh(mode = 'elementary') {
  return {
    version: 1, id: globalThis.crypto?.randomUUID?.() ?? String(Date.now()),
    mode, fieldEdition:6, survey:newSurvey(), clues: [], question: '', report: '', route: null, pieces: [], delivered: false,
    complete: false, consequence:'', rigTrials:[], attempts: [], fieldActions: [], hints: [], practiced: [], stretch: '', zh: mode === 'elementary',
    mute: true, motion: null, sound: {enabled:false, voice:true, ambience:true, effects:true}, x: 278, y: 449, draft: '',
  };
}

export function authorize(state, route, cited, message, claim) {
  if (!Object.hasOwn(ROUTES, route) || state.route) return false;
  const production=checkRecommendation(state.mode,message,{...claim,route});
  const evidence=Array.isArray(cited)?[...new Set(cited.filter(id=>state.clues.includes(id)))]:[];
  const accepted=Boolean(state.question&&readyForPermit(state)&&production.ok&&ROUTES[route].clues.every(id=>evidence.includes(id)));
  state.attempts.push({
    route,cited:evidence,message:production.message,accepted,
    ...(production.production?{production:production.production}:{}),
    ...cleanClaim(route,production),
  });
  if (accepted) state.route = route;
  return accepted;
}

export function operate(state, piece) {
  const policy = ROUTES[state.route];
  if (!policy || state.delivered || !policy.pieces.includes(piece) || state.pieces.includes(piece)) return false;
  if (piece === policy.pieces[2] && state.pieces.length !== 2) return false;
  state.pieces.push(piece);
  state.delivered = state.pieces.length === 3;
  return true;
}

export function restore(raw) {
  try {
    const saved = JSON.parse(raw);
    if (saved?.version !== 1 || !['elementary', 'middle'].includes(saved.mode)) return null;
    const initial = fresh(saved.mode);
    const safe = { ...initial };
    safe.fieldEdition=saved.fieldEdition===6?6:5;
    safe.survey=restoreSurvey(saved.survey);
    if(safe.fieldEdition===5&&typeof saved.mute==='boolean')safe.sound.effects=!saved.mute;
    for(const key of Object.keys(safe.sound)) {
      if(typeof saved.sound?.[key]==='boolean')safe.sound[key]=saved.sound[key];
    }
    for (const name of ['id','question','report','draft','stretch','consequence']) {
      if (typeof saved[name] === 'string') safe[name] = saved[name].slice(0, 1500);
    }
    for (const name of ['clues','attempts','hints','practiced']) {
      if (Array.isArray(saved[name])) safe[name] = saved[name].slice(0, 200);
    }
    for (const name of ['zh','mute','motion']) {
      if (typeof saved[name] === 'boolean') safe[name] = saved[name];
    }
    safe.x = Number.isFinite(saved.x) ? Math.max(55, Math.min(1005, saved.x)) : initial.x;
    safe.y = Number.isFinite(saved.y) ? Math.max(202, Math.min(490, saved.y)) : initial.y;
    safe.clues = [...new Set(safe.clues.filter(id => ['bridge','rack','depth','sign'].includes(id)))];
    safe.attempts = safe.attempts.filter(attempt => attempt && typeof attempt.message === 'string'
      && typeof attempt.accepted === 'boolean' && Array.isArray(attempt.cited)
      && ['bridge','ford','unsafe'].includes(attempt.route))
      .map(attempt => ({ route:attempt.route, message:attempt.message.slice(0,1500), accepted:attempt.accepted,
        cited:attempt.cited.filter(id => safe.clues.includes(id)).slice(0,4),
        ...(['supported-elementary','student-written'].includes(attempt.production)?{production:attempt.production}:{}),
        ...cleanClaim(attempt.route,attempt) }));
    if(Array.isArray(saved.fieldActions)) {
      const actions=['collected','contact-rejected','rope-hooked','rope-tensioned','placed'];
      const methods=['tap','drag','guide','keyboard'];
      safe.fieldActions=saved.fieldActions.filter(record=>record&&Object.hasOwn(ROUTES,record.route)
        &&ROUTES[record.route].pieces.includes(record.piece)&&actions.includes(record.action)
        &&methods.includes(record.method)&&typeof record.assisted==='boolean').slice(-100)
        .map(({action,piece,route,assisted,method})=>({action,piece,route,assisted,method}));
    }
    if(Array.isArray(saved.rigTrials)) {
      safe.rigTrials=saved.rigTrials.filter(trial=>trial&&['','inner','outer'].includes(trial.path)
        &&typeof trial.cleat==='boolean'&&Number.isInteger(trial.load)&&trial.load>=0&&trial.load<=100).slice(-30)
        .map(({path,cleat,load,assisted})=>({path,cleat,load,result:checkRig(path,cleat,load),assisted:assisted===true}));
    }
    safe.hints = safe.hints.filter(entry => typeof entry === 'string');
    safe.practiced = safe.practiced.filter(entry => typeof entry === 'string');
    if (Object.hasOwn(ROUTES, saved.route) && safe.question && ROUTES[saved.route].clues.every(id=>safe.clues.includes(id))) {
      safe.route = saved.route;
      for (const piece of Array.isArray(saved.pieces)?saved.pieces:[]) operate(safe,piece);
    }
    safe.complete = safe.delivered && saved.complete === true;
    return safe;
  } catch {
    return null;
  }
}
