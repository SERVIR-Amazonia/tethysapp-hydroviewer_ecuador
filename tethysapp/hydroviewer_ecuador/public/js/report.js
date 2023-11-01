function get_date(now){
    const months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    const dayOfMonth = now.getDate();
    const month = months[now.getMonth()];
    const year = now.getFullYear();
    const hours = now.getHours().toString().padStart(2, "0");
    const minutes = now.getMinutes().toString().padStart(2, "0");
    const formattedDate = `${dayOfMonth} de ${month} de ${year}, ${hours}:${minutes}`;
    return(formattedDate)
}

const now = new Date();
const future = new Date();
future.setDate(now.getDate() + 5)

$("#emision-date").html(get_date(now));
$("#validity-date").html(`Desde ${get_date(now)} hasta ${get_date(future)}`); 

