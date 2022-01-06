<script setup>
import { ref, inject, watchEffect } from 'vue'
import { NDivider, NSpace, NProgress } from 'naive-ui'

const cpuUsage = ref(0);
const memUsage = ref(0);

const cpuData = ref([])
const memData = ref([])

let old_tx = null;
const net_tx = ref(0);

const auth = inject("auth");
let connection = null;
watchEffect(async () => {
    if (connection) {
        connection.close();
        connection = null;
    }
    if (auth.isAuthenticated.value) {
        connection = new WebSocket('wss://' + import.meta.env.VITE_APP_IDLEREPORTER + '/usage?rate=1&token=' + await auth.getToken());
        connection.onmessage = function (event) {
            let data = JSON.parse(event.data)
            
            cpuUsage.value = data["cpu"];
            cpuData.value = [...cpuData.value.slice(9), [Date.now(), ~~cpuUsage.value]]);
            
            memUsage.value = data["memory"]["used"];
            memData.value = [...memData.value.slice(9), [Date.now(), ~~memUsage.value]]);

            if (old_tx) {
                net_tx.value = ~~((data["net"]["out"] - old_tx) / 1024 / 1024 * 8);
            }

            old_tx = data["net"]["out"];
        }

        connection.onopen = function () {
            console.log("Successfully connected to the websocket server...")
        }
    }
});
const chartOptions = {
    chart: {
        id: 'realtime',
        height: 350,
        type: 'line',
        animations: {
            enabled: true,
            easing: 'linear',
            dynamicAnimation: {
                speed: 1000
            }
        },
        toolbar: {
            show: false
        },
        zoom: {
            enabled: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    title: {
        text: 'Dynamic Updating Chart',
        align: 'left'
    },
    markers: {
        size: 0
    },
    xaxis: {
        crosshairs: { show: false },
        tooltip: { enabled: false },
        labels: {
            show: false
        }
    },
    yaxis: {
        crosshairs: { show: false },
        tooltip: { enabled: false },
        max: 100,
        min: 0,
        labels: {
            show: false
        }
    },
    legend: {
        show: false
    }
}

</script>
<template>
    <n-divider title-placement="left">USAGE</n-divider>
    <apexchart type="line" :options="chartOptions" height="350" :series="[{ name: 'CPU', data: cpuData.value }]"></apexchart>
    <apexchart type="line" :options="chartOptions" height="350" :series="[{ name: 'MEMORY', data: memData.value }]"></apexchart>

    <n-space justify="space-around">
        <n-space justify="center" align="center" :vertical="true">
            <n-progress type="circle" :percentage="cpuUsage" />CPU
        </n-space>
        <n-space justify="center" align="center" :vertical="true">
            <n-progress type="circle" :percentage="memUsage" />MEMORY
        </n-space>
    </n-space>
</template>

<style>
</style>
