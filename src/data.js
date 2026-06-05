const DEIDADES_META = {
  tutu:     { color:'var(--tutu)',     hex:'#c4a96a', symbol:'☽',  dir:null, attrs:'hijo del humo · iniciador',        smokeRGB:[196,169,106] },
  isis:     { color:'var(--isis)',     hex:'#c4824a', symbol:'🜂', dir:'N',  attrs:'🜂 Fuego · Ished egipcio',          smokeRGB:[196,130,74]  },
  afrodita: { color:'var(--afrodita)', hex:'#b8a0cc', symbol:'🜁', dir:'E',  attrs:'🜁 Aire · Cosmos griego',           smokeRGB:[184,160,204] },
  lilith:   { color:'var(--lilith)',   hex:'#5a9bc4', symbol:'🜄', dir:'S',  attrs:'🜄 Agua · Yggdrasil',               smokeRGB:[90,155,196]  },
  artemisa: { color:'var(--artemisa)', hex:'#7aad6a', symbol:'🜃', dir:'O',  attrs:'🜃 Tierra · Yaxché maya',           smokeRGB:[122,173,106] },
};
const CURSOR_SYMBOLS = { tutu:'☽', isis:'🜂', afrodita:'🜁', lilith:'🜄', artemisa:'🜃' };

let selectedDeidad = 'tutu';
let cargando = false;
let historialUI = [];
let grimorioLocal = [];
let decisionesLocales = [];
let sonidoOn = false;
let audioCtx = null;
let smokeTargetRGB = [196,169,106];
let smokeCurRGB    = [196,169,106];
let proyectoCodigo = null;
