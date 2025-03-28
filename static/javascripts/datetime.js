function updateDateTime() {
    const now = new Date();
    const options = { weekday: 'short', day: '2-digit', month: 'short' };
    const formattedDate = now.toLocaleDateString('en-GB', options);
    const formattedTime = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    
    const datetime = formattedDate + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + formattedTime;  
    document.getElementById('datetime').innerHTML = datetime; 
}

setInterval(updateDateTime, 1000);
updateDateTime();