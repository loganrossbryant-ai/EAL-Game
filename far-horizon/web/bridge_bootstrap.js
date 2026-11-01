(function () {
  "use strict";
  if (window.fhGMBridge) return;
  let id;
  try {
    id = sessionStorage.getItem("fh-gm-stage-channel");
    if (!id) {
      id = "fh-gm-" + (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2));
      sessionStorage.setItem("fh-gm-stage-channel", id);
    }
  } catch (_) { id = "fh-gm-" + Date.now(); }
  const channel = new BroadcastChannel(id);
  const allowed = new Set(["jump", "cue", "next", "previous", "clue", "hide_clue", "close", "freeze", "clean", "language", "sound", "voice", "replay", "talk", "threat", "board", "glossary", "export", "reset_session"]);
  const queue = [];
  channel.onmessage = function (event) {
    const data = event.data;
    if (!data || data.app !== "far-horizon-gm" || data.kind !== "command") return;
    if (!data.command || !allowed.has(data.command.action) || queue.length > 60) return;
    queue.push(data.command);
  };
  window.fhGMBridge = {
    id: id,
    queue: queue,
    publish: function (state) { channel.postMessage({ app: "far-horizon-gm", kind: "state", state: state }); },
    openDesk: function () {
      const url = new URL("gm.html", window.location.href);
      url.searchParams.set("channel", id);
      const desk = window.open(url.toString(), "far-horizon-gm-desk", "width=1120,height=820");
      if (desk) { desk.focus(); return true; }
      return false;
    }
  };
})();
