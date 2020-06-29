import defaultSettings from '@/settings'

export default function getPageTitle(pageTitle) {
  if (!window._i18n || !window._i18n.tc('web.title')) {
    return `${title}`
  }
  const title = (window._i18n ? window._i18n.tc('web.title') : '') || defaultSettings.title
  const pageTitle2 = window._i18n ? window._i18n.tc(pageTitle) : ''
  return `${pageTitle2} - ${title}`
}
