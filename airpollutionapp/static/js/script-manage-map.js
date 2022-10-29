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



if (buttons) {
buttons.addEventListener("click", (event)=>{
    const nodes = fields.childNodes;
    nodes.forEach((el)=>{
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


let chart;


showModals.addEventListener("click", (event)=>{
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


map.on('resize', function(e){
    map.setView([52.10, 19.52], 5);
});


map.on('popupopen', async function(e) {
    if (typeof chart !== "undefined"){
        chart.destroy();
    };

    const marker = e.popup._source;
    mapa.style.filter = "blur(8px)"
    let res = await fetch('http://127.0.0.1:8000/return-data/?q=' + marker.options.title);
    data = await res.json();

    const options = {
          series: [{
            name: "Desktops",
            data: [0, 0, 0, 0, 0, 10, 10, 50, 100]
        }],
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
          text: 'Product Trends by Month',
          align: 'left'
        },
        grid: {
          row: {
            colors: ['#f3f3f3'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        }
        };
    chart = new ApexCharts(document.querySelector(".chart0"), options);
    chart.render();

    chart1 = new ApexCharts(document.querySelector(".chart1"), options);
    chart1.render();

    chart2 = new ApexCharts(document.querySelector(".chart2"), options);
    chart2.render();

    chart3 = new ApexCharts(document.querySelector(".chart3"), options);
    chart3.render();
    sensorID.textContent = marker.options.title;
    dataDiv.classList.toggle("hide");
});


map.on('click', function(e) {
    mapa.style.filter = ""
    sensorID.textContent = ""
    menuItems.classList.add("hide")
    dataDiv.classList.add("hide")

    loginModal && loginModal.classList.add("hide")
    registerModal && registerModal.classList.add("hide")
    settingsModal && settingsModal.classList.add("hide")

    setTimeout(function(){ map.invalidateSize()}, 100);
    if (typeof chart !== "undefined"){
        chart.destroy();
    };
});


menu.addEventListener("click", function(e){
    e.preventDefault();
    menuItems.classList.toggle("hide")
    })
