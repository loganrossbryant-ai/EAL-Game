// Versioned, local-only student work. No names, accounts, or remote analytics.
export const STORAGE_KEY = 'signal-save-v1';
export const initialState = {
  version: 1,
  level: 3,
  evidence: [],
  sources: [],
  talked: false,
  dialogueChoice: null,
  response: '',
  decision: '',
  feedback: null,
  completed: false,
  room: 'newsroom',
  position: null,
  responses: [],
};

const EVIDENCE_IDS = ['campaign', 'request', 'email'];
const DECISIONS = ['pause', 'publish', 'verify'];
const freshState = () => ({ ...initialState, evidence: [], sources: [], responses: [] });
const validText = (value, limit = 8000) => typeof value === 'string' ? value.slice(0, limit) : '';
const evidenceIds = (value) => Array.isArray(value)
  ? [...new Set(value.filter((id) => EVIDENCE_IDS.includes(id)))] : [];

function cleanFeedback(value) {
  if (!value || typeof value !== 'object' || typeof value.passed !== 'boolean') return null;
  return {
    passed: value.passed,
    title: validText(value.title, 200),
    message: validText(value.message, 2000),
    strengths: Array.isArray(value.strengths) ? value.strengths.filter((v) => typeof v === 'string').slice(0, 10) : [],
    nextSteps: Array.isArray(value.nextSteps) ? value.nextSteps.filter((v) => typeof v === 'string').slice(0, 10) : [],
  };
}

function cleanResponse(value) {
  if (!value || typeof value !== 'object' || typeof value.response !== 'string') return null;
  const result = {
    response: validText(value.response),
    decision: DECISIONS.includes(value.decision) ? value.decision : '',
    evidence: evidenceIds(value.evidence),
    sources: evidenceIds(value.sources),
    feedback: cleanFeedback(value.feedback),
  };
  // Accept the common timestamp names used by the UI without treating arbitrary
  // objects from local storage as application state.
  for (const key of ['timestamp', 'at', 'submittedAt']) {
    if (typeof value[key] === 'string' || typeof value[key] === 'number') result[key] = value[key];
  }
  return result;
}

export function loadProgress(storage) {
  try {
    const raw = (storage ?? globalThis.localStorage)?.getItem(STORAGE_KEY);
    if (!raw) return freshState();
    const saved = JSON.parse(raw);
    if (!saved || Array.isArray(saved) || saved.version !== 1) return freshState();
    const feedback = cleanFeedback(saved.feedback);
    const evidence = evidenceIds(saved.evidence);
    const responses = Array.isArray(saved.responses) ? saved.responses.map(cleanResponse).filter(Boolean).slice(-100) : [];
    // Opening a new draft clears its feedback, but must not undo an earned story
    // milestone. A successful submitted message remains in the local history.
    const completed = saved.completed === true && evidence.length === EVIDENCE_IDS.length
      && (feedback?.passed === true || responses.some((entry) => entry.feedback?.passed === true));
    const position = saved.position && Number.isFinite(saved.position.x) && Number.isFinite(saved.position.y)
      && saved.position.x >= 0 && saved.position.x <= 1280 && saved.position.y >= 0 && saved.position.y <= 780
      ? { x: saved.position.x, y: saved.position.y } : null;
    return {
      ...freshState(),
      level: [2, 3, 4].includes(saved.level) ? saved.level : 3,
      evidence,
      talked: saved.talked === true,
      dialogueChoice: typeof saved.dialogueChoice === 'string' ? saved.dialogueChoice.slice(0, 200) : null,
      response: validText(saved.response),
      decision: DECISIONS.includes(saved.decision) ? saved.decision : '',
      feedback,
      completed,
      room: saved.room === 'courtyard' && completed ? 'courtyard' : 'newsroom',
      position,
      sources: evidenceIds(saved.sources),
      responses,
    };
  } catch {
    // Disabled storage or damaged save data must never prevent playing.
    return freshState();
  }
}

export function saveProgress(state, storage) {
  try {
    const target = storage ?? globalThis.localStorage;
    if (!target?.setItem) return false;
    target.setItem(STORAGE_KEY, JSON.stringify({ ...state, version: 1 }));
    return true;
  } catch {
    return false;
  }
}

/**
 * A transparent formative completeness check, not a language-quality grade.
 * Explicit source choices and a concrete detail are checked together. All three
 * editorial decisions can proceed; teachers review the reasoning and language.
 */
export function evaluateResponse({ response = '', decision = '', evidence = [], sources } = {}) {
  const collected = evidenceIds(evidence);
  const cited = evidenceIds(sources ?? evidence).filter((id) => collected.includes(id));
  const words = typeof response === 'string'
    ? response.trim().match(/[\p{L}\p{N}]+(?:['’%-][\p{L}\p{N}]+)*/gu) ?? [] : [];
  const text = typeof response === 'string' ? response.toLowerCase() : '';
  const detailFound = /\b48\s+(?:local\s+)?famil(?:y|ies)\b/.test(text)
    || /\b120\s+(?:(?:donation|emergency)\s+)?kits\b/.test(text)
    || /\b35\s*(?:%|percent|per cent)/.test(text)
    || /\bblankets?\b/.test(text) && /\b(?:supplies|requested|need|asked)\b/.test(text);
  const strengths = [];
  const nextSteps = [];

  if (collected.length === 3) strengths.push('You investigated all three sources.');
  else nextSteps.push('Read and collect the campaign page, the noticeboard, and Ms Chen’s email before sending your recommendation.');

  if (DECISIONS.includes(decision)) strengths.push('You chose a clear editorial action.');
  else nextSteps.push('Choose whether to pause the post, publish with context, or verify the claim first.');

  if (cited.length >= 2) strengths.push('You attached at least two sources for Maya to check.');
  else nextSteps.push('Attach at least two different collected sources to support your message.');

  if (words.length >= 20) strengths.push('You developed a message of at least 20 words.');
  else nextSteps.push(`Develop your explanation to at least 20 words (currently ${words.length}). Explain what the evidence means for your decision.`);

  if (detailFound) strengths.push('You included a concrete detail from the investigation.');
  else nextSteps.push('Include a specific source detail, such as 48 families, 120 kits, the 35% fee, or the request for blankets and supplies. Explain why it matters.');

  const passed = nextSteps.length === 0;
  return {
    passed,
    title: passed ? 'Your recommendation is ready for Maya.' : 'Maya has a revision request.',
    message: passed
      ? 'Your message meets the evidence checklist. Maya will use your selected action to plan the next step. This automatic check confirms completeness; your teacher can review the accuracy, reasoning, and English in your saved response.'
      : 'You can revise and send again. These automatic checks help you prepare a complete message; they do not grade your English or decide whether your argument is convincing.',
    strengths,
    nextSteps,
  };
}
