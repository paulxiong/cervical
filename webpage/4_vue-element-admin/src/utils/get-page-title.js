import defaultSettings from '@/settings'

export default function getPageTitle(pageTitle) {
  const title = (window._i18n ? window._i18n.tc('web.title') : '') || defaultSettings.title
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
