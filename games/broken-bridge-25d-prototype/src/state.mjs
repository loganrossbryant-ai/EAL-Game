export const ROUTES = {
  bridge: { clues: ['bridge', 'rack'], pieces: ['boardA', 'boardB', 'rope'] },
  ford: { clues: ['depth', 'sign'], pieces: ['postA', 'postB', 'pack'] },
};
export const SAVE_KEY = 'broken-bridge-v1';
export function fresh(mode = 'elementary') {
  return {
    version: 1, id: globalThis.crypto?.randomUUID?.() ?? String(Date.now()),
    mode, clues: [], question: '', report: '', route: null, pieces: [], delivered: false,
    complete: false, attempts: [], hints: [], practiced: [], stretch: '', zh: mode === 'elementary',
    mute: true, motion: null, x: 278, y: 449, draft: '',
  };
}

export function authorize(state, route, cited, message) {
  const policy = ROUTES[route];
  if (!Object.hasOwn(ROUTES, route) || state.route) return false;
  const accepted = Boolean(state.question && message.trim() &&
    policy.clues.every(id => state.clues.includes(id) && cited.includes(id)));
  state.attempts.push({ route, cited, message, accepted });
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
    for (const name of ['id','question','report','draft','stretch']) {
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
        cited:attempt.cited.filter(id => safe.clues.includes(id)).slice(0,4) }));
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
