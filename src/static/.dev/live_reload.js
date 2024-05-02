'use strict';


let LR_VERBOSE = true;

/**
 * @param {'log'|'info'|'warn'|'error'} type
 * @param  {...any} args
 */
function lrLog(type, ...args) {
  if (!LR_VERBOSE) return;

  console[type](...args);
}

const WS_HOSTNAME = window.location.hostname;
const WS_PORT = 5678;
const WS_URL = `ws://${WS_HOSTNAME}:${WS_PORT}`;
const WS_CLOSE_TIMEOUT = 1000;
const WS_RECONNECT_TIMEOUT = 5000;

/** @type {WebSocket|undefined} */
let lrWebSocket;

/** @type {ReturnType<setTimeout>|undefined} */
let lrwsCloseTimeout;

/**
 * @param {number=} code
 * @param {string=} reason
 */
function lrwsClose(code = 1000, reason = 'Live reload') {
  lrWebSocket?.close(code, reason);
}


/** @type {ReturnType<setTimeout>|undefined} */
let lrwsReconnectTimeout;
let lrwsReconnectTimeoutCount = 0;

function lrwsAutoReconnect() {
  if (lrwsCloseTimeout) {
    clearTimeout(lrwsReconnectTimeout);
    return;
  }

  lrwsReconnectTimeoutCount++;
  lrLog('info', `Reconnecting to ${WS_URL} (${lrwsReconnectTimeoutCount})`);
  lrwsInit();
}

function lrwsCancelAutoReconnect() {
  clearTimeout(lrwsReconnectTimeout);
  lrwsReconnectTimeout = undefined;
}


function lrwsInit() {
  /** @type {WebSocket|undefined} */
  lrWebSocket = new WebSocket(WS_URL);

  lrWebSocket.addEventListener('open', () => {
    lrLog('info', `Connected to ${WS_URL}`);
  });

  lrWebSocket.addEventListener('message', (event) => {
    /** @type {unknown} */
    let msg;
    try {
      msg = JSON.parse(event.data);
      if (
        !msg || typeof msg !== 'object' ||
        !('type' in msg) ||
        typeof msg.type !== 'string'
      ) {
        lrLog('error', 'Invalid message type', msg);
        return;
      }
    }
    catch (e) {
      lrLog('error', 'Failed to parse message', e);
      return;
    }

    lrLog('log', 'Received message', msg);

    if (msg.type === 'TRIGGER_FULL_RELOAD') {
      if (lrwsCloseTimeout) {
        return;
      }

      lrwsCloseTimeout = setTimeout(
        () => {
          window.location.reload();
        },
        WS_CLOSE_TIMEOUT
      );
      return;
    }
  });

  lrWebSocket.addEventListener('close', (event) => {
    lrLog('info', `Disconnected from ${WS_URL}`);

    if (!lrwsCloseTimeout) {
      lrwsReconnectTimeout = setTimeout(
        lrwsAutoReconnect,
        (Math.floor(lrwsReconnectTimeoutCount / 10) + 1) * WS_RECONNECT_TIMEOUT
      );
    }
  });

  lrWebSocket.addEventListener('error', (event) => {
    if (event.currentTarget.readyState !== WebSocket.CLOSED) {
      lrLog('error', 'WebSocket error', event);
    }
  });

  window.addEventListener('beforeunload', () => {
    lrwsClose()
  });
}


window.addEventListener('load', lrwsInit);
