import defaultSettings from '@/settings'

export default function getPageTitle(pageTitle) {
  const title = (window._i18n ? window._i18n.tc('web.title') : '') || defaultSettings.title
  if (!window._i18n || !window._i18n.tc('web.title')) {
    return `${title}`
  }
  const pageTitle2 = window._i18n ? window._i18n.tc(pageTitle) : ''

  if (pageTitle2) {
    return `${pageTitle2} - ${title}`
  }
  return `${title}`
}
