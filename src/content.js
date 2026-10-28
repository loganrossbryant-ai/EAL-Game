export const evidenceDetails = {
 campaign: {title:'The public campaign',source:'Kindred · campaign page',detail:'120 relief kits advertised. The beneficiary count has not been independently verified. A 35% service fee applies.',icon:'Globe'},
 request: {title:'What the community needs',source:'Community notice · Ms Chen',detail:'48 families requested blankets and school supplies. The confirmed needs list arrives tomorrow.',icon:'FileText'},
 email: {title:'Behind the headline',source:'Email · Community coordinator',detail:'The campaign is a sponsored partnership. Ms Chen asks the newsroom to verify the needs before sharing the appeal.',icon:'Mail'},
};
export const glossary = [
 ['claim','主张；声称','Something a person or message says is true.'],
 ['evidence','证据','Information that helps you evaluate a claim.'],
 ['verify','核实','Check whether information is accurate.'],
 ['sponsor','赞助者','A person or business that pays to support something.'],
 ['beneficiary','受益者','A person who receives help.'],
 ['credible','可信的','Supported by trustworthy information.'],
 ['allocate','分配','Decide how resources will be used.'],
 ['impact','影响','The effect an action has on people.'],
];
export const support = {
 2:{label:'More support',intro:'A donation campaign is spreading. Does it meet the community’s needs? Find three sources. Help Maya decide what to share.',frame:'I recommend ___. The campaign says ___. However, Ms Chen says ___. This matters because ___. Our next step should be ___.',prompt:'Use two sources. Explain a difference. Suggest a helpful next step.'},
 3:{label:'Guided support',intro:'A donation campaign is going viral. Before the school shares it, investigate whether its promises match what local families need.',frame:'Although the campaign claims ___, evidence from ___ shows ___. I recommend ___ because ___.',prompt:'Compare two sources, explain a concern, and recommend a next step.'},
 4:{label:'Light support',intro:'An urgent appeal promises a big impact. Investigate its claims, weigh the evidence, and advise the school newsroom before publication.',frame:'The available evidence suggests ___. Despite ___, we should ___ in order to ___.',prompt:'Evaluate the campaign’s credibility and propose a proportionate, evidence-based response.'},
};
