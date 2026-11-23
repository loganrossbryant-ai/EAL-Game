export const sites = {
  ranger: { name: 'Ranger Lin', zh: '林护林员', x: 246, y: 429, icon: '◇' },
  rack: { name: 'Tool rack', zh: '工具架', x: 113, y: 439, icon: '▤',
    clue: 'Two 90 cm boards fit the repair sockets. A coil of rope is clipped to the rack.',
    simple: 'Board · 木板. Both boards are 90 cm long. There is a rope, too.' },
  bridge: { name: 'Broken bridge', zh: '坏了的桥', x: 450, y: 407, icon: '≋',
    clue: 'Two 90 cm boards are missing. The ranger’s inspection tag confirms that the supports are sound.',
    simple: 'The bridge is broken. Two boards are missing. The supports are strong. Each board must be 90 cm.' },
  depth: { name: 'Depth marker', zh: '水深标尺', x: 778, y: 416, icon: '↕',
    clue: 'Today: 38 cm beside the bridge and 16 cm at the ford. The posted limit for this ford is 20 cm.',
    simple: 'The river is 38 cm deep here and 16 cm deep at the ford. For this ford, 20 cm is the limit.' },
  sign: { name: 'Fallen sign', zh: '倒下的路标', x: 934, y: 450, icon: '➜',
    clue: 'Trail map: follow the white stones to the opposite bank. Mark the near and far ends before moving supplies.',
    simple: 'Follow the white stones. Put a marker at each end of the path.' },
};
export const language = {
  elementary: {
    questions: ['Can you help me?', 'Where is the bridge?'],
    bridge: 'We should use the bridge because the boards fit.',
    ford: 'The bridge is broken but the ford is shallow.',
    wrong: 'We should walk through the deep water.',
    stretch: 'The bridge is broken, but the marked path is safe because…',
  },
  middle: {
    questions: ['Where is the safe crossing?', 'How can I check whether the bridge can be repaired?'],
    bridge: 'We should repair the bridge because the boards fit.',
    ford: 'We should use the ford because the water is shallow.',
    wrong: 'We should cross beside the bridge even if the water is deeper.',
    stretch: 'If we mark the ford, the ranger can… / I changed my plan after…',
  },
};
export const repair = {
  bridge: { name: 'Repair the bridge', site: 'bridge', parts: ['First board', 'Second board', 'Rope'],
    targets: ['Left socket', 'Right socket', 'Anchor cleat'],
    guide: 'Fit both boards into the gaps. Then secure the rope to the cleat.' },
  ford: { name: 'Mark the ford', site: 'sign', parts: ['Near marker', 'Far marker', 'Supply pack'],
    targets: ['Near white stone', 'Far white stone', 'Loading spot'],
    guide: 'Mark both ends of the white-stone crossing. Then move the pack to the loading spot.' },
};
