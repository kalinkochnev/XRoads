const weekdayName = (dateObj) => moment(dateObj).format('dddd');
const strToTime = (timeStr) => moment(timeStr, "H:mm:ss").toDate();
const parseJSDate = (dateStr) => new Date(Date.parse(dateStr));
const timeObjToStr = (timeObj) => moment(timeObj).format("h:mm  a");
const dateStrToDate = (dateStr) => moment(dateStr, "MM/dd/yyyy").toDate();

const isToday = (otherDate) => {
    if (typeof otherDate == "string") {
        otherDate = parseJSDate(otherDate);
    }
    const today = new Date()
    return otherDate.getDate() == today.getDate() &&
        otherDate.getMonth() == today.getMonth() &&
        otherDate.getFullYear() == today.getFullYear()
}

const eventToStartEnd = (event) => {
    let date = dateStrToDate(event.date);
    let endDate = dateStrToDate(event.date);
    let startTime = utils.strToTime(event.start)
    let endTime = utils.strToTime(event.end)
    moment(date).clone().

    new Date().setTime(start)
    new Date().getTime()
}

export {weekdayName, strToTime, parseJSDate, timeObjToStr, isToday};