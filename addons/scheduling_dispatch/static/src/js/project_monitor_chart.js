/** @odoo-module **/
import { Component, useState, onMounted } from "@odoo/owl";

// Ensure Chart.js is loaded from CDN if it's not already available
if (!window.Chart) {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/chart.js";
    script.async = true;
    script.onload = () => console.log("Chart.js Loaded Successfully");
    document.head.appendChild(script);
}

export class ProjectMonitorChart extends Component {
    setup() {
        this.data = useState({ projects: [] });
        onMounted(this.renderChart.bind(this));
    }

    async fetchData() {
        const response = await this.rpc("/project_monitor_chart_data");
        this.data.projects = await response.json();  // Ensure data is properly fetched
        console.log("Fetched Data:", this.data.projects); // Debugging
    }

    async renderChart() {
        await this.fetchData();

        const ctx = document.getElementById("projectMonitorChart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: this.data.projects.map(p => p.name),
                datasets: [
                    {
                        label: "Overdue",
                        data: this.data.projects.map(p => p.overdue_jobs),
                        backgroundColor: "red",
                    },
                    {
                        label: "Next 7 Days",
                        data: this.data.projects.map(p => p.next_7_days_jobs),
                        backgroundColor: "yellow",
                    },
                    {
                        label: "After 7 Days",
                        data: this.data.projects.map(p => p.after_7_days_jobs),
                        backgroundColor: "green",
                    },
                ],
            },
            options: {
                responsive: true,
                indexAxis: "y",
                scales: {
                    x: { stacked: true },
                    y: { stacked: true },
                },
            },
        });
    }
}
