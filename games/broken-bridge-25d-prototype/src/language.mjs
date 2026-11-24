const productionSources = ['supported-elementary', 'student-written'];
const evidenceClaims = {
  bridge: {
    facts: {
      'matching-boards': 'The rack has boards the same length as the missing ones.',
      'sound-supports': 'The inspection tag says the supports are sound.',
      'short-boards': 'The boards on the rack are too short.',
    },
    inferences: {
      'fill-sockets': 'Fit the matching boards into the open sockets.',
      'repair-deck': 'Replace the deck boards while keeping the supports.',
      'walk-open-gap': 'Try to cross the open gap as it is.',
    },
  },
  ford: {
    facts: {
      'ford-depth': 'The ford is 16 cm deep, below its 20 cm limit.',
      'white-stones': 'The sign points to the line of white stepping stones.',
      'deep-ford': 'The ford is 38 cm deep, above its limit.',
    },
    inferences: {
      'use-shallows': 'Use the ford within its posted limit.',
      'flag-stones': 'Mark both ends of the stepping-stone route.',
      'ignore-limit': 'Ignore the marker and walk through deep water.',
    },
  },
};

const numberWords = {
  one:1, two:2, four:4, eight:8, sixteen:16, eighteen:18, twenty:20, 'thirty eight':38,
  eighty:80, ninety:90, 'one hundred':100, 'one hundred sixty':160,
  'one hundred and sixty':160, 'nine hundred':900,
};

function measurements(text) {
  const numbers=Object.keys(numberWords).sort((a,b)=>b.length-a.length).join('|');
  const units='mm|millimeters?|millimetres?|cm|centimeters?|centimetres?|m|meters?|metres?';
  const expression=new RegExp(`\\b(\\d+(?:\\.\\d+)?|${numbers})\\s*(${units})\\b`,'g');
  return [...text.matchAll(expression)].map(([,quantity,unit])=>{
    const number=numberWords[quantity]??Number(quantity);
    if(unit==='mm'||unit.startsWith('milli')) return number/10;
    if(unit==='m'||unit.startsWith('met')) return number*100;
    return number;
  });
}

const factChecks = {
  'matching-boards': {
    feedback:'Name how the boards or planks match the gap, or use their 90 cm length.',
    supports(text, sizes) {
      if(sizes.some(size=>size!==90)) return false;
      if(/\b(?:not|never|cannot|can t|don t|doesn t)\s+(?:really\s+)?(?:fit|match)\b|\btoo\s+(?:short|long)\b/.test(text)) return false;
      const topic=/\b(?:boards?|planks?|deck|timber|wood|sockets?|gap|pieces?)\b/.test(text);
      const fit=/\b(?:fit\w*|match\w*|same (?:length|size|width)|right (?:length|size|dimensions)|long enough|wide enough|fill\w*)\b/.test(text);
      return topic&&(fit||sizes.includes(90));
    },
  },
  'sound-supports': {
    feedback:'Tell Lin what the tag says about the supports, beams or frame.',
    supports(text) {
      const topic=/\b(?:supports?|beams?|frames?|framing|structure|foundations?)\b/.test(text);
      const status=/\b(?:sound|strong|solid|stable|intact|undamaged|safe|sturdy|still good|okay|ok|(?:not|aren t|isn t|weren t) (?:been )?(?:damaged|broken|weakened))\b/.test(text);
      const conflict=/\b(?:supports?|beams?|frames?|framing|structure|foundations?)\s+(?:(?:are|is|were|have|has|still|now)\s+)*(?:failed|broken|weak|unsafe|unstable|unsound|damaged|collapsed|not\s+(?:sound|strong|solid|stable|intact|safe))\b/.test(text);
      return topic&&status&&!conflict;
    },
  },
  'ford-depth': {
    feedback:'Use the ford’s depth, or explain that the water is shallow enough or within the posted limit.',
    supports(text) {
      const focus=/\b(?:ford|shallows?|crossing)\b/;
      const clauses=text.split(/[!?;,]|\.(?!\d)|\b(?:and|but|whereas|while)\b/);
      const relevant=clauses.filter(clause=>!(/\bbridge\b/.test(clause)&&!focus.test(clause)));
      const observation=relevant.join(' ');
      const fordSizes=measurements(observation);
      if(/\b(?:too deep|above (?:the )?limit|over (?:the )?limit|not shallow|not safe|not under (?:the )?limit)\b/.test(observation)) return false;
      // A sentence can contrast the bridge and ford. Check the first reading
      // after "ford" so mentioning the right number elsewhere cannot swap them.
      const attached=observation.match(/\bford\b([^.!;,]{0,54})/);
      const direct=attached?measurements(attached[1])[0]:undefined;
      if(direct!==undefined&&direct!==16&&direct!==20) return false;
      const topic=/\b(?:ford|water|shallows?|crossing|depth|limit|river)\b/.test(observation);
      const safe=/\b(?:shallow\w*|within|below|under|less than)\b/.test(observation);
      return topic&&(fordSizes.includes(16)||(safe&&fordSizes.every(size=>size===20)));
    },
  },
  'white-stones': {
    feedback:'Mention the white stones, stepping stones, or the sign that points to their path.',
    supports(text) {
      if(/\b(?:no|not any|aren t any)\s+(?:white\s+|stepping\s+)?(?:stones?|rocks?)\b/.test(text)) return false;
      return /\b(?:white|stepping|marked|flat)\s+(?:stones?|rocks?)\b/.test(text) ||
        (/\b(?:sign|map|arrow|marker)\b/.test(text)&&/\b(?:points?|directs?|shows?|leads?|stones?|rocks?|path)\b/.test(text));
    },
  },
};

const sameRouteInferences = {
  bridge: ['fill-sockets', 'repair-deck'],
  ford: ['use-shallows', 'flag-stones'],
};

const wordGroups = [
  ['Places and materials', ['bridge', 'ford', 'boards', 'beams', 'white stones']],
  ['Evidence words', ['fit', 'strong', 'shallow', '16 cm', '90 cm']],
  ['Linking words', ['I saw', 'because', 'below the limit']],
];

export function recommendationFields({ mode, draft, escape, chinese }) {
  const elementary = mode === 'elementary';
  const support = elementary
    ? `<p id="production-support">Use your chosen observation. Try <em>The … fit.</em> or <em>I saw …</em> and add what you saw. Use the word bank or type your own words.</p>
      <details class="language-bank">
        <summary>Open word bank</summary>
        ${wordGroups.map(([label,words])=>`<p class="small">${label}</p>
          <div class="actions">${words.map(word=>`<button type="button" data-language-word="${word}">${word}</button>`).join('')}</div>`).join('')}
      </details>`
    : `<p id="production-support">Write a short reason that uses your chosen observation to explain the route. Try <em>I recommend … because I measured / found …</em></p>`;
  return `<fieldset id="claim-slots" hidden>
    <legend>Connect what you saw to what you’ll do</legend>
    <label for="claim-fact">What did you observe?</label><select id="claim-fact"></select>
    <label for="claim-link">What does that let you do safely?</label><select id="claim-link"></select>
    </fieldset>${support}<label for="draft">Your message to Ranger Lin</label>
    ${chinese?'<p class="small" lang="zh-Hans">选择一项观察结果，并用自己的话说明它如何支持你的路线。</p>':''}
    <textarea id="draft" aria-describedby="production-support" maxlength="1500" required>${escape(draft)}</textarea>
    <p class="small">Lin checks whether your observation, next step and message go together. Your teacher reviews your writing.</p>`;
}

export function wireRecommendation(container, saveDraft) {
  const draft=container.querySelector('#draft');
  const route=container.querySelector('#recommend');
  const slots=container.querySelector('#claim-slots');
  const updateClaims=()=>{
    const options=evidenceClaims[route.value];
    slots.hidden=!options;
    for(const [select,entries] of [[slots.querySelector('#claim-fact'),options?.facts],
      [slots.querySelector('#claim-link'),options?.inferences]]) {
      select.innerHTML='<option value="">Choose from the field notes</option>'+
        Object.entries(entries??{}).map(([id,label])=>`<option value="${id}">${label}</option>`).join('');
    }
  };
  updateClaims();
  route.addEventListener('change',updateClaims);
  draft.addEventListener('input',()=>saveDraft(draft.value));
  for(const word of container.querySelectorAll('[data-language-word]')) {
    word.addEventListener('click',()=>{
      const prefix=draft.value&&!/\s$/u.test(draft.value)?' ':'';
      const addition=prefix+word.dataset.languageWord;
      if(draft.value.length+addition.length>draft.maxLength) return;
      draft.value+=addition;
      saveDraft(draft.value);
      draft.focus();
    });
  }
}

export function cleanClaim(route, claim) {
  if(!Object.hasOwn(evidenceClaims,route)) return {};
  const options=evidenceClaims[route];
  return {
    ...(Object.hasOwn(options.facts,claim?.fact)?{fact:claim.fact}:{}),
    ...(Object.hasOwn(options.inferences,claim?.inference)?{inference:claim.inference}:{}),
  };
}

export function checkRecommendation(mode, value, {route,...claim}={}) {
  const message=(typeof value==='string'?value.trim():'').slice(0,1500);
  const elementary=mode==='elementary';
  const production=message?(elementary?'supported-elementary':'student-written'):undefined;
  const content=cleanClaim(route,claim);
  const reject=feedback=>({ok:false,message,production,...content,feedback});
  if(!content.fact||!content.inference) {
    return reject('Choose an observation and the safe next step it supports.');
  }
  const check=factChecks[content.fact];
  if(!check||!sameRouteInferences[route].includes(content.inference)) {
    return reject('That observation or next step does not match the field notes. Check the clues for your route.');
  }
  const normalized=message.toLocaleLowerCase('en').replace(/[’']/gu,' ').replace(/\p{Dash_Punctuation}/gu,' ');
  const words=normalized.match(/\p{L}+/gu)??[];
  const endsInLink=['because','and','or','the','to'].includes(words.at(-1));
  if(words.length<(elementary?3:4)||new Set(words).size<3||endsInLink||!check.supports(normalized,measurements(normalized))) {
    return reject('Connect your words to the observation you selected. '+check.feedback);
  }
  return {ok:true,message,production,...content};
}

export function readRecommendation(container, mode, route) {
  return checkRecommendation(mode,container.querySelector('#draft').value,{
    route,
    fact:container.querySelector('#claim-fact').value,
    inference:container.querySelector('#claim-link').value,
  });
}

export function reviewRecommendations(attempts) {
  return attempts.map(attempt=>{
    const produced=productionSources.includes(attempt.production);
    const {fact,inference}=cleanClaim(attempt.route,attempt);
    return {
      ...attempt,
      submissionSource:produced?attempt.production:attempt.message?'legacy-route-selection':'no-student-output',
      languageReview:produced?'teacher-review':'not-applicable',
      structuredEvidence:fact&&inference?{fact,inference}:null,
    };
  });
}
