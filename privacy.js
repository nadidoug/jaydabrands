'use strict';
(() => {
  const KEY = 'jaynova_privacy_choice';
  const VERSION = '2026-11-21';
  const AGE = 180 * 24 * 60 * 60 * 1000;
  const banner = document.querySelector('#cookie-banner');
  const dialog = document.querySelector('#cookie-dialog');
  const toggle = document.querySelector('#analytics-consent');
  const globalOptOut = navigator.globalPrivacyControl === true || navigator.doNotTrack === '1';
  const readChoice = () => {
    try { const saved = JSON.parse(localStorage.getItem(KEY)); if (saved?.version === VERSION && Date.now() - saved.savedAt < AGE && saved.savedAt <= Date.now()) return saved; } catch {}
    return null;
  };
  let choice = readChoice();
  const analyticsAllowed = () => choice?.analytics === true && Date.now() - choice.savedAt < AGE && !globalOptOut;
  const update = () => {
    if (banner) banner.hidden = choice !== null;
    if (toggle) { toggle.checked = analyticsAllowed(); toggle.disabled = globalOptOut; }
    const signal = document.querySelector('#privacy-signal');
    if (signal) signal.hidden = !globalOptOut;
    document.querySelectorAll('[data-accept-analytics]').forEach(button => { button.disabled = globalOptOut; });
    const status = document.querySelector('#privacy-status');
    if (status) status.textContent = analyticsAllowed() ? 'Optional download counting is on. Change this anytime in Cookie preferences.' : 'Optional download counting is off. Your downloads still work.';
  };
  const save = analytics => {
    choice = {version:VERSION, analytics:analytics === true && !globalOptOut, savedAt:Date.now()};
    try { localStorage.setItem(KEY, JSON.stringify(choice)); } catch {}
    update();
    if (dialog?.open) dialog.close();
    const status = document.querySelector('#privacy-status');
    if (status) status.textContent = choice.analytics ? 'Optional download counting is on. Change this anytime in Cookie preferences.' : 'Optional download counting is off. Your downloads still work.';
  };
  document.querySelectorAll('[data-essential-only]').forEach(button => button.addEventListener('click', () => save(false)));
  document.querySelectorAll('[data-accept-analytics]').forEach(button => button.addEventListener('click', () => save(true)));
  document.querySelectorAll('[data-cookie-preferences]').forEach(button => button.addEventListener('click', () => { update(); dialog?.showModal(); }));
  document.querySelector('#save-cookie-preferences')?.addEventListener('click', () => save(toggle?.checked === true));
  window.trackGuideDownload = async () => {
    if (!analyticsAllowed()) return;
    const config = window.JAYNOVA_CONFIG;
    if (!config?.analyticsUrl || !config?.publishableKey) return;
    try { await fetch(config.analyticsUrl, {method:'POST', mode:'cors', credentials:'omit', keepalive:true, referrerPolicy:'no-referrer', headers:{'content-type':'application/json','apikey':config.publishableKey}, body:JSON.stringify({product:'starter-guide',consent:true,version:VERSION})}); } catch {}
  };
  document.querySelectorAll('[data-track-guide]').forEach(link => link.addEventListener('click', () => window.trackGuideDownload()));
  window.addEventListener('storage', event => { if (event.key === KEY || event.key === null) { choice = readChoice(); update(); } });
  update();
  if (location.hash === '#cookies') dialog?.showModal();
})();
