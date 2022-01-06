<script setup>

const props = defineProps({
    title: String,
    max: Number,
    data: Array,
    length: Number
})

const chartOptions = {
    chart: {
        id: 'realtime',
        height: 350,
        type: 'area',
        animations: {
            enabled: true,
            easing: 'linear',
            dynamicAnimation: {
                speed: 650
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
        text: props.title,
        align: 'left'
    },
    markers: {
        size: 0
    },
    xaxis: {
        crosshairs: { show: false },
        labels: {
            show: false
        },
        type: 'datetime'
    },
    yaxis: {
        crosshairs: { show: false },
        tooltip: { enabled: true },
        max: props.max,
        min: 0,
        labels: {
            show: false
        }
    },
    legend: {
        show: false
    },
    tooltip: { enabled: false },
    states: {
        hover: {
            filter: {
                type: 'none',
            }
        },
    },

}

</script>
<template>
    <apexchart
        :options="chartOptions"
        height="350"
        :series="[{ name: props.name, data: props.data.length < props.length ? props.data : props.data.slice(-props.length) }]"
    ></apexchart>
</template>

<style>
</style>