//Authored By Eeliya
// function to update date and time every second
function updateDateTime() {
    // get current date and time
    const now = new Date();
    // set formatting options for the date (short weekday, day, and month)
    const options = { weekday: 'short', day: '2-digit', month: 'short' };
    // format the date according to the options
    const formattedDate = now.toLocaleDateString('en-GB', options);
    // format the time (hours and minutes)
    const formattedTime = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    // combine date and time into a single string with spacing
    const datetime = formattedDate + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + formattedTime;  
    // update the HTML element with id 'datetime' with the new date and time
    document.getElementById('datetime').innerHTML = datetime; 
}

// call the updateDateTime function every second
setInterval(updateDateTime, 1000);
// call the updateDateTime function immediately on page load
updateDateTime();