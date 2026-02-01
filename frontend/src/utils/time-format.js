/**
 * 时间格式化工具函数（格式化 + 解析 双向转换）
 * 新增支持 'yyyy-mm-dd hh:mm:ss' 格式（适配接口返回的 "2023-12-01 10:25:30"）
 * @param {string|number|Date} date - 时间戳/日期字符串/Date对象
 * @param {string} format - 目标格式：'HH:MM' | 'HH:MM:SS' | 'yyyy-mm-dd' | 'yyyy-mm' | 'yyyy-mm-dd hh:mm:ss'
 * @returns {string} 格式化后的时间字符串
 */
export function formatDate(date, format) {
  // 处理空值
  if (!date) return '';

  let targetDate;
  if (typeof date === 'string') {
    targetDate = new Date(date.replace(/-/g, '/'));
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

  // 统一格式为小写（兼容HH:MM和hh:mm）
  const lowerFormat = format.toLowerCase();
  
  // 根据格式返回结果
  switch (lowerFormat) {
    case 'hh:mm':
      return `${hours}:${minutes}`;
    case 'hh:mm:ss':
      return `${hours}:${minutes}:${seconds}`;
    case 'yyyy-mm-dd':
      return `${year}-${month}-${day}`;
    case 'yyyy-mm-dd hh:mm:ss': // ✅ 新增：支持完整格式
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    case 'yyyy-mm':
      return `${year}-${month}`;
    default:
      console.warn('不支持的格式:', format);
      return '';
  }
}

/**
 * 时间解析函数（反向转换：格式化字符串 → 时间戳/Date对象）
 * 新增支持 'yyyy-mm-dd hh:mm:ss' 格式解析
 * @param {string} dateStr - 格式化的时间字符串（如 '2023-12-01 10:25:30'、'14:30'）
 * @param {string} format - 输入字符串的格式：'HH:MM' | 'HH:MM:SS' | 'yyyy-mm-dd' | 'yyyy-mm' | 'yyyy-mm-dd hh:mm:ss'
 * @param {boolean} returnTimestamp - 是否返回时间戳（默认返回Date对象）
 * @returns {Date|number|''} 解析后的Date对象/时间戳，解析失败返回空字符串
 */
export function parseDate(dateStr, format, returnTimestamp = false) {
  // 处理空值
  if (!dateStr || !format) return '';

  // 定义解析正则（匹配对应格式的字符串），新增完整格式正则
  const regexMap = {
    'HH:MM': /^(\d{2}):(\d{2})$/,
    'HH:MM:SS': /^(\d{2}):(\d{2}):(\d{2})$/,
    'yyyy-mm-dd': /^(\d{4})-(\d{2})-(\d{2})$/,
    'yyyy-mm-dd hh:mm:ss': /^(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})$/, // ✅ 新增
    'yyyy-mm': /^(\d{4})-(\d{2})$/,
  };

  // 统一格式为大写（兼容传入小写的情况）
  const upperFormat = format.toUpperCase();
  const regex = regexMap[upperTypeFormat];
  
  if (!regex) {
    console.warn('不支持的解析格式:', format);
    return '';
  }

  const match = dateStr.match(regex);
  if (!match) {
    console.warn(`时间字符串 ${dateStr} 不符合 ${format} 格式`);
    return '';
  }

  let targetDate;

  switch (upperTypeFormat) {
    case 'HH:MM': {
      const [, hours, minutes] = match;
      targetDate = new Date(
        new Date().getFullYear(),
        new Date().getMonth(),
        new Date().getDate(),
        parseInt(hours),
        parseInt(minutes),
        0
      );
      break;
    }
    case 'HH:MM:SS': {
      const [, hours, minutes, seconds] = match;
      targetDate = new Date(
        new Date().getFullYear(),
        new Date().getMonth(),
        new Date().getDate(),
        parseInt(hours),
        parseInt(minutes),
        parseInt(seconds)
      );
      break;
    }
    case 'yyyy-mm-dd': {
      const [, year, month, day] = match;
      targetDate = new Date(
        parseInt(year),
        parseInt(month) - 1, // 月份从0开始
        parseInt(day),
        0,
        0,
        0
      );
      break;
    }
    case 'yyyy-mm-dd hh:mm:ss': { // ✅ 新增：解析完整格式
      const [, year, month, day, hours, minutes, seconds] = match;
      targetDate = new Date(
        parseInt(year),
        parseInt(month) - 1,
        parseInt(day),
        parseInt(hours),
        parseInt(minutes),
        parseInt(seconds)
      );
      break;
    }
    case 'yyyy-mm': {
      const [, year, month] = match;
      targetDate = new Date(
        parseInt(year),
        parseInt(month) - 1,
        1, // 默认当月1号
        0,
        0,
        0
      );
      break;
    }
  }

  // 验证解析结果
  if (isNaN(targetDate.getTime())) {
    console.warn('解析后的日期无效:', dateStr);
    return '';
  }

  // 返回时间戳或Date对象
  return returnTimestamp ? targetDate.getTime() : targetDate;
}

// ---------------------- 快捷格式化方法 ----------------------
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
 * 快捷方法：格式化为 yyyy-mm-dd hh:mm:ss（核心新增）
 * 适配接口返回的 "2023-12-01 10:25:30" 格式
 * @param {string|number|Date} date
 * @returns {string}
 */
export function formatToYYYYMMDDHHMMSS(date) {
  return formatDate(date, 'yyyy-mm-dd hh:mm:ss');
}

/**
 * 快捷方法：格式化为 yyyy-mm
 * @param {string|number|Date} date
 * @returns {string}
 */
export function formatToYYYYMM(date) {
  return formatDate(date, 'yyyy-mm');
}

// ---------------------- 快捷解析方法 ----------------------
/**
 * 快捷方法：解析 HH:MM 格式字符串 → Date对象
 * @param {string} dateStr - 如 '14:30'
 * @param {boolean} returnTimestamp - 是否返回时间戳
 * @returns {Date|number|''}
 */
export function parseHHMM(dateStr, returnTimestamp = false) {
  return parseDate(dateStr, 'HH:MM', returnTimestamp);
}

/**
 * 快捷方法：解析 HH:MM:SS 格式字符串 → Date对象
 * @param {string} dateStr - 如 '14:30:45'
 * @param {boolean} returnTimestamp - 是否返回时间戳
 * @returns {Date|number|''}
 */
export function parseHHMMSS(dateStr, returnTimestamp = false) {
  return parseDate(dateStr, 'HH:MM:SS', returnTimestamp);
}

/**
 * 快捷方法：解析 yyyy-mm-dd 格式字符串 → Date对象
 * @param {string} dateStr - 如 '2026-02-01'
 * @param {boolean} returnTimestamp - 是否返回时间戳
 * @returns {Date|number|''}
 */
export function parseYYYYMMDD(dateStr, returnTimestamp = false) {
  return parseDate(dateStr, 'yyyy-mm-dd', returnTimestamp);
}

/**
 * 快捷方法：解析 yyyy-mm-dd hh:mm:ss 格式字符串 → Date对象（核心新增）
 * 适配接口返回的 "2023-12-01 10:25:30" 格式
 * @param {string} dateStr - 如 '2023-12-01 10:25:30'
 * @param {boolean} returnTimestamp - 是否返回时间戳
 * @returns {Date|number|''}
 */
export function parseYYYYMMDDHHMMSS(dateStr, returnTimestamp = false) {
  return parseDate(dateStr, 'yyyy-mm-dd hh:mm:ss', returnTimestamp);
}

/**
 * 快捷方法：解析 yyyy-mm 格式字符串 → Date对象
 * @param {string} dateStr - 如 '2026-02'
 * @param {boolean} returnTimestamp - 是否返回时间戳
 * @returns {Date|number|''}
 */
export function parseYYYYMM(dateStr, returnTimestamp = false) {
  return parseDate(dateStr, 'yyyy-mm', returnTimestamp);
}

// ---------------------- 额外工具：Date对象转指定格式字符串（按需使用） ----------------------
/**
 * 将Date对象直接转为 "yyyy-mm-dd hh:mm:ss" 格式字符串
 * @param {Date} dateObj - Date对象
 * @returns {string} 如 "2023-12-01 10:25:30"
 */
export function dateObjToFullString(dateObj) {
  if (!(dateObj instanceof Date) || isNaN(dateObj.getTime())) {
    console.warn('无效的Date对象:', dateObj);
    return '';
  }
  return formatToYYYYMMDDHHMMSS(dateObj);
}