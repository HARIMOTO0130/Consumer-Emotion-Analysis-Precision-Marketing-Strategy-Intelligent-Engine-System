/**
 * 时间格式化工具函数
 * @param {string|number|Date} date - 时间戳/日期字符串/Date对象
 * @param {string} format - 目标格式：'HH:MM' | 'HH:MM:SS' | 'yyyy-mm-dd' | 'yyyy-mm'
 * @returns {string} 格式化后的时间字符串
 */
export function formatDate(date, format) {
  // 处理空值
  if (!date) return '';

  let targetDate;
  if (typeof date === 'string') {
    targetDate = new Date(date);
  } else if (typeof date === 'number') {
    targetDate = new Date(date);
  } else if (date instanceof Date) {
    targetDate = date;
  } else {
    console.warn('无效的时间格式:', date);
    return '';
  }

  // 处理无效日期
  if (isNaN(targetDate.getTime())) {
    console.warn('无法解析的日期:', date);
    return '';
  }

  // 补零函数
  const padZero = (num) => num.toString().padStart(2, '0');

  // 提取时间组件
  const year = targetDate.getFullYear();
  const month = padZero(targetDate.getMonth() + 1);
  const day = padZero(targetDate.getDate());
  const hours = padZero(targetDate.getHours());
  const minutes = padZero(targetDate.getMinutes());
  const seconds = padZero(targetDate.getSeconds());

  // 根据格式返回结果
  switch (format) {
    case 'HH:MM':
      return `${hours}:${minutes}`;
    case 'HH:MM:SS':
      return `${hours}:${minutes}:${seconds}`;
    case 'yyyy-mm-dd':
      return `${year}-${month}-${day}`;
    case 'yyyy-mm':
      return `${year}-${month}`;
    default:
      console.warn('不支持的格式:', format);
      return '';
  }
}

/**
 * 快捷方法：格式化为 HH:MM
 * @param {string|number|Date} date
 * @returns {string}
 */
export function formatToHHMM(date) {
  return formatDate(date, 'HH:MM');
}

/**
 * 快捷方法：格式化为 HH:MM:SS
 * @param {string|number|Date} date
 * @returns {string}
 */
export function formatToHHMMSS(date) {
  return formatDate(date, 'HH:MM:SS');
}

/**
 * 快捷方法：格式化为 yyyy-mm-dd
 * @param {string|number|Date} date
 * @returns {string}
 */
export function formatToYYYYMMDD(date) {
  return formatDate(date, 'yyyy-mm-dd');
}

/**
 * 快捷方法：格式化为 yyyy-mm
 * @param {string|number|Date} date
 * @returns {string}
 */
export function formatToYYYYMM(date) {
  return formatDate(date, 'yyyy-mm');
}