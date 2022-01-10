<script setup>
import { inject, watch, watchEffect } from 'vue';
import realtimeChartVue from './realtimeChart.vue';

const fontColor = inject("fontColor")

const props = defineProps({
    title: String,
    data: Number,
})

const chartOptions = {
    chart: {
        id: 'realtime',
        type: 'radialBar',
        toolbar: {
            show: false
        }
    },
    plotOptions: {
        radialBar: {
            startAngle: -180,
            endAngle: 180,
            hollow: {
                margin: 0,
                size: '70%',
                image: undefined,
                imageOffsetX: 0,
                imageOffsetY: 0,
                position: 'front',
                dropShadow: {
                    enabled: true,
                    top: 3,
                    left: 0,
                    blur: 4,
                    opacity: 0.24
                }
            },
            track: {
                background: '#fff',
                strokeWidth: '67%',
                margin: 0, // margin is in pixels
                dropShadow: {
                    enabled: true,
                    top: -3,
                    left: 0,
                    blur: 4,
                    opacity: 0.15
                }
            },

            dataLabels: {
                show: true,
                name: {
                    show: true,
                    color: fontColor.value,
                    fontSize: '14px'
                },
                value: {
                    offsetY: 10,
                    color: fontColor.value,
                    fontSize: '12px',
                    show: true,
                }
            }
        }
    },
    stroke: {
        lineCap: 'round'
    },
    labels: [props.title],
    fill: {
        colors: [function ({ value, seriesIndex, w }) {
            if (value < 25) {
                return '#87D4F9'
            } else if (value >= 25 && value < 40) {
                return '#61DBC3'
            } else if (value >= 40 && value < 70) {
                return '#95DA74'
            } else if (value >= 70 && value < 90) {
                return '#FAD375'
            } else {
                return '#D9534F'
            }
        }],
    }
}

</script>
<template>
    <apexchart ref="chart" :options="chartOptions" height="175" width="175" :series="[props.data]"></apexchart>
</template>

<style>
</style>