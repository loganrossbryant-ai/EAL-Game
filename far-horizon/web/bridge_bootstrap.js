(function () {
  "use strict";
  if (window.fhGMBridge) return;
  let id;
  try {
    id = sessionStorage.getItem("fh-gm-stage-channel-performance-v3");
    if (!id) {
      id = "fh-gm-" + (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2));
      sessionStorage.setItem("fh-gm-stage-channel-performance-v3", id);
    }
  } catch (_) { id = "fh-gm-" + Date.now(); }
  const channel = new BroadcastChannel(id);
  const allowed = new Set(["move", "interact", "reply", "jump", "cue", "next", "previous", "clue", "hide_clue", "close", "freeze", "clean", "language", "sound", "voice", "replay", "talk", "threat", "board", "glossary", "export", "reset_session", "presentation", "quality", "cover"]);
  let lastActivity=0;
  window.addEventListener('pointermove',()=>{const now=performance.now();if(window.parent!==window&&now-lastActivity>250){lastActivity=now;window.parent.postMessage({app:'far-horizon-preview',kind:'activity'},location.origin);}});
  const queue = [];
  const submit = function(command) {
    if (!command || !allowed.has(command.action) || queue.length > 60) return false;
    queue.push(command);return true;
  };
  channel.onmessage = function (event) {
    const data = event.data;
    if (!data || data.app !== "far-horizon-gm" || data.kind !== "command") return;
    submit(data.command);
  };
  window.fhGMBridge = {
    id: id,
    queue: queue,
    submit: submit,
    publish: function (state) {
      channel.postMessage({ app: "far-horizon-gm", kind: "state", state: state });
      if (window.parent !== window) window.parent.postMessage({app:"far-horizon-preview",kind:"state",state:state},location.origin);
    },
    openDesk: function () {
      const url = new URL("gm.html", window.location.href);
      url.searchParams.set("channel", id);
      const desk = window.open(url.toString(), "far-horizon-gm-desk-"+id, "width=1120,height=820");
      if (desk) { desk.focus(); return true; }
      return false;
    }
  };
})();
