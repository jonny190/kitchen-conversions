/*
 * Consent management placeholder — deliberately empty.
 *
 * Nothing on this site sets a cookie or loads a third-party script, so no consent is
 * required today. Before any advertising is enabled (see ADSENSE_CLIENT in
 * generator/build.py) Google requires a **certified consent management platform** for
 * visitors in the UK, the EEA and Switzerland: ads must not be requested before consent.
 *
 * To activate:
 *   1. choose a Google-certified CMP that integrates with IAB Europe's TCF,
 *   2. paste its loader snippet below,
 *   3. make the AdSense tag load only after the CMP reports consent.
 *
 * Left as a no-op on purpose: an ad tag that fires before consent is worse than no ad.
 */
(function () {
  "use strict";
  window.KC_CONSENT = { cmpLoaded: false, note: "no CMP configured; no ads served" };
})();
