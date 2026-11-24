const productionSources = ['supported-elementary', 'student-written'];
const wordGroups = [
  ['Places and materials', ['bridge', 'ford', 'boards', 'white stones']],
  ['Evidence words', ['fit', 'shallow', 'safe', 'measure', '16 cm', '90 cm']],
  ['Linking words', ['I saw', 'because', 'below the limit']],
];

export function recommendationFields({ mode, draft, escape, chinese }) {
  const elementary = mode === 'elementary';
  const support = elementary
    ? `<p id="production-support">Finish a thought about what you saw. Try <em>I saw …</em> or <em>The … fit.</em> Use a word below or type your own.</p>
      <details class="language-bank">
        <summary>Open word bank</summary>
        ${wordGroups.map(([label, words])=>`<p class="small">${label}</p>
          <div class="actions">${words.map(word=>`<button type="button" data-language-word="${word}">${word}</button>`).join('')}</div>`).join('')}
      </details>`
    : `<p id="production-support">Write a short recommendation with one specific detail you observed. Try <em>I recommend … because I measured / found …</em></p>`;
  return `${support}<label for="draft">Your message to Ranger Lin</label>
    ${chinese ? '<p class="small" lang="zh-Hans">用自己组织的英语告诉林护林员你的建议，并说明你观察到了什么。</p>' : ''}
    <textarea id="draft" aria-describedby="production-support" maxlength="1500" required>${escape(draft)}</textarea>
    <p class="small">Lin checks the selected route and evidence. Your teacher can review the writing.</p>`;
}

export function wireRecommendation(container, saveDraft) {
  const draft = container.querySelector('#draft');
  draft.addEventListener('input', ()=>saveDraft(draft.value));
  for (const word of container.querySelectorAll('[data-language-word]')) {
    word.addEventListener('click', ()=>{
      const prefix=draft.value && !/\s$/u.test(draft.value) ? ' ' : '';
      const addition=prefix+word.dataset.languageWord;
      if(draft.value.length+addition.length>draft.maxLength) return;
      draft.value+=addition;
      saveDraft(draft.value);
      draft.focus();
    });
  }
}

export function checkRecommendation(mode, value) {
  const message = value.trim().slice(0,1500);
  const elementary = mode === 'elementary';
  const production = message
    ? (elementary ? 'supported-elementary' : 'student-written') : undefined;
  const words = message.toLocaleLowerCase('en').match(/\p{L}+/gu) ?? [];
  // This floor only guards blank, unfinished and repeated input. Evidence and
  // route are checked separately. A teacher interprets meaning and language.
  const endsInLink = ['because','and','or','the','to'].includes(words.at(-1));
  if(words.length<(elementary?3:5) || new Set(words).size<3 || endsInLink) {
    return {
      ok:false, message, production,
      feedback:elementary
        ? 'Lin needs your observation. Finish a short sentence about what you saw.'
        : 'Lin needs one specific observation. Finish your short recommendation with an evidence detail.',
    };
  }
  return { ok:true, message, production };
}

export function readRecommendation(container, mode) {
  return checkRecommendation(mode,container.querySelector('#draft').value);
}

export function reviewRecommendations(attempts) {
  return attempts.map(attempt=>{
    const produced = productionSources.includes(attempt.production);
    return {
      ...attempt,
      submissionSource:produced ? attempt.production : attempt.message ? 'legacy-route-selection' : 'no-student-output',
      languageReview:produced ? 'teacher-review' : 'not-applicable',
    };
  });
}
