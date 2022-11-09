const dataDiv = document.querySelector(".data")
const mapa = document.querySelector(".body-grid")
const menuItems = document.querySelector(".menu-items")
const menu = document.querySelector(".menu-icon")
const sensorID = document.querySelector(".sensor-id")
const showModals = document.querySelector(".menu-items")
const loginModal = document.querySelector(".login-modal")
const registerModal = document.querySelector(".register-modal")
const settingsModal = document.querySelector(".settings-modal")

const buttons = document.querySelector(".buttons")
const fields = document.querySelector(".settings-items")

const chartsError = document.querySelector(".charts-error")

const userSensors = document.querySelector(".user-menu")

const favouriteImg = document.querySelector(".favourite-img")
const favouriteSensorsDIV = document.querySelector(".favourite-sensors")

const userSensorsButton = document.querySelector(".your-sensors-btn")
const userFavouriteButton = document.querySelector(".your-favourite-btn")
const userSensorsDIV = document.querySelector(".your-sensors-div")
const userFavouriteDIV = document.querySelector(".your-favourite-div")


let chart;


function deleteCharts(){
    if(typeof chart !== "undefined"){
        chart.destroy();
        chart1.destroy();
        chart2.destroy();
        chart3.destroy();
        chart4.destroy();
    }
}

if (buttons) {
buttons.addEventListener("click", event => {
    const nodes = fields.childNodes;
    nodes.forEach(el => {
        if (el.nodeName.toLowerCase() == 'div'){
            if([...el.classList].includes(event.target.name)){
                el.classList.remove("hide");
            }
            else{
                el.classList.add("hide");
            }
     }
    })
})
}


showModals.addEventListener("click", event => {
    const targetClassList = [...event.target.classList]
    if (targetClassList.includes("login-img")){
        event.preventDefault();
        loginModal.classList.toggle("hide");
    }
    if (targetClassList.includes("register-img")){
        event.preventDefault();
        registerModal.classList.toggle("hide");
    }
    if (targetClassList.includes("setting-img")){
        event.preventDefault();
        settingsModal.classList.toggle("hide");
    }
})


map.on('popupopen', async e => {
    const marker = e.popup._source;
    mapa.style.filter = "blur(8px)"
    let res = await fetch('http://127.0.0.1:8000/return-data/?q=' + marker.options.title);
    data = await res.json();

    if(favouriteImg){
        if (favouriteSensors[Number(marker.options.title)]){
            favouriteImg.src = "static/favourite.png";
            favouriteImg.classList.add("favourite")
        }else{
            favouriteImg.src = "static/non-favourite.png";
            favouriteImg.classList.remove("favourite")
        }
    }
    if (data.data.dates.length !== 0){
        chartsError.innerHTML = ""
        const options = {
              chart: {
              height: 350,
              type: 'line',
              zoom: {
                enabled: true
              }
            },
            dataLabels: {
              enabled: false
            },
            stroke: {
              curve: 'straight'
            },
            title: {
              align: 'left'
            },
            grid: {
              row: {
                colors: ['#f3f3f3'],
                opacity: 0.5
              },
            },
            xaxis: {
              categories: data.data.dates,
            }
            };



        options["series"] = [{
            name: "PM1",
            data: data.data.pm1,
        }]
        options["title"]["text"] = 'Air Pollution PM1 by Day'

        chart = new ApexCharts(document.querySelector(".chart0"), options);
        chart.render();



        options["series"] = [{
            name: "PM2.5",
            data: data.data.pm25,
        }]
        options["title"]["text"] = 'Air Pollution PM2.5 by Day'
        chart1 = new ApexCharts(document.querySelector(".chart1"), options);
        chart1.render();



        options["series"] = [{
            name: "PM10",
            data: data.data.pm10,
        }]
        options["title"]["text"] = 'Air Pollution PM10 by Day'
        chart2 = new ApexCharts(document.querySelector(".chart2"), options);
        chart2.render();



        options["series"] = [{
            name: "Temperature",
            data: data.data.temperature,
        }]
        options["title"]["text"] = 'Temperature by Day'
        chart3 = new ApexCharts(document.querySelector(".chart3"), options);
        chart3.render();



        options["series"] = [{
            name: "Pressure",
            data: data.data.pressure,
        }]
        options["title"]["text"] = 'Pressure by Day'
        chart4 = new ApexCharts(document.querySelector(".chart4"), options);
        chart4.render();
    }else{
        chartsError.innerHTML = "<h5>No data available</h5>"
    }

    sensorID.textContent = marker.options.title;
    dataDiv.classList.toggle("hide");
});


map.on('click', e => {
    mapa.style.filter = ""
    sensorID.textContent = ""
    menuItems.classList.add("hide")
    dataDiv.classList.add("hide")

    loginModal && loginModal.classList.add("hide")
    registerModal && registerModal.classList.add("hide")
    settingsModal && settingsModal.classList.add("hide")

    setTimeout(function(){ map.invalidateSize()}, 100);
    deleteCharts();
});


menu.addEventListener("click", e => {
    e.preventDefault();
    menuItems.classList.toggle("hide")
    })

    if(userSensors !== null){
    userSensors.addEventListener("click", event => {
        if([...event.target.classList].includes("user-sensor")){
            map.setView([event.target.dataset.lat, event.target.dataset.lon], map.getZoom());
        }
    })
}

if(favouriteImg !== null){
    favouriteImg.addEventListener("click", async event => {
        let operation = "";

        if ([...event.target.classList].includes("favourite")){
            event.target.src = "static/non-favourite.png";
            event.target.classList.toggle("favourite");
            operation = "delete"
            delete favouriteSensors[Number(sensorID.textContent)];
        }
        else{
            event.target.src = "static/favourite.png";
            event.target.classList.toggle("favourite");
            operation = "add";
            favouriteSensors[Number(sensorID.textContent)] = allSensors[sensorID.textContent]
        }
        let response = await fetch('http://127.0.0.1:8000/modify-favourite/' + operation + '/' + sensorID.textContent);
        data = await response.json();
        updateFavourites();
    })
}
if(favouriteSensorsDIV !== null){
    function updateFavourites(){
        let contentHTML = ""
        favouriteSensorsDIV.innerHTML = ""

        for(const id in favouriteSensors){

            const li = document.createElement('li');
            li.setAttribute('class', "user-sensor");
            li.setAttribute('data-lat', favouriteSensors[id].lat);
            li.setAttribute('data-lon', favouriteSensors[id].lon);
            li.textContent = `${favouriteSensors[id].serial} --- ${favouriteSensors[id].description}`;
            favouriteSensorsDIV.appendChild(li);
        }
    }

    userSensorsButton.addEventListener("click", e => {
        userSensorsDIV.classList.toggle("hide")
    })

    userFavouriteButton.addEventListener("click", e => {
        userFavouriteDIV.classList.toggle("hide")
    })


updateFavourites();
}






