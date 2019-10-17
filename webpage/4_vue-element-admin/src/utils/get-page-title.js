import defaultSettings from '@/settings'

const title = defaultSettings.title || '讯动医疗'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
